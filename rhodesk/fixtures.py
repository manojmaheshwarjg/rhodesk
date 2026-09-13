"""A generated ledger that looks like a real business.

Why this exists: the public Rho sandbox holds 72 transactions over a short
window, and its busiest vendor has two charges. That is enough to prove the
API client works and not enough for the product to be interesting, because
subscription detection never fires and entity resolution has nothing to merge.

This module generates eighteen months of activity for a Series B company:
recurring vendors billed under messy aliases, one genuinely duplicated
subscription, and receivables spread across the age bands so Collect, Cover
and Cut all have real work.

Two properties matter:

  Deterministic. Everything comes from a seeded RNG, so the same run produces
  the same ledger and your demo does not change under you.

  Anchored to today. Dates are computed backwards from date.today(), so the
  overdue counts are always right no matter when you run it. A fixture set
  with hardcoded dates rots within a week.

Shapes match the live API exactly, field for field, so `FixtureClient` is a
drop-in for `RhoClient`.
"""
from __future__ import annotations

import random
from datetime import date, datetime, timedelta, timezone

SEED = 20260912
CURRENCY = "USD"

# --- the cast ---------------------------------------------------------------

# Real companies, so that a live Tavily key returns real research about them.
# `aliases` is what the ledger actually writes, which is the whole point of the
# resolve step.
VENDORS = [
    {"name": "Amazon Web Services", "monthly": 4_820_00, "drift": 0.08, "months": 18,
     "aliases": ["AWS EMEA", "AMZN AWS", "AMAZON WEB SVCS"], "category": "Cloud"},
    {"name": "Datadog", "monthly": 1_940_00, "drift": 0.05, "months": 16,
     "aliases": ["DATADOG INC", "DDOG*MONITORING"], "category": "Observability"},
    {"name": "Atlassian", "monthly": 1_880_00, "drift": 0.0, "months": 18,
     "aliases": ["ATLASSIAN PTY", "ATLASSIAN*JIRA"], "category": "Productivity"},
    {"name": "Figma", "monthly": 990_00, "drift": 0.02, "months": 14,
     "aliases": ["FIGMA MONTHLY", "FIGMA.COM"], "category": "Design"},
    {"name": "Vercel", "monthly": 640_00, "drift": 0.06, "months": 15,
     "aliases": ["VERCEL INC", "VERCEL*HOSTING"], "category": "Hosting"},
    {"name": "GitHub", "monthly": 520_00, "drift": 0.03, "months": 18,
     "aliases": ["GITHUB.COM", "MSFT*GITHUB"], "category": "Developer tools"},
    {"name": "Notion", "monthly": 360_00, "drift": 0.01, "months": 13,
     "aliases": ["NOTION LABS", "NOTION.SO"], "category": "Productivity"},
    {"name": "Linear", "monthly": 280_00, "drift": 0.02, "months": 12,
     "aliases": ["LINEAR.APP"], "category": "Productivity"},
    {"name": "Deel", "monthly": 62_400_00, "drift": 0.04, "months": 18,
     "aliases": ["DEEL INC", "DEEL PAYROLL"], "category": "Payroll"},
    {"name": "Crescent Property Group", "monthly": 18_500_00, "drift": 0.0, "months": 18,
     "aliases": ["CRESCENT PROPERTY GRP", "CRESCENT PPTY"], "category": "Rent"},
]

# The duplicate. Two live Asana subscriptions on two cards under two
# departments, which is the single clearest Cut finding a real company has.
DUPLICATE = {
    "name": "Asana", "category": "Productivity",
    "legs": [
        {"alias": "ASANA.COM", "monthly": 1_170_00, "months": 18, "card": 0},
        {"alias": "ASANA INC", "monthly": 1_170_00, "months": 11, "card": 3},
    ],
}

# Irregular spend, so the ledger is not wall-to-wall subscriptions.
ONE_OFFS = [
    ("Midtown Parking Services", 40_00, 120_00, "Travel"),
    ("Graceway Car Service", 60_00, 240_00, "Travel"),
    ("Northstar Office Supply", 80_00, 900_00, "Office"),
    ("Canal House Bistro", 90_00, 480_00, "Meals"),
    ("Meridian Travel Inc.", 400_00, 3_200_00, "Travel"),
    ("Summit Legal LLP", 2_500_00, 14_000_00, "Legal"),
]

