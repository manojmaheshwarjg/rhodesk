"""extract -> resolve -> monitor -> classify.

Deliberately NOT an agent loop. Extraction and classification are arithmetic
and rules, which keeps the demo deterministic; the only judgement calls handed
to a model are entity resolution and the call script. The one genuinely
agentic thing in the system is the voice agent on the phone, and ElevenLabs
runs that.
"""
from __future__ import annotations

import hashlib
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import uuid
from collections import defaultdict
from datetime import date, datetime, timezone

from . import config, db, history, research_seed
from .llm import LLMClient
from . import rho as rho_module
from .rho import RhoClient
from .tavily import TavilyClient

OPEN_INVOICE_STATUSES = {"unpaid", "overdue"}
LEGAL_SUFFIXES = {"INC", "LLC", "LTD", "CORP", "CORPORATION", "CO", "COMPANY",
                  "PTY", "GMBH", "BV", "SA", "AG", "PLC", "LP", "LLP", "THE"}

# Tokens that are never the brand: payment-processor prefixes, TLDs, regions,
# and the generic nouns that follow a brand in a card descriptor.
NOISE_TOKENS = {
    "SQ", "SQUARE", "MSFT", "PAYPAL", "PP", "TST", "SP", "WWW", "HTTP",
    "COM", "NET", "ORG", "IO", "SO", "APP", "AI", "DEV", "CO",
    "EMEA", "APAC", "AMER", "USA", "US", "UK", "EU", "INTL", "GLOBAL",
    "MONTHLY", "ANNUAL", "SUBSCRIPTION", "SUBSCR", "RENEWAL", "BILLING",
    "HOSTING", "MONITORING", "SERVICES", "SERVICE", "SOFTWARE", "LABS",
    "PAYROLL", "GROUP", "GRP", "HOLDINGS", "PARTNERS", "SOLUTIONS",
    "PAYMENT", "PAYMENTS", "INVOICE", "STORE", "ONLINE", "PURCHASE",
    "SVCS", "SVC", "TECHNOLOGIES", "TECH", "SYSTEMS", "ENTERPRISES",
}

# Kept upper when tidying a name. A heuristic cannot tell AWS from WEB, so this
# is an explicit list rather than a clever rule.
ACRONYMS = {
    "AWS", "DDOG", "PPTY", "LLP", "LLC", "PLC", "SVC", "API", "HR", "IT",
    "AI", "ML", "SAAS", "CRM", "ERP", "VPN", "SMS", "USD", "EUR", "GBP", "NYC",
}


# The name resolver sometimes annotates a sector it suspects is made up, as in
# "Retail (Sample Data)". That is the model hedging, not a sector, and it reads
# as fake on every screen that shows it.
_SECTOR_HEDGE = re.compile(
    r"\s*\((?=[^)]*\b(?:sample|example|fictional|fictitious|placeholder|test|demo|dummy|mock)\b)[^)]*\)",
    re.IGNORECASE)


def clean_sector(sector: str | None) -> str:
    return _SECTOR_HEDGE.sub("", sector or "").strip()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalise(name: str) -> str:
    """Collapse a ledger string toward the company behind it.
    'AMZN MKTP US*2K4L5' and 'AMAZON WEB SVCS' do not collapse to the same
    key, which is exactly why the resolve step exists."""
    s = (name or "").upper()
    s = re.sub(r"[*#]+\s*\w*$", " ", s)          # trailing store/ref codes
    s = re.sub(r"\b\d{3,}\b", " ", s)             # long digit runs
    s = re.sub(r"[^A-Z0-9 ]+", " ", s)
    tokens = [t for t in s.split() if t and t not in LEGAL_SUFFIXES]
    return " ".join(tokens).strip()


def brand_key(name: str) -> str:
    """The token a human would recognise as the brand.

    Ledger descriptors bury the brand in noise: "MSFT*GITHUB", "FIGMA MONTHLY",
    "VERCEL*HOSTING", "ASANA.COM". Taking the first substantial token that is
    not a processor prefix, a TLD, a region or a generic noun collapses most of
    those onto each other without a model.

    It deliberately does NOT merge "AWS EMEA" with "AMAZON WEB SVCS", or
    "DATADOG INC" with "DDOG*MONITORING". Those need to know what the company
    is actually called, which is the job of the resolve step.
    """
    normalised = normalise(name)
    for token in normalised.split():
        if len(token) >= 4 and token not in NOISE_TOKENS:
            return token
    return normalised


def sig_tokens(name: str) -> frozenset[str]:
    """Tokens that actually distinguish one company from another."""
    return frozenset(tok for tok in normalise(name).split()
                     if tok not in NOISE_TOKENS and len(tok) > 2)


