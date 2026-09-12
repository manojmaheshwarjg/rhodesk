"""The morning briefing.

"What changed" is the complete feed, sorted by weight. Today is the edit of
it: the few things that need a person, what the desk did on its own, and what
it intends to do next. If those are the same length, the edit has failed.

Everything here is derived. Nothing is stored, so the briefing can never drift
from the tables it describes.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from . import config, db, history, settings as desk_settings

WEEK = 7


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _parse(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        stamp = datetime.fromisoformat(value)
    except ValueError:
        return None
    return stamp if stamp.tzinfo else stamp.replace(tzinfo=timezone.utc)


def _greeting(now: datetime) -> str:
    hour = now.astimezone().hour
    if hour < 12:
        return "Good morning"
    return "Good afternoon" if hour < 18 else "Good evening"


# --- needs you -------------------------------------------------------------

def _needs_you(queue: dict, cfg: dict) -> list[dict]:
    """Only things a person has to decide. A long list here means the desk is
    handing back work rather than doing it, which is worth seeing."""
    out: list[dict] = []
    threshold = cfg["approval_threshold_cents"]

    for item in queue["items"]:
        if item["posture"] == "cover":
            out.append({
                "kind": "escalate", "weight": "urgent",
                "counterparty_id": item["id"],
                "title": f"{item['display_name']} needs escalating, not chasing",
                "detail": "Verified distress found. A standard collections call "
                          "is the wrong move here.",
                "amount": item["outstanding"], "action": "Review",
            })

    for item in queue["items"]:
        if item["posture"] != "cover" and item["outstanding"] >= threshold:
            out.append({
                "kind": "approval", "weight": "attention",
                "counterparty_id": item["id"],
                "title": f"{item['display_name']} call is above your threshold",
                "detail": "Approval needed before it dials.",
                "amount": item["outstanding"], "action": "Review",
            })

    # One row, not one per counterparty: with no contact enrichment this is
    # true of nearly everyone, and twelve identical rows is not a briefing.
    unreachable = [i for i in queue["items"] if not i.get("contact_phone")]
    if unreachable:
        emailable = sum(1 for i in unreachable if i.get("contact_email"))
        out.append({
            "kind": "unreachable", "weight": "attention",
            "counterparty_id": unreachable[0]["id"],
            "title": f"{len(unreachable)} in the queue have no phone number",
            "detail": (f"{emailable} have an email address on file. The rest have "
                       "no way to reach them at all."
                       if emailable else
                       "No way to reach any of them without contact enrichment."),
            "amount": sum(i["outstanding"] for i in unreachable), "action": None,
        })

    return out


def _degraded(status_services: dict) -> list[dict]:
    """A service that quietly stopped working is a thing a person needs to
    know, because every number below it is then wrong."""
    out = []
    for name, label in (("tavily", "Research"), ("llm", "The model"),
                        ("voice", "Calling")):
        service = status_services.get(name) or {}
        if service.get("last_error"):
            out.append({
                "kind": "degraded", "weight": "urgent", "counterparty_id": None,
                "title": f"{label} is failing",
                "detail": str(service["last_error"])[:200],
                "amount": None, "action": None,
            })
    return out


# --- handled ---------------------------------------------------------------

def _headline(name: str, headline: str) -> str:
    """Signal headlines are news titles, which usually open with the company
    name. Prefixing the name again gives "Summit Analytics · Summit Analytics
    raises a round", so the duplicate is trimmed."""
    lead = headline.strip()
    if lead.lower().startswith(name.lower()):
        trimmed = lead[len(name):].lstrip(" ,:-")
        if trimmed:
            lead = trimmed[0].upper() + trimmed[1:]
    return f"{name} · {lead}"