# Receivables. Fictional, because a real company cannot owe a fictional one
# money. `overdue` is days past due relative to today, so the spread is stable.
CUSTOMERS = [
    {"name": "Northwind Traders", "domain": "northwind.example",
     "invoices": [(94, 47_200_00, "unpaid"), (12, 12_000_00, "unpaid"),
                  (-210, 31_000_00, "paid")]},
    {"name": "Summit Analytics", "domain": "summitanalytics.example",
     "invoices": [(71, 28_400_00, "unpaid"), (-120, 19_500_00, "paid")]},
    {"name": "Orbit Media Group", "domain": "orbitmedia.example",
     "invoices": [(46, 31_850_00, "unpaid"), (-90, 22_000_00, "paid")]},
    {"name": "Brightleaf Design", "domain": "brightleaf.example",
     "invoices": [(38, 9_400_00, "unpaid")]},
    {"name": "Harbor Logistics", "domain": "harborlogistics.example",
     "invoices": [(21, 7_450_00, "unpaid"), (-60, 11_200_00, "paid")]},
    {"name": "Cedar & Co", "domain": "cedarandco.example",
     "invoices": [(8, 5_600_00, "unpaid")]},
    {"name": "Wellstone Media", "domain": "wellstone.example",
     "invoices": [(-14, 18_900_00, "unpaid"), (-140, 16_000_00, "paid")]},
    {"name": "Foundry Works", "domain": "foundryworks.example",
     "invoices": [(-30, 24_000_00, "unpaid"), (-175, 20_500_00, "paid")]},
    {"name": "Teamline Software", "domain": "teamline.example",
     "invoices": [(-260, 42_000_00, "paid")]},
    {"name": "Civic Affairs Inc.", "domain": "civicaffairs.example",
     "invoices": [(-300, 59_000_00, "paid")]},
]

PEOPLE = [("Ethan", "Parker"), ("Maya", "Chen"), ("Lucas", "Bennett"),
          ("Priya", "Raman"), ("Noah", "Gill"), ("Zara", "Okafor")]


# Invoice references are one letter and three digits with no separator: R204.
# An INV-2026-0001 style reference spends three syllables and a year before
# the part anyone needs, and every dash is something a voice agent is tempted
# to read out. R because it sits in none of the letter groups that blur
# together on a narrowband phone line (B D E P T V, A J K, F S, M N).
INVOICE_PREFIX = "R"
INVOICE_BASE = 200


def invoice_ref(seq: int) -> str:
    """R201 for the first invoice. Offset so every reference has three digits
    and no leading zero, which reads as a number rather than a code."""
    return f"{INVOICE_PREFIX}{INVOICE_BASE + seq}"


def _uuid(prefix: int, n: int) -> str:
    return f"{prefix:08x}-0000-4000-8000-{n:012d}"