def prettiest(aliases: list[str]) -> str:
    """Pick the most human spelling out of the ledger's variants and tidy it.

    Ledger descriptors shout and carry freight: "ASANA.COM", "ATLASSIAN*JIRA",
    "DEEL PAYROLL". Strip the separators and the freight, then title-case,
    keeping short vowel-less tokens upper so AWS does not become Aws.
    """
    if not aliases:
        return ""
    best = min(aliases, key=lambda a: (sum(c in "*#&_." for c in a),
                                       0 if any(c.islower() for c in a) else 1,
                                       len(a)))
    if any(c.islower() for c in best):
        return best                                  # already human, leave it
    words = [w for w in re.split(r"[^A-Za-z0-9]+", best) if w]
    keep = [w for w in words
            if w.upper() not in NOISE_TOKENS and w.upper() not in LEGAL_SUFFIXES]
    keep = keep or words
    out = []
    for w in keep:
        out.append(w.upper() if w.upper() in ACRONYMS else w.capitalize())
    return " ".join(out)


def slug(name: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")
    return base or "cp-" + hashlib.sha1(name.encode()).hexdigest()[:8]


def _days_since(value: str | None) -> int | None:
    if not value:
        return None
    try:
        d = date.fromisoformat(value[:10])
    except ValueError:
        return None
    return (config.reading_date() - d).days


# --- 1. extract ------------------------------------------------------------

def extract(rho: RhoClient | None = None) -> dict[str, dict]:
    """Pull the ledger and build one bucket per counterparty NAME.
    Aliases are merged later, in resolve()."""
    owns_client = rho is None
    rho = rho or rho_module.client()
    try:
        accounts = rho.accounts()
        transactions = rho.transactions()
        customers = rho.customers()
        invoices = rho.invoices()
    finally:
        if owns_client:
            rho.close()

    # Internal transfers name your OWN accounts as the counterparty. Those are
    # not relationships, so drop them: account names from /accounts, the
    # account_name seen on transactions, and Rho's own product names.
    internal = {normalise(a.get("account_name", "")) for a in accounts}
    internal |= {normalise(t.get("account_name", "")) for t in transactions}
    internal |= {normalise(n) for n in
                 ("Rho", "Rho Rewards", "Rho Savings", "Rho Treasury",
                  "Rho Card Payment", "Rewards", "Treasury", "Payroll",
                  "Bill Pay", "Rho Card Repayment")}
    internal.discard("")

    buckets: dict[str, dict] = {}

    def bucket(name: str) -> dict:
        brand = brand_key(name) or name.upper()
        sig = sig_tokens(name)
        # Walk the buckets already claiming this brand token; join the first
        # one whose core is compatible, otherwise start a new one.
        n = 0
        while True:
            key = brand if n == 0 else f"{brand}#{n}"
            b = buckets.get(key)
            if b is None:
                buckets[key] = {
                    "key": key, "core": sig, "aliases": set(), "display_name": name,
                    "money_in": 0, "money_out": 0, "txn_count": 0,
                    "charge_dates": [], "charge_amounts": [],
                    "invoices": [], "customer_ids": set(),
                    "card_charges": {}, "contact_email": None,
                }
                buckets[key]["aliases"].add(name)
                return buckets[key]
            core = b["core"]
            if sig <= core or core <= sig:
                b["core"] = core & sig or core
                b["aliases"].add(name)
                return b
            n += 1

    # Card and bank activity -> who you pay, and who pays you.
    for txn in transactions:
        name = (txn.get("counterparty_name") or "").strip()
        if not name or normalise(name) in internal:
            continue
        b = bucket(name)
        cents = (txn.get("amount") or {}).get("amount", 0)
        if cents >= 0:
            b["money_in"] += cents
        else:
            b["money_out"] += -cents
            b["charge_dates"].append(txn.get("initiated_at", "")[:10])
            b["charge_amounts"].append(-cents)
            card = txn.get("card_id")
            if card:
                b["card_charges"][card] = b["card_charges"].get(card, 0) + 1
        b["txn_count"] += 1

    # Invoices -> receivables. invoice.customer is {"id": ...}.
    by_customer = {c["id"]: c for c in customers}
    for inv in invoices:
        cid = (inv.get("customer") or {}).get("id")
        cust = by_customer.get(cid)
        if not cust:
            continue
        b = bucket(cust.get("legal_name") or "Unknown customer")
        b["customer_ids"].add(cid)
        b["contact_email"] = b["contact_email"] or cust.get("email")
        status = (inv.get("status") or "").lower()
        total = (inv.get("total") or {}).get("amount", 0)
        overdue_days = _days_since(inv.get("due_date"))
        b["invoices"].append({
            "id": inv.get("id"),
            "number": inv.get("invoice_number"),
            "total": total,
            "status": status,
            "due_date": inv.get("due_date"),
            "days_overdue": overdue_days if (overdue_days or 0) > 0 else 0,
            "open": status in OPEN_INVOICE_STATUSES,
        })

    # Derive per-bucket aggregates.
    for b in buckets.values():
        open_invs = [i for i in b["invoices"] if i["open"]]
        b["open_invoices"] = len(open_invs)
        b["outstanding"] = sum(i["total"] for i in open_invs)
        b["oldest_days"] = max((i["days_overdue"] for i in open_invs), default=0)
        b["recurring"], b["monthly_spend"] = _recurrence(b)
        # Two or more cards each billed repeatedly by the same vendor is a
        # duplicate subscription, which is a real finding. One card billed
        # monthly is just a subscription.
        repeat_cards = [n for n in b["card_charges"].values() if n >= 3]
        b["duplicate"] = 1 if (b["recurring"] and len(repeat_cards) >= 2) else 0

    total_ar = sum(b["outstanding"] for b in buckets.values()) or 1
    for b in buckets.values():
        b["ar_share"] = round(b["outstanding"] / total_ar, 4)

    db.log_run("extract", f"{len(transactions)} transactions, {len(invoices)} invoices, "
                          f"{len(buckets)} counterparty names")
    return buckets


def _recurrence(b: dict) -> tuple[int, int]:
    """Is this a subscription, and roughly what does it cost a month?

    Checks cadence AND amount. Irregular spend (parking, meals, legal fees) can
    easily average out to a monthly-looking gap, so a median gap alone flags
    half the ledger. A real subscription also charges close to the same amount
    every time.
    """
    pairs = sorted(zip(b["charge_dates"], b.get("charge_amounts", [])))
    pairs = [(d, a) for d, a in pairs if d and a]
    if len(pairs) < 3 or b["money_out"] <= 0:
        return 0, 0
    try:
        parsed = [(date.fromisoformat(d), a) for d, a in pairs]
    except ValueError:
        return 0, 0

    gaps = [(parsed[i + 1][0] - parsed[i][0]).days for i in range(len(parsed) - 1)]
    gaps = [g for g in gaps if g > 0]
    if len(gaps) < 2:
        return 0, 0
    median_gap = sorted(gaps)[len(gaps) // 2]
    if not 20 <= median_gap <= 40:
        return 0, 0
    # Cadence must be regular, not merely monthly on average.
    off_cadence = sum(1 for g in gaps if not 18 <= g <= 45)
    if off_cadence > len(gaps) * 0.35:
        return 0, 0

    amounts = [a for _, a in parsed]
    mean = sum(amounts) / len(amounts)
    if mean <= 0:
        return 0, 0
    spread = sum(abs(a - mean) for a in amounts) / len(amounts) / mean
    if spread > 0.35:            # amounts all over the place: not a plan
        return 0, 0
    return 1, round(mean)


# --- 2. resolve ------------------------------------------------------------

RESOLVE_SYSTEM = """You resolve messy accounting ledger strings to the real
company behind them. Merchant descriptors are abbreviated, carry store codes
and vary between systems, so several strings often mean one company.

For each group you are given, return the real company name, its primary
domain if you are confident, and a short sector label. Also say which of the
supplied groups should be MERGED because they are the same company.

Return JSON: {"companies": [{"keys": ["KEY1","KEY2"], "name": "...",
"domain": "...", "sector": "...", "note": "..."}]}
Use the exact key strings you were given. Every key must appear exactly once."""


def resolve(buckets: dict[str, dict], llm: LLMClient | None = None) -> list[dict]:
    """Merge alias groups into companies. Falls back to one company per
    normalised key when no model is configured."""
    llm = llm or LLMClient()
    keys = sorted(buckets)
    fallback = {"companies": [
        {"keys": [k], "name": prettiest(sorted(buckets[k]["aliases"])), "domain": "",
         "sector": "", "note": "grouped by brand token, no model configured"}
        for k in keys]}

    listing = "\n".join(
        f'- {k}  (seen as: {", ".join(sorted(buckets[k]["aliases"]))})'
        for k in keys)
    result = llm.json_call(RESOLVE_SYSTEM,
                           f"Ledger groups:\n{listing}", fallback, max_tokens=3000)
    # A rate-limited resolve returns the fallback, which groups nothing. The
    # run still completes and still looks normal, so unless this is recorded
    # the next diff reports the ungrouping as counterparties appearing and
    # disappearing. It is a degraded run, not news.
    degraded = llm.live and not llm.last_call_ok

    companies, seen = [], set()
    for item in (result.get("companies") or []):
        member_keys = [k for k in (item.get("keys") or []) if k in buckets and k not in seen]
        if not member_keys:
            continue
        seen.update(member_keys)
        companies.append(_merge(member_keys, buckets, item))

    for k in keys:                                # anything the model dropped
        if k not in seen:
            companies.append(_merge([k], buckets, {"name": buckets[k]["display_name"]}))

    for company in companies:
        company["degraded"] = degraded
    note = f"{len(keys)} names -> {len(companies)} companies"
    db.log_run("resolve", note + (" (DEGRADED, model unavailable)" if degraded else ""))
    return companies


def _merge(keys: list[str], buckets: dict[str, dict], meta: dict) -> dict:
    aliases, invoices = set(), []
    agg = defaultdict(int)
    contact_email = None
    for k in keys:
        b = buckets[k]
        aliases |= b["aliases"]
        invoices += b["invoices"]
        contact_email = contact_email or b.get("contact_email")
        agg["duplicate"] = max(agg["duplicate"], b.get("duplicate", 0))
        for field in ("money_in", "money_out", "txn_count", "open_invoices",
                      "outstanding", "monthly_spend"):
            agg[field] += b[field]
        agg["oldest_days"] = max(agg["oldest_days"], b["oldest_days"])
        agg["recurring"] = max(agg["recurring"], b["recurring"])

    name = meta.get("name") or prettiest(sorted(aliases))
    return {
        # The id is the first ledger key in the group, NOT a slug of the
        # resolved name. The model picks the name and can change its mind
        # between runs ("Amazon Web Services" one day, "Amazon.com, Inc." the
        # next), which would read as one counterparty leaving and another
        # arriving, taking its call history with it. The ledger keys come from
        # the transaction descriptors and do not move.
        "id": slug(sorted(keys)[0]),
        # Every id this group could have had. When the resolver regroups
        # between runs, this is what tells the diff that a counterparty was
        # absorbed rather than deleted.
        "member_key_ids": [slug(k) for k in sorted(keys)],
        "display_name": name,
        "aliases": sorted(aliases),
        "domain": meta.get("domain") or "",
        "sector": clean_sector(meta.get("sector")),
        "resolution_note": meta.get("note") or "",
        "money_in": agg["money_in"], "money_out": agg["money_out"],
        "txn_count": agg["txn_count"], "open_invoices": agg["open_invoices"],
        "outstanding": agg["outstanding"], "oldest_days": agg["oldest_days"] or None,
        "recurring": agg["recurring"], "monthly_spend": agg["monthly_spend"],
        "duplicate": agg["duplicate"],
        "invoices": invoices, "contact_email": contact_email,
        "ar_share": 0.0,
    }


# --- 3. monitor ------------------------------------------------------------

SIGNAL_SYSTEM = """You read web search results about a company that a business
either owes money to or is owed money by, and extract only signals that change
how that business should act.

Severity: "severe" for distress that threatens payment (down round, layoffs,
insolvency, litigation, breach); "warn" for something to watch (leadership
exit, slowing hiring, price change); "info" for neutral context; "positive"
for news that means they can pay (funding, growth, acquisition).

Reject anything you cannot tie to THIS EXACT company. A similar or shared name
is not enough: many companies share a word. If the result is about a different
business that happens to have a similar name, discard it. If you are unsure,
discard it. Returning nothing is the correct answer for a company with no
public footprint.

Ignore marketing copy, listicles, pricing pages, and vendor comparison sites.
A company publishing its prices is not news.
Return JSON: {"signals": [{"severity": "...", "title": "...", "detail": "...",
"source_url": "...", "source_name": "..."}]}
Return an empty list if nothing is material. Never invent a source_url: use
one of the supplied result urls."""


def monitor(company: dict, tavily: TavilyClient | None = None,
            llm: LLMClient | None = None) -> list[dict]:
    tavily = tavily or TavilyClient()
    llm = llm or LLMClient()
    name = company["display_name"]

    queries = [f"{name} funding OR layoffs OR lawsuit OR acquisition news"]
    if company["outstanding"] > 0:
        queries.append(f"{name} financial difficulty OR insolvency OR down round")
    if company["recurring"]:
        queries.append(f"{name} pricing per user per month")

    results, seen_urls = [], set()
    searched, failed = 0, 0
    for q in queries[:3]:
        searched += 1
        for r in tavily.search(q, topic="news" if "news" in q else "general",
                               max_results=4):
            if r.get("error"):
                failed += 1
                continue
            key = (r.get("url") or "") + "|" + (r.get("title") or "")
            if key in seen_urls:
                continue
            seen_urls.add(key)
            results.append(r)

    # Whether this counterparty was actually researched, as opposed to looked
    # up against a service that refused. A run built on refusals must not
    # report the resulting absence of signals as good news.
    company["researched_ok"] = failed < searched

    # For a subscription vendor, read the pricing page properly.
    if company["recurring"]:
        pricing_urls = [r["url"] for r in results
                        if "pricing" in (r.get("url") or "").lower()][:2]
        for page in tavily.extract(pricing_urls):
            results.append({"title": f"{name} pricing page",
                            "url": page.get("url", ""),
                            "content": (page.get("raw_content") or "")[:2000],
                            "extracted": True})

    fallback = {"signals": _rule_signals(company, results)}
    digest = "\n\n".join(
        f"URL: {r.get('url')}\nTITLE: {r.get('title')}\n{(r.get('content') or '')[:700]}"
        for r in results[:8])
    payload = (f"Company: {name}\n"
               f"Known domain: {company.get('domain') or 'unknown'}\n"
               f"Relationship: {'they owe us' if company['outstanding'] else 'we pay them'}\n"
               f"Outstanding: ${company['outstanding'] / 100:,.2f}\n"
               f"Monthly spend: ${company['monthly_spend'] / 100:,.2f}\n\n"
               f"Search results:\n{digest}")
    parsed = llm.json_call(SIGNAL_SYSTEM, payload, fallback, max_tokens=1800)

    signals, seen = [], set()
    for s in (parsed.get("signals") or [])[:8]:
        key = (s.get("title") or "").strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        signals.append({
            "id": signal_key(company["id"], s.get("title") or "",
                             s.get("source_url") or ""),
            "counterparty_id": company["id"],
            "severity": (s.get("severity") or "info").lower(),
            "title": s.get("title") or "Signal",
            "detail": s.get("detail") or "",
            "source_url": s.get("source_url") or "",
            "source_name": s.get("source_name") or _host(s.get("source_url") or ""),
            "observed_at": _now(),
        })
    return signals


def signal_key(counterparty_id: str, title: str, url: str) -> str:
    """Content-addressed signal id.

    A random id per run meant the same news story counted as new every single
    run, which makes "what changed since yesterday" meaningless. Hashing the
    counterparty, the headline and the page it came from means a story found
    twice is one row that was seen twice.
    """
    host_path = re.sub(r"^https?://(www\.)?", "", (url or "").strip().lower()).rstrip("/")
    # Key on the page, not the headline. The model rewrites the same story a
    # different way every run, so including the title would make every signal
    # new every time and drown the briefing in its own noise. The title is
    # only the key when there is no source to point at.
    body = host_path or " ".join(
        re.sub(r"[^a-z0-9 ]+", " ", (title or "").lower()).split())
    return hashlib.sha1(f"{counterparty_id}|{body}".encode()).hexdigest()[:20]


def _rule_signals(company: dict, results: list[dict]) -> list[dict]:
    """Used when no model is configured: keyword spotting, honestly labelled."""
    out = []
    for r in results[:5]:
        blob = f"{r.get('title','')} {r.get('content','')}".lower()
        severity = "info"
        # Check the bad news first: "raises at a reduced valuation" is a down
        # round, and matching "raises" before that reads it as good news.
        if any(w in blob for w in ("down round", "reduced valuation", "layoff",
                                   "insolven", "lawsuit", "bankrupt", "administration",
                                   "did not participate", "half its prior")):
            severity = "severe"
        elif any(w in blob for w in ("raises", "series ", "funding", "acquisition")):
            severity = "positive"
        elif "pricing" in blob or "per user" in blob:
            severity = "warn"
        if severity == "info":
            continue
        out.append({"severity": severity, "title": r.get("title", "Signal"),
                    "detail": (r.get("content") or "")[:240],
                    "source_url": r.get("url", ""),
                    "source_name": _host(r.get("url", ""))})
    return out


def _host(url: str) -> str:
    m = re.match(r"https?://([^/]+)", url or "")
    return m.group(1) if m else ""


# --- 4. classify -----------------------------------------------------------

BRIEF_SYSTEM = """You write the brief for an AI voice agent about to telephone
a company on behalf of a business.

Tone: professional, warm, never threatening. The agent discloses it is an AI
in its first sentence. It must never reveal that it researched the company
online: the research shapes HOW it speaks, never what it says.

Return JSON:
{"opening_line": "one or two sentences the agent says first",
 "context": ["facts the agent may rely on"],
 "may_agree": ["what it is authorised to accept"],
 "must_not": ["what it must never do or say"],
 "rationale": "one sentence on why this posture, for the human reviewer"}"""


def classify(company: dict, signals: list[dict]) -> dict:
    """Rules pick the posture. The model only writes the words."""
    # "Cedar & Co" matches a healthcare startup, a fraud conviction and an
    # insolvency, none of them this customer. Without a resolved domain we
    # cannot tell, so unverified distress is recorded but never escalates.
    verified = bool(company.get("domain"))
    severities = {s["severity"] for s in signals}
    if not verified:
        severities.discard("severe")
    outstanding = company["outstanding"]
    overdue = (company["oldest_days"] or 0) >= config.OVERDUE_DAYS

    if outstanding > 0 and overdue and "severe" in severities:
        posture, risk = "cover", "high"
        recommendation = "Escalate today, get a dated commitment"
    elif outstanding > 0 and overdue:
        posture, risk = "collect", ("medium" if "warn" in severities else "low")
        if not verified and any(s["severity"] == "severe" for s in signals):
            recommendation = "Call, but verify who they are first"
        recommendation = "Call and agree a payment date"
    elif company["recurring"] and company.get("duplicate"):
        posture, risk = "cut", "low"
        recommendation = "Cancel the duplicate subscription"
    elif company["recurring"] and _price_moved(signals):
        posture, risk = "cut", "low"
        recommendation = "Call to renegotiate"
    elif "severe" in severities:
        # Distress at a vendor matters (a payroll provider in trouble is a
        # supply risk) but there is no receivable to chase, so it stays a
        # watch item with the risk flag raised rather than a calling posture.
        posture, risk = "watch", "high"
        recommendation = "No exposure, but worth knowing"
    else:
        posture, risk = "watch", "none"
        recommendation = "None"

    company["posture"] = posture
    company["risk"] = risk
    company["recommendation"] = recommendation
    company["rationale"] = ""
    return company


def _price_moved(signals: list[dict]) -> bool:
    """A vendor publishing a price list is not a finding. A vendor CHANGING its
    price is. Without that distinction every subscription lands in Cut, because
    every vendor has a pricing page and Tavily will always find it."""
    moved = ("price cut", "price drop", "reduced price", "lowered", "price increase",
             "raises price", "now costs", "down from", "up from", "new pricing",
             "changed its pricing", "price change")
    for s in signals:
        blob = f"{s.get('title','')} {s.get('detail','')}".lower()
        if any(w in blob for w in moved):
            return True
    return False


def build_brief(company: dict, signals: list[dict], llm: LLMClient | None = None) -> dict:
    from . import settings as desk_settings
    cfg = desk_settings.get()

    llm = llm or LLMClient()
    open_invs = [i for i in company.get("invoices", []) if i.get("open")]
    invoice_number = open_invs[0]["number"] if open_invs else ""
    amount = f"${company['outstanding'] / 100:,.2f}"
    days = company.get("oldest_days") or 0
    company_name = cfg["company_name"]
    collecting = company["posture"] in ("collect", "cover")

    # The settings screen writes these, so an operator can widen or narrow the
    # agent's room without touching code.
    if collecting:
        may_agree = [m.replace("the window below", f"{cfg['payment_window_days']} days")
                      .replace("the limit below", str(cfg["max_instalments"]))
                     for m in cfg["may_agree"]]
    else:
        may_agree = ["Moving to current published pricing",
                     "Cancelling a duplicate plan"]

    opener = "this is an AI assistant calling" if cfg["disclose_ai"] else "calling"
    recording = " This call is recorded." if cfg["announce_recording"] else ""

    fallback = {
        "opening_line": (
            f"Hello, {opener} on behalf of {company_name} "
            f"about invoice {invoice_number}.{recording} It is {amount} and "
            f"now {days} days past due. Do you have two minutes?"
            if collecting else
            f"Hello, {opener} on behalf of {company_name} "
            f"about our {company['display_name']} subscription.{recording} "
            "I would like to review our current rate."),
        "context": [f"{amount} outstanding", f"{days} days past due"] if open_invs else
                   [f"${company['monthly_spend'] / 100:,.2f} a month"],
        "may_agree": may_agree,
        "must_not": list(cfg["must_not"]),
        "rationale": company.get("recommendation", ""),
    }

    signal_text = "\n".join(f"- [{s['severity']}] {s['title']}: {s['detail']}"
                            for s in signals) or "- none"
    payload = (f"Calling: {company['display_name']}\n"
               f"On behalf of: {company_name}\n"
               f"Tone: {cfg['tone']}\n"
               f"Posture: {company['posture']}\n"
               f"Outstanding: {amount} across {company['open_invoices']} invoices\n"
               f"Oldest: {days} days past due\n"
               f"Invoice number: {invoice_number}\n"
               f"Monthly spend with them: ${company['monthly_spend'] / 100:,.2f}\n"
               f"Signals:\n{signal_text}")

    brief = llm.json_call(BRIEF_SYSTEM, payload, fallback, max_tokens=1200)
    brief["invoice_number"] = invoice_number
    brief["needs_approval"] = company["outstanding"] >= cfg["approval_threshold_cents"]
    brief["voice_name"] = cfg["voice_name"]
    brief["tone"] = cfg["tone"]
    brief["do_not_call"] = company["id"] in (cfg["do_not_call"] or [])
    return brief


# --- demo overlay ----------------------------------------------------------

def demo_vendors() -> list[dict]:
    """Synthetic recurring vendors, because the Rho sandbox is too small for
    subscription detection to fire: its busiest real vendor has two charges.

    These rows carry demo=1 and the UI badges them, so nothing here can be
    mistaken for ledger data. Turn them off with DEMO_VENDORS=false.
    """
    seed = [
        {"name": "Asana", "domain": "asana.com", "sector": "Productivity",
         "aliases": ["ASANA.COM", "Asana Inc"], "monthly": 234000, "charges": 14},
        {"name": "Atlassian", "domain": "atlassian.com", "sector": "Productivity",
         "aliases": ["ATLASSIAN PTY", "ATLASSIAN*JIRA"], "monthly": 188000, "charges": 11},
        {"name": "Figma", "domain": "figma.com", "sector": "Design",
         "aliases": ["FIGMA MONTHLY", "FIGMA.COM"], "monthly": 99000, "charges": 9},
    ]
    out = []
    for s in seed:
        out.append({
            "id": slug(s["name"]), "display_name": s["name"],
            "aliases": s["aliases"], "domain": s["domain"], "sector": s["sector"],
            "resolution_note": "synthetic demo vendor, not from the Rho ledger",
            "money_in": 0, "money_out": s["monthly"] * s["charges"],
            "txn_count": s["charges"], "open_invoices": 0, "outstanding": 0,
            "oldest_days": None, "ar_share": 0.0,
            "recurring": 1, "monthly_spend": s["monthly"],
            "invoices": [], "contact_email": None, "demo": 1,
        })
    return out


# --- the whole run ---------------------------------------------------------

# The columns a counterparty row actually has. Hoisted out of run_desk so the
# storage step and the history snapshot agree on what a counterparty is.
COUNTERPARTY_COLUMNS = {
    "id", "display_name", "aliases", "domain", "sector", "resolution_note",
    "money_in", "money_out", "txn_count", "open_invoices", "outstanding",
    "oldest_days", "ar_share", "recurring", "monthly_spend", "duplicate",
    "posture", "recommendation", "rationale", "risk", "contact_name",
    "contact_phone", "contact_email", "invoices", "researched_at", "demo",
    "note", "note_source", "note_date", "note_url", "verdict", "verdict_reason",
}


def qualify(company: dict) -> dict:
    """Attach the research note and decide what, if anything, to do about this
    counterparty. The note is what a person reads to check the reasoning, so
    the verdict never stands on its own.

    Live research fills this in from Tavily. Seeded notes stand in where it
    has not run, which is what keeps the board legible without a key.
    """
    seed = research_seed.for_counterparty(company)
    if seed:
        company.update(note=seed["note"], note_source=seed["source"],
                       note_date=seed["date"], note_url=seed["url"],
                       verdict=seed["verdict"], verdict_reason=seed["reason"])
        return company

    owed = company.get("outstanding", 0)
    company.setdefault("note", "")
    company["verdict"] = "call" if owed and company.get("oldest_days") else "none"
    company["verdict_reason"] = ("Overdue with no adverse findings."
                                 if company["verdict"] == "call"
                                 else "Nothing outstanding and nothing recurring.")
    return company


def run_desk(progress=None) -> dict:
    """extract -> resolve -> monitor -> classify -> capture.

    Every run is recorded, snapshotted and diffed against the previous one.
    Nothing is wiped: the tables accumulate, and the current view is whatever
    carries the latest run id. That is what makes "what changed overnight"
    answerable instead of just "here is everything, again".
    """
    run_id = history.start_run()

    def say(stage: str, detail: str = "") -> None:
        db.log_run(stage, detail, run_id)
        if progress:
            progress(stage, detail)

    try:
        return _run_desk(run_id, say)
    except Exception as exc:  # noqa: BLE001 - a failed run must not look done
        history.finish_run(run_id, status="failed", note=str(exc)[:300])
        raise


def _run_desk(run_id: int, say) -> dict:
    llm, tavily = LLMClient(), TavilyClient()
    prev_run_id = history.previous_run(run_id)

    say("extract", "reading the Rho ledger")
    with rho_module.client() as rho:
        buckets = extract(rho)

    say("resolve", f"{len(buckets)} ledger names")
    companies = resolve(buckets, llm)

    if config.DEMO_VENDORS:
        companies += demo_vendors()
        say("resolve", f"added {len(demo_vendors())} labelled demo vendors")

    # Identity has to settle before anything is researched or stored, because
    # a counterparty id is a slug of its resolved name and the resolver is
    # allowed to change its mind. Without this, "Amazon Web Services" becoming
    # "Amazon.com, Inc." reads as one company leaving and another arriving,
    # and the new one arrives with no call history.
    degraded_stages = ["resolve"] if any(c.get("degraded") for c in companies) else []
    companies = history.carry_identity(companies, prev_run_id)
    renamed = [c for c in companies if c.get("renamed_from")]
    if renamed:
        say("resolve", f"{len(renamed)} counterparties kept their identity "
                       f"through a rename")

    total_ar = sum(c["outstanding"] for c in companies) or 1
    for company in companies:
        company["ar_share"] = round(company["outstanding"] / total_ar, 4)

    # The monitor stage is pure network: a few Tavily searches and one LLM call
    # per counterparty. Sequentially that is minutes; in a pool it is seconds.
    # Results are collected into a dict and applied in the original order, so
    # the output does not depend on which request finished first.
    found: dict[str, list[dict]] = {}
    workers = max(1, min(config.MONITOR_CONCURRENCY, len(companies) or 1))
    started = time.monotonic()
    say("monitor", f"researching {len(companies)} counterparties, {workers} at a time")

    with ThreadPoolExecutor(max_workers=workers) as pool:
        pending = {pool.submit(monitor, c, tavily, llm): c for c in companies}
        completed = 0
        for fut in as_completed(pending, timeout=config.MONITOR_TIMEOUT_SECONDS * 4):
            company = pending[fut]
            try:
                found[company["id"]] = fut.result(timeout=config.MONITOR_TIMEOUT_SECONDS)
            except Exception as exc:  # noqa: BLE001 - one bad lookup is not a failed run
                found[company["id"]] = []
                db.log_run("monitor-error", f"{company['display_name']}: {str(exc)[:160]}",
                           run_id)
            completed += 1
            if completed % 5 == 0 or completed == len(companies):
                say("monitor", f"{completed} of {len(companies)} researched "
                               f"({time.monotonic() - started:.0f}s)")

    # If most counterparties could not be researched, this run has no opinion
    # about the outside world, and the absence of signals is our outage rather
    # than quiet news.
    researched = sum(1 for c in companies if c.get("researched_ok"))
    if companies and researched < len(companies) / 2:
        degraded_stages.append("research")
        say("monitor", f"research degraded: only {researched} of {len(companies)} "
                       f"counterparties could be looked up")

    all_signals = []
    signal_counts: dict[str, int] = {}
    for company in companies:
        signals = found.get(company["id"], [])
        all_signals += signals
        signal_counts[company["id"]] = len(signals)
        classify(company, signals)
        qualify(company)
        company["researched_at"] = _now()
        company.setdefault("demo", 0)

    say("store", f"{len(companies)} companies, {len(all_signals)} signals")
    stamp = _now()

    # Signals are append-only. A story does not stop having happened because
    # this run's search did not surface it again, so nothing is deleted and
    # only first sightings count as new.
    known = {r["id"]: r for r in db.query("signals")}
    new_signals = []
    for sig in all_signals:
        prior = known.get(sig["id"])
        if prior and prior.get("first_seen_run"):
            sig["first_seen_run"] = prior["first_seen_run"]
            sig["first_seen_at"] = prior["first_seen_at"]
            sig["observed_at"] = prior.get("observed_at") or sig["observed_at"]
        else:
            sig["first_seen_run"] = run_id
            sig["first_seen_at"] = stamp
            new_signals.append(sig)
        sig["last_seen_run"] = run_id
        sig["last_seen_at"] = stamp

    known_cps = {r["id"]: r for r in db.query("counterparties")}
    rows = []
    for company in companies:
        prior = known_cps.get(company["id"]) or {}
        row = {k: v for k, v in company.items() if k in COUNTERPARTY_COLUMNS}
        row["first_seen_run"] = prior.get("first_seen_run") or run_id
        row["first_seen_at"] = prior.get("first_seen_at") or stamp
        row["last_seen_run"] = run_id
        rows.append(row)

    db.upsert("counterparties", rows)
    db.upsert("signals", all_signals)

    history.capture(run_id, companies, signal_counts)
    # Recorded before the diff, because the diff reads it back to decide
    # whether this run's counterparty set can be trusted.
    history.mark_degraded(run_id, degraded_stages)
    changes = history.diff(run_id, prev_run_id, new_signals)
    history.store(changes)
    history.finish_run(run_id, counterparties=len(companies),
                       signals=len(all_signals), new_signals=len(new_signals),
                       change_count=len(changes), degraded=bool(degraded_stages),
                       note=", ".join(degraded_stages))

    say("done", f"{len(changes)} changes since run {prev_run_id}" if prev_run_id
        else "first run, nothing to compare against yet")
    return {"run_id": run_id, "previous_run_id": prev_run_id,
            "degraded": degraded_stages,
            "companies": len(companies), "signals": len(all_signals),
            "new_signals": len(new_signals), "changes": len(changes),
            "llm_live": llm.live, "tavily_live": tavily.live}