def _handled(now: datetime, since: datetime) -> list[dict]:
    """What the desk did without being asked. Calls first, because those are
    the actions; changes after, because those are observations."""
    out: list[dict] = []
    names = {c["id"]: c["display_name"] for c in db.query("counterparties")}

    for call in db.query("calls", "state = ?", ("done",), "created_at DESC"):
        at = _parse(call.get("ended_at") or call.get("created_at"))
        if not at or at < since:
            continue
        outcome = call.get("outcome") or {}
        summary = outcome.get("summary") or "Call completed."
        out.append({
            "kind": "call", "at": at.isoformat(),
            "counterparty_id": call["counterparty_id"],
            "title": f"{names.get(call['counterparty_id'], call['counterparty_id'])}"
                     f" · {outcome.get('result') or 'called'}",
            "detail": summary[:220],
            "simulated": bool(call.get("simulated")),
        })

    run_id = history.current_run()
    for change in history.changes_for(run_id):
        if change["weight"] == "info":
            continue                      # the feed has these; a briefing does not
        at = _parse(change.get("at"))
        if not at or at < since:
            continue
        out.append({
            "kind": "change", "at": at.isoformat(),
            "counterparty_id": change.get("counterparty_id"),
            "title": _headline(change["display_name"], change["headline"]),
            "detail": (change.get("detail") or "")[:220],
            "weight": change["weight"],
        })

    out.sort(key=lambda row: row["at"], reverse=True)
    return out


# --- this week -------------------------------------------------------------

def _week(now: datetime) -> dict:
    since = (now - timedelta(days=WEEK)).isoformat()
    recovered = db.scalar(
        "SELECT COALESCE(SUM(amount), 0) FROM changes WHERE kind='cleared' AND at >= ?",
        (since,)) or 0
    duplicates = db.scalar(
        "SELECT COALESCE(SUM(amount), 0) FROM changes WHERE kind='duplicate' AND at >= ?",
        (since,)) or 0

    calls = [c for c in db.query("calls") if (_parse(c.get("created_at")) or now)
             >= now - timedelta(days=WEEK)]
    answered = sum(1 for c in calls
                   if (c.get("outcome") or {}).get("result") not in (None, "", "none"))
    return {
        "recovered": recovered,
        "duplicate_spend": duplicates,
        "calls": len(calls),
        "answered": answered,
        "real_calls": sum(1 for c in calls if not c.get("simulated")),
    }


# --- assembly --------------------------------------------------------------

def brief(status_services: dict | None = None) -> dict:
    from .api import queue as build_queue   # lazy: api imports this module

    now = _now()
    cfg = desk_settings.get()
    queue = build_queue()
    run_id = history.current_run()
    run = history.run(run_id) if run_id else None
    finished = _parse((run or {}).get("finished_at"))

    # Everything since the previous run is "overnight". Before there is a
    # previous run, fall back to a day so the screen is not empty on day one.
    previous = history.previous_run(run_id) if run_id else None
    since = _parse((history.run(previous) or {}).get("finished_at")) if previous else None
    since = since or (now - timedelta(days=1))

    needs = _degraded(status_services or {}) + _needs_you(queue, cfg)
    handled = _handled(now, since)

    if not run:
        headline = "The desk has not run yet. Run it to take a first reading."
    elif not needs:
        headline = (f"The desk ran {_ago(finished, now)}. Nothing needs you, "
                    f"{len(handled)} things handled.")
    else:
        count = len(needs)
        headline = (f"The desk ran {_ago(finished, now)}. "
                    f"{count} thing{'s' if count != 1 else ''} need"
                    f"{'' if count != 1 else 's'} you, the rest is handled.")

    return {
        "greeting": _greeting(now),
        "company": cfg["company_name"],
        "headline": headline,
        "run": run,
        "comparable": bool(previous),
        "needs_you": needs,
        "handled": handled,
        "week": _week(now),
        "queued": queue["items"][:6],
        "queue_total": len(queue["items"]),
    }


def _ago(stamp: datetime | None, now: datetime) -> str:
    if not stamp:
        return "recently"
    seconds = (now - stamp).total_seconds()
    if seconds < 120:
        return "just now"
    if seconds < 5400:
        return f"{round(seconds / 60)} minutes ago"
    if seconds < 172800:
        return f"{round(seconds / 3600)} hours ago"
    return f"{round(seconds / 86400)} days ago"
