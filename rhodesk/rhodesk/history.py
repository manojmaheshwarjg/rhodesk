"""Run history and the run-over-run diff.

The desk used to be a snapshot generator: every run wiped the tables and wrote
a fresh picture, so "Northwind is 88 days overdue" read the same whether it had
just crossed 60 or had been sitting there for a month. Monitoring is about
deltas, so this module gives every run an identity, stores what each
counterparty looked like at that moment, and computes what moved.

Two rules shape the diff:

1. Counterparties can appear and disappear. A vendor with no transactions in
   the window is genuinely gone from the ledger, so both directions are
   reported.
2. Signals only ever appear. News does not un-happen, and a live search
   returns a slightly different set every time, so reporting "signal
   disappeared" would be reporting search noise. Signals are append-only and
   only the new ones are a change.
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any

from . import config, db

# How much a number has to move before it is worth telling someone about.
MATERIAL_CENTS = 25_000          # $250
MATERIAL_FRACTION = 0.10         # or 10% of the previous value
SPEND_FRACTION = 0.20            # subscriptions are noisier, so a wider band

AGING_BANDS = (90, 60, 30)

# Ordered worst first. The briefing sorts on this.
WEIGHTS = ("urgent", "attention", "info", "good")

SNAPSHOT_FIELDS = (
    "display_name", "domain", "posture", "risk", "outstanding", "open_invoices",
    "oldest_days", "monthly_spend", "money_in", "money_out", "txn_count",
    "ar_share", "recurring", "duplicate", "signal_count", "member_keys",
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _money(cents: int | None) -> str:
    return f"${(cents or 0) / 100:,.0f}"


def _band(days: int | None) -> int:
    for edge in AGING_BANDS:
        if (days or 0) >= edge:
            return edge
    return 0


# --- run records -----------------------------------------------------------

def start_run() -> int:
    db.execute(
        "INSERT INTO runs (started_at, status, mode) VALUES (?,?,?)",
        (_now(), "running", config.RHO_MODE),
    )
    return int(db.scalar("SELECT MAX(id) FROM runs") or 0)


def finish_run(run_id: int, *, status: str = "done", counterparties: int = 0,
               signals: int = 0, new_signals: int = 0, change_count: int = 0,
               degraded: bool = False, note: str = "") -> None:
    db.execute(
        "UPDATE runs SET finished_at=?, status=?, counterparties=?, signals=?, "
        "new_signals=?, change_count=?, degraded=?, note=? WHERE id=?",
        (_now(), status, counterparties, signals, new_signals, change_count,
         int(degraded), note, run_id),
    )


# Which stage failed decides what the diff can still be trusted to say.
# A resolver outage corrupts identity; a research outage corrupts everything
# derived from signals. The ledger arithmetic survives both.
SUPPRESSED_BY_STAGE = {
    "resolve": {"appeared", "disappeared", "merged"},
    "research": {"risk", "posture", "signal"},
}

STAGE_EXPLANATION = {
    "resolve": ("Entity resolution was unavailable",
                "Counterparties appearing and disappearing are suppressed for "
                "this comparison, because the grouping could not be trusted."),
    "research": ("Research was unavailable",
                 "Signal, risk and posture changes are suppressed for this "
                 "comparison. No news found is not the same as no news."),
}


def mark_degraded(run_id: int, stages: list[str] | None = None) -> None:
    """Recorded as soon as it is known, because the diff reads it back before
    the run is finished."""
    stages = sorted(set(stages or []))
    db.execute("UPDATE runs SET degraded=?, degraded_stages=? WHERE id=?",
               (int(bool(stages)), ",".join(stages), run_id))


def previous_run(run_id: int) -> int | None:
    return db.scalar(
        "SELECT MAX(id) FROM runs WHERE id < ? AND status = 'done'", (run_id,))


def latest_run() -> int | None:
    return db.scalar("SELECT MAX(id) FROM runs WHERE status = 'done'")


def runs(limit: int = 30) -> list[dict]:
    return db.rows(
        "SELECT * FROM runs WHERE status != 'running' ORDER BY id DESC LIMIT ?",
        (limit,))


# --- identity across runs --------------------------------------------------

def carry_identity(companies: list[dict], prev_run_id: int | None) -> list[dict]:
    """A counterparty's id is a slug of its resolved name, so a resolver that
    returns "Amazon Web Services" this run and "Amazon.com, Inc." the next
    would look like one company leaving and another arriving, taking its call
    history with it. Re-attach those to the id they already had, matching on
    domain first and then on a shared alias.

    Mutates and returns `companies`, adding `renamed_from` where it applies.
    """
    if not prev_run_id:
        return companies

    prior = db.rows(
        "SELECT counterparty_id, display_name, domain FROM counterparty_history "
        "WHERE run_id = ?", (prev_run_id,))
    if not prior:
        return companies

    current_ids = {c["id"] for c in companies}
    orphans = [p for p in prior if p["counterparty_id"] not in current_ids]
    if not orphans:
        return companies

    by_domain = {p["domain"].lower(): p for p in orphans
                 if (p.get("domain") or "").strip()}

    prior_ids = {p["counterparty_id"] for p in prior}
    claimed: set[str] = set()

    for company in companies:
        if company["id"] in prior_ids:
            continue
        domain = (company.get("domain") or "").strip().lower()
        match = by_domain.get(domain) if domain else None
        if not match:
            aliases = {a.lower() for a in (company.get("aliases") or [])}
            aliases.add(company["display_name"].lower())
            for candidate in orphans:
                if candidate["counterparty_id"] in claimed:
                    continue
                if (candidate["display_name"] or "").lower() in aliases:
                    match = candidate
                    break
        if match and match["counterparty_id"] not in claimed:
            claimed.add(match["counterparty_id"])
            company["renamed_from"] = match["display_name"]
            company["id"] = match["counterparty_id"]

    return companies


# --- snapshots -------------------------------------------------------------

def capture(run_id: int, companies: list[dict], signal_counts: dict[str, int]) -> None:
    """Write one history row per counterparty for this run."""
    if not companies:
        return
    cols = ("run_id", "counterparty_id", "captured_at", *SNAPSHOT_FIELDS)
    placeholders = ",".join("?" for _ in cols)
    now = _now()
    payload = []
    for c in companies:
        row = [run_id, c["id"], now]
        for field in SNAPSHOT_FIELDS:
            value = c.get(field)
            if field == "signal_count":
                value = signal_counts.get(c["id"], 0)
            if field == "member_keys":
                value = ",".join(c.get("member_key_ids") or [c["id"]])
            if isinstance(value, bool):
                value = int(value)
            row.append(value)
        payload.append(row)
    from .db import cursor
    with cursor() as conn:
        conn.executemany(
            f"INSERT OR REPLACE INTO {'counterparty_history'} ({','.join(cols)}) "
            f"VALUES ({placeholders})", payload)


def snapshot(run_id: int) -> dict[str, dict]:
    return {r["counterparty_id"]: r for r in db.rows(
        "SELECT * FROM counterparty_history WHERE run_id = ?", (run_id,))}


# --- the diff --------------------------------------------------------------

def _change(run_id: int, prev_run_id: int | None, kind: str, weight: str,
            cp: dict, headline: str, detail: str = "", *,
            from_value: Any = None, to_value: Any = None,
            amount: int | None = None, source_url: str = "",
            key: str = "") -> dict:
    cp_id = cp.get("counterparty_id") or cp.get("id") or ""
    seed = f"{run_id}|{kind}|{cp_id}|{key or headline}"
    return {
        "id": hashlib.sha1(seed.encode()).hexdigest()[:20],
        "run_id": run_id,
        "prev_run_id": prev_run_id,
        "at": _now(),
        "kind": kind,
        "weight": weight,
        "counterparty_id": cp_id,
        "display_name": cp.get("display_name") or cp_id,
        "headline": headline,
        "detail": detail,
        "from_value": None if from_value is None else str(from_value),
        "to_value": None if to_value is None else str(to_value),
        "amount": amount,
        "source_url": source_url,
    }


def _material(before: int | None, after: int | None) -> bool:
    before, after = before or 0, after or 0
    delta = abs(after - before)
    if delta < MATERIAL_CENTS:
        return False
    return before == 0 or delta / before >= MATERIAL_FRACTION


def degraded_stages(run_id: int | None) -> set[str]:
    if not run_id:
        return set()
    raw = db.scalar("SELECT degraded_stages FROM runs WHERE id = ?", (run_id,))
    return {s for s in (raw or "").split(",") if s}


def diff(run_id: int, prev_run_id: int | None,
         new_signals: list[dict] | None = None) -> list[dict]:
    """Compare two runs. `new_signals` are the signals this run saw for the
    first time, which the caller knows and the tables would not (a signal that
    reappears after a gap is not new)."""
    now_rows = snapshot(run_id)
    out: list[dict] = []

    if prev_run_id is None:
        # A first run has nothing to compare against. Saying "28 things
        # appeared" would be noise dressed as news.
        return out

    was_rows = snapshot(prev_run_id)

    # A change is only news if it came from the business rather than from one
    # of our own outages. Whatever was broken in EITHER run is untrustworthy
    # across the comparison, so both sides are pooled.
    broken = degraded_stages(run_id) | degraded_stages(prev_run_id)
    suppressed: set[str] = set()
    for stage in broken:
        suppressed |= SUPPRESSED_BY_STAGE.get(stage, set())
    trust_identity = "appeared" not in suppressed
    # the snapshot stores numbers, not prose, so the reasoning behind a
    # posture comes from the live row
    reasons = {r['id']: (r.get('rationale') or '')
               for r in db.query('counterparties')}

    for cp_id, now in now_rows.items():
        was = was_rows.get(cp_id)

        if was is None:
            if not trust_identity:
                continue
            owed = now["outstanding"] or 0
            out.append(_change(
                run_id, prev_run_id, "appeared",
                "attention" if owed else "info", now,
                f"New on the ledger",
                (f"First seen this run, owing {_money(owed)}." if owed
                 else "First seen this run."),
                amount=owed))
            continue

        # posture is the headline fact about a counterparty, so it leads
        if now["posture"] != was["posture"]:
            weight = "urgent" if now["posture"] == "cover" else (
                "good" if now["posture"] == "watch" else "attention")
            out.append(_change(
                run_id, prev_run_id, "posture", weight, now,
                f"{was['posture'].title()} to {now['posture'].title()}",
                reasons.get(cp_id, ""),
                from_value=was["posture"], to_value=now["posture"]))

        if now["risk"] != was["risk"] and now["risk"] not in ("", None):
            order = {"none": 0, "low": 1, "medium": 2, "high": 3}
            up = order.get(now["risk"], 0) > order.get(was["risk"] or "none", 0)
            out.append(_change(
                run_id, prev_run_id, "risk",
                "urgent" if up and now["risk"] == "high" else
                ("attention" if up else "good"), now,
                f"Risk {was['risk'] or 'none'} to {now['risk']}",
                from_value=was["risk"], to_value=now["risk"]))

        # receivables
        before, after = was["outstanding"] or 0, now["outstanding"] or 0
        if before and not after:
            out.append(_change(
                run_id, prev_run_id, "cleared", "good", now,
                f"Paid off {_money(before)}",
                "Nothing outstanding now.", from_value=before, to_value=0,
                amount=before))
        elif _material(before, after):
            rose = after > before
            out.append(_change(
                run_id, prev_run_id, "outstanding",
                "attention" if rose else "good", now,
                f"Owes {_money(after)}, {'up' if rose else 'down'} "
                f"{_money(abs(after - before))}",
                from_value=before, to_value=after, amount=after - before))

        # ageing is the thing a finance team actually watches
        band_was, band_now = _band(was["oldest_days"]), _band(now["oldest_days"])
        if band_now > band_was:
            out.append(_change(
                run_id, prev_run_id, "aging",
                "urgent" if band_now >= 90 else "attention", now,
                f"Past {band_now} days",
                (f"Their first overdue invoice, now {now['oldest_days'] or 0} days."
                 if not was["oldest_days"] else
                 f"Oldest invoice went from {was['oldest_days']} to "
                 f"{now['oldest_days'] or 0} days."),
                from_value=was["oldest_days"], to_value=now["oldest_days"],
                amount=now["outstanding"]))

        # spend
        if not was["duplicate"] and now["duplicate"]:
            out.append(_change(
                run_id, prev_run_id, "duplicate", "attention", now,
                "Duplicate subscription found",
                "Charged on more than one card.",
                amount=now["monthly_spend"]))

        spend_was, spend_now = was["monthly_spend"] or 0, now["monthly_spend"] or 0
        if (spend_was and spend_now > spend_was
                and (spend_now - spend_was) / spend_was >= SPEND_FRACTION
                and spend_now - spend_was >= 10_000):
            out.append(_change(
                run_id, prev_run_id, "spend", "attention", now,
                f"Monthly spend up to {_money(spend_now)}",
                f"Was {_money(spend_was)}.",
                from_value=spend_was, to_value=spend_now,
                amount=spend_now - spend_was))

    # A counterparty that was folded into another one this run did not leave
    # the ledger, it changed shape. The resolver regroups more often than
    # companies actually go away, so without this the briefing fills up with
    # phantom departures.
    absorbed: dict[str, dict] = {}
    for row in now_rows.values():
        for key in (row.get("member_keys") or "").split(","):
            if key and key != row["counterparty_id"]:
                absorbed[key] = row

    for cp_id, was in was_rows.items():
        if cp_id in now_rows or not trust_identity:
            continue
        into = absorbed.get(cp_id)
        if into:
            out.append(_change(
                run_id, prev_run_id, "merged", "info", was,
                f"Now grouped under {into['display_name']}",
                "Same spend, recognised as one counterparty rather than two.",
                to_value=into["counterparty_id"]))
            continue
        out.append(_change(
            run_id, prev_run_id, "disappeared", "info", was,
            "No longer on the ledger",
            "No transactions or open invoices in this window."))

    for sig in (new_signals or []):
        cp = now_rows.get(sig["counterparty_id"])
        if not cp:
            continue
        severity = (sig.get("severity") or "info").lower()
        weight = {"severe": "urgent", "warn": "attention",
                  "positive": "good"}.get(severity, "info")
        out.append(_change(
            run_id, prev_run_id, "signal", weight, cp,
            sig.get("title") or "New signal",
            sig.get("detail") or "",
            source_url=sig.get("source_url") or "",
            key=sig["id"]))

    if suppressed:
        out = [c for c in out if c["kind"] not in suppressed]
        for stage in sorted(broken):
            headline, detail = STAGE_EXPLANATION.get(
                stage, (f"{stage.title()} was unavailable",
                        "Some comparisons are suppressed for this run."))
            out.append(_change(run_id, prev_run_id, "degraded", "info",
                               {"counterparty_id": ""}, headline, detail,
                               key=stage))

    order = {w: i for i, w in enumerate(WEIGHTS)}
    out.sort(key=lambda c: (order.get(c["weight"], 9), -(c["amount"] or 0)))
    return out


def store(changes: list[dict]) -> None:
    if not changes:
        return
    cols = list(changes[0].keys())
    placeholders = ",".join("?" for _ in cols)
    from .db import cursor
    with cursor() as conn:
        conn.executemany(
            f"INSERT OR REPLACE INTO changes ({','.join(cols)}) VALUES ({placeholders})",
            [[c[k] for k in cols] for c in changes])


def changes_for(run_id: int | None = None) -> list[dict]:
    run_id = run_id or latest_run()
    if not run_id:
        return []
    order = "CASE weight " + " ".join(
        f"WHEN '{w}' THEN {i}" for i, w in enumerate(WEIGHTS)) + " ELSE 9 END"
    return db.rows(
        f"SELECT * FROM changes WHERE run_id = ? ORDER BY {order}, "
        f"COALESCE(amount, 0) DESC", (run_id,))


def timeline(counterparty_id: str) -> list[dict]:
    """Every snapshot of one counterparty, oldest first, for a sparkline or a
    detail panel."""
    return db.rows(
        "SELECT h.*, r.started_at, r.finished_at FROM counterparty_history h "
        "JOIN runs r ON r.id = h.run_id WHERE h.counterparty_id = ? "
        "ORDER BY h.run_id ASC", (counterparty_id,))


def current_run() -> int | None:
    """The run whose picture the app is currently showing. Read off the
    counterparties table rather than the runs table so the two can never
    disagree."""
    return db.scalar("SELECT MAX(last_seen_run) FROM counterparties")


def run(run_id: int) -> dict | None:
    found = db.rows("SELECT * FROM runs WHERE id = ?", (run_id,))
    return found[0] if found else None