def _iso(d: date, rng: random.Random) -> str:
    return datetime(d.year, d.month, d.day,
                    rng.randrange(8, 20), rng.randrange(0, 60),
                    rng.randrange(0, 60), tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def _months_back(anchor: date, n: int) -> date:
    y, m = anchor.year, anchor.month - n
    while m <= 0:
        m += 12
        y -= 1
    day = min(anchor.day, 28)
    return date(y, m, day)


def generate(seed: int = SEED) -> dict:
    """`as_of` reads THIS ledger as it stood on an earlier date.

    The history layer needs two runs that genuinely differ before it has
    anything to compare, and waiting a day for one is not a demo. So the
    ledger is generated once, anchored to today as always, and then rewound:
    transactions that had not posted yet are removed, and invoices that were
    paid since are put back to unpaid. Nothing is invented. It is the same
    ledger, read at an earlier moment.
    """
    rng = random.Random(seed)
    today = date.today()

    # --- accounts ----------------------------------------------------------
    accounts = [
        {"id": _uuid(0x30000000, 1), "account_name": "Operating", "account_type": "checking",
         "account_number_last_4": "9508", "routing_number_last_4": "0089",
         "balance": {"amount": 1_284_600_00, "currency": CURRENCY}},
        {"id": _uuid(0x30000000, 2), "account_name": "Payroll", "account_type": "checking",
         "account_number_last_4": "4609", "routing_number_last_4": "0089",
         "balance": {"amount": 186_400_00, "currency": CURRENCY}},
        {"id": _uuid(0x30000000, 3), "account_name": "Savings", "account_type": "savings",
         "account_number_last_4": "2112", "routing_number_last_4": "0089",
         "balance": {"amount": 2_400_000_00, "currency": CURRENCY}},
        {"id": _uuid(0x30000000, 4), "account_name": "Treasury", "account_type": "investment",
         "balance": {"amount": 5_180_000_00, "currency": CURRENCY}},
        {"id": _uuid(0x30000000, 5), "account_name": "Credit Account", "account_type": "credit",
         "balance": {"amount": -142_800_00, "currency": CURRENCY}},
        {"id": _uuid(0x30000000, 6), "account_name": "Rewards", "account_type": "rewards",
         "balance": {"amount": 8_940_00, "currency": CURRENCY}},
    ]
    checking, credit = accounts[0], accounts[4]

    # --- cards -------------------------------------------------------------
    cards = []
    for i, (first, last) in enumerate(PEOPLE):
        cards.append({
            "id": _uuid(0x20000000, i + 1),
            "name": f"{first} {last}",
            "last_4": f"{rng.randrange(1000, 9999)}",
            "cardholder": {"first_name": first, "last_name": last,
                           "user_id": _uuid(0x10000000, i + 1)},
            "status": "active",
            "spending_limit": {"amount": 10_000_00, "currency": CURRENCY},
            "spending_limit_type": "monthly",
            "current_spend": {"amount": rng.randrange(200_00, 8_000_00), "currency": CURRENCY},
            "pending_spend": {"amount": rng.randrange(0, 900_00), "currency": CURRENCY},
            "billing_address": {"street": "100 Crosby Street", "second_line": "Floor 5",
                                "city": "New York", "subdivision": "NY",
                                "postal_code": "10012", "country_code": "US"},
            "shipping_address": None,
        })

    txns: list[dict] = []
    seq = 0

    def add(counterparty: str, cents: int, when: date, ttype: str,
            account: dict, card: dict | None = None) -> None:
        nonlocal seq
        seq += 1
        settled = when + timedelta(days=rng.randrange(0, 3))
        txns.append({
            "id": _uuid(0x019f0000, seq),
            "money_movement_id": _uuid(0x40000000, seq),
            "account_id": account["id"], "account_name": account["account_name"],
            "account_type": account["account_type"],
            "amount": {"amount": cents, "currency": CURRENCY},
            "counterparty_name": counterparty,
            "initiated_at": _iso(when, rng),
            "posted_at": _iso(min(settled, today), rng),
            "status": "settled" if settled <= today else "pending",
            "transaction_type": ttype,
            "card_id": card["id"] if card else None,
            "card_name": card["name"] if card else None,
            "user_id": card["cardholder"]["user_id"] if card else None,
            "user_full_name": card["name"] if card else None,
            "attachments": [],
        })

    # --- recurring vendors, billed under rotating aliases -------------------
    for v in VENDORS:
        card = cards[rng.randrange(len(cards))]
        big = v["monthly"] > 10_000_00          # payroll and rent leave the bank
        for m in range(v["months"], 0, -1):
            when = _months_back(today, m)
            amount = int(v["monthly"] * (1 + v["drift"] * (v["months"] - m) / 12))
            amount = int(amount * rng.uniform(0.98, 1.02))
            alias = v["aliases"][rng.randrange(len(v["aliases"]))]
            if big:
                add(alias, -amount, when, "ach_debit", checking)
            else:
                add(alias, -amount, when, "card_debit", credit, card)

    # --- the duplicate subscription ----------------------------------------
    for leg in DUPLICATE["legs"]:
        card = cards[leg["card"]]
        for m in range(leg["months"], 0, -1):
            when = _months_back(today, m)
            add(leg["alias"], -int(leg["monthly"] * rng.uniform(0.99, 1.01)),
                when, "card_debit", credit, card)

    # --- irregular spend ---------------------------------------------------
    for name, lo, hi, _cat in ONE_OFFS:
        for _ in range(rng.randrange(6, 20)):
            when = today - timedelta(days=rng.randrange(1, 540))
            add(name, -rng.randrange(lo, hi), when, "card_debit",
                credit, cards[rng.randrange(len(cards))])

    # --- customers and invoices -------------------------------------------
    customers, invoices = [], []
    inv_seq = 0
    for ci, c in enumerate(CUSTOMERS, 1):
        cid = _uuid(0x60000000, ci)
        slug = c["name"].lower().replace(" ", "").replace("&", "and").replace(".", "")
        received = 0
        last_invoice_id = None
        for overdue_days, cents, status in c["invoices"]:
            inv_seq += 1
            iid = _uuid(0x70000000, inv_seq)
            last_invoice_id = iid
            due = today - timedelta(days=overdue_days)
            issued = due - timedelta(days=30)
            payments, activities = [], [
                {"activity_type": "created", "created_at": _iso(issued, rng),
                 "emails": [], "user_id": _uuid(0x40000000, 1)},
                {"activity_type": "sent", "created_at": _iso(issued, rng),
                 "emails": [f"accounts@{c['domain']}"], "user_id": _uuid(0x40000000, 1)},
            ]
            if status == "paid":
                paid_on = due - timedelta(days=rng.randrange(0, 12))
                received += cents
                payments.append({"type": "received_in_account", "external_method": None,
                                 "paid_at": paid_on.isoformat(), "transaction_id": None})
                activities.append({"activity_type": "marked_as_paid",
                                   "created_at": _iso(paid_on, rng), "emails": [],
                                   "user_id": None})
                # Money in also shows up on the ledger.
                add(c["name"], cents, paid_on, "ach_credit", checking)
            elif overdue_days > 30:
                activities.append({"activity_type": "reminder_sent",
                                   "created_at": _iso(due + timedelta(days=14), rng),
                                   "emails": [f"accounts@{c['domain']}"], "user_id": None})

            invoices.append({
                "id": iid, "invoice_number": invoice_ref(inv_seq),
                "customer": {"id": cid},
                "date": issued.isoformat(), "due_date": due.isoformat(),
                "status": status, "total": {"amount": cents, "currency": CURRENCY},
                "discount_rate": 0, "tax_rate": 0,
                "line_items": [{"name": "Professional services", "quantity": 1,
                                "total": {"amount": cents, "currency": CURRENCY},
                                "discount_rate": 0, "tax_rate": None}],
                "payments": payments, "activities": activities,
                "note": None, "file_id": _uuid(0x50000000, inv_seq),
                "accounting_sync_status": "synced" if status == "paid" else "not_pushed",
                "accounting_synced_at": _iso(issued, rng) if status == "paid" else None,
                "created_at": _iso(issued, rng), "updated_at": _iso(due, rng),
            })

        customers.append({
            "id": cid, "legal_name": c["name"],
            "email": f"accounts@{c['domain']}",
            "cc_emails": [f"billing@{c['domain']}"],
            "address": {"address1": "77 Broadway", "address2": "", "city": "Boston",
                        "state": "MA", "zip_code": "02109", "country": "USA"},
            "note": None, "deleted_at": None, "last_invoice_id": last_invoice_id,
            "total_revenue": {"amount": received, "currency": CURRENCY},
            "created_at": _iso(today - timedelta(days=600), rng),
            "updated_at": _iso(today - timedelta(days=rng.randrange(1, 60)), rng),
        })

    txns.sort(key=lambda t: t["initiated_at"], reverse=True)
    return {"accounts": accounts, "cards": cards, "transactions": txns,
            "customers": customers, "invoices": invoices}


def _rewind(data: dict, as_of: date) -> dict:
    """Undo everything that happened after `as_of`. Used only to give the
    history layer two readings to compare."""
    cutoff = as_of.isoformat()

    data["transactions"] = [t for t in data["transactions"]
                            if (t.get("initiated_at") or "")[:10] <= cutoff]

    invoices = []
    for inv in data["invoices"]:
        if (inv.get("created_at") or "")[:10] > cutoff:
            continue                          # not raised yet
        inv = dict(inv)
        paid_after = any((p.get("paid_at") or "")[:10] > cutoff
                         for p in inv.get("payments") or [])
        if paid_after:
            inv["payments"] = []
            inv["status"] = "unpaid"
            inv["accounting_sync_status"] = "not_pushed"
            inv["accounting_synced_at"] = None
            inv["activities"] = [a for a in inv.get("activities") or []
                                 if a.get("activity_type") != "marked_as_paid"]
        inv["activities"] = [a for a in inv.get("activities") or []
                             if (a.get("created_at") or "")[:10] <= cutoff]
        invoices.append(inv)
    data["invoices"] = invoices
    return data


class FixtureClient:
    """Drop-in for RhoClient, serving the generated ledger."""

    def __init__(self, seed: int = SEED, as_of: date | None = None):
        self.base_url = "fixtures://generated"
        if as_of:
            self.base_url += f"?as_of={as_of.isoformat()}"
        self._data = generate(seed)
        if as_of and as_of < date.today():
            self._data = _rewind(self._data, as_of)

    def close(self) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        pass

    def accounts(self) -> list[dict]:
        return self._data["accounts"]

    def cards(self) -> list[dict]:
        return self._data["cards"]

    def transactions(self) -> list[dict]:
        return self._data["transactions"]

    def customers(self) -> list[dict]:
        return self._data["customers"]

    def invoices(self) -> list[dict]:
        return self._data["invoices"]

    def all(self, path: str, params: dict | None = None) -> list[dict]:
        key = path.rstrip("/").split("/")[-1]
        return self._data.get("customers" if key == "customers" else key, [])

    def ping(self) -> dict:
        accs = self.accounts()
        return {"ok": True, "accounts": len(accs), "base_url": self.base_url,
                "fixtures": True,
                "total_balance_cents": sum(a["balance"]["amount"] for a in accs)}
