"""A counterparty's calls, newest first: the Timeline modal on the board, and
the history Rhonica is given before she dials.

Both read from here, so what the operator sees under Timeline is exactly what
the agent works from. It is also why a follow-up two hours after the last call
can open differently from a first one. The opener is decided here, in code,
because an ElevenLabs first message is fixed text and cannot branch.
"""
from __future__ import annotations

from calendar import monthrange
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from . import config, db

# Under this, the person still remembers the last call, so Rhonica checks the
# moment is still good rather than asking afresh.
RECENT_SECONDS = 6 * 3600

# How many earlier calls go into the agent's context. Older ones add length,
# not judgement.
HISTORY_LIMIT = 5


def is_rehearsal(call: dict) -> bool:
    """A browser session is the operator talking to the agent themselves, to
    hear how it sounds before it dials anyone. Nobody was contacted, so it is
    never an outcome on the board, a row in the call log, a figure in the
    stats, or a line in a counterparty's history. Only calls that reached a
    number count."""
    return (call.get("to_number") or "") == "browser"


def for_counterparty(cp_id: str) -> list[dict]:
    """Every real call to this counterparty, newest first."""
    rows = db.query("calls", "counterparty_id = ?", (cp_id,), "created_at DESC")
    return [_entry(r) for r in rows if not is_rehearsal(r)]


def agent_context(cp: dict, now: datetime | None = None) -> dict[str, str]:
    """What Rhonica is told about earlier calls, as dynamic variables: the
    current time, the real dates behind phrases like "early next week", the
    history, and the line she opens with."""
    now = now or datetime.now(ZoneInfo(config.TIMEZONE))
    done = [c for c in for_counterparty(cp["id"]) if c["state"] == "done"]

    lines = []
    for c in done[:HISTORY_LIMIT]:
        at = _parse(c["at"]).astimezone(now.tzinfo)
        head = [f"{_written(at)} ({say_ago(at, now)})",
                "answered" if _answered(c) else "not answered"]
        if c["duration_secs"]:
            head.append(f"lasted {c['duration_secs'] // 60}:{c['duration_secs'] % 60:02d}")
        line = "- " + ", ".join(head) + ": " + (c["summary"] or "nothing was recorded.")
        agreed = "; ".join(f"{_label(x['label'])}: {x['value']}" for x in c["commitments"])
        lines.append(line + (f" Agreed: {agreed}." if agreed else ""))

    spoke = next((c for c in done if _answered(c)), None)
    return {
        "now": _written(now, year=True),
        "calendar": _calendar(now),
        "call_history": "\n".join(lines) or "No earlier calls. This is the first time you are calling them.",
        "opener": opener(cp.get("contact_name"), config.COMPANY_NAME, spoke,
                         done[0] if done else None, now),
    }


def opener(contact_name: str | None, company: str, spoke: dict | None,
           tried: dict | None, now: datetime) -> str:
    """The first thing Rhonica says: a normal call from the accounts team. It
    names the company and says the call is being recorded. It does not lead
    with being an AI; the prompt has her say so plainly if anyone asks. "We
    spoke" is only said when someone actually answered."""
    name = contact_name or "there"
    recorded = "and I should mention this call is being recorded"
    if spoke:
        at = _parse(spoke["at"])
        still = (now - at).total_seconds() < RECENT_SECONDS
        return (f"Hey {name}, it's Rhonica again from the {company} accounts team. "
                f"We spoke {say_ago(at, now)}, {recorded} too. "
                + ("Is now still a good time for a quick chat?" if still
                   else "Is now a good time for a quick chat?"))
    if tried:
        return (f"Hey {name}, it's Rhonica from the accounts team at {company}. "
                f"I tried you {say_ago(_parse(tried['at']), now)}, {recorded}. "
                "Is now a good time for a quick chat?")
    return (f"Hey {name}, it's Rhonica from the accounts team at {company}, "
            f"{recorded}. Is now a good time for a quick chat?")


def say_ago(then: datetime, now: datetime) -> str:
    """How long ago, the way a person says it on the phone."""
    from .voice import say_number     # voice imports this module, so import late

    mins = max(0.0, (now - then).total_seconds()) / 60
    if mins < 10:
        return "a few minutes ago"
    if mins < 55:
        return f"about {say_number(round(mins / 5) * 5)} minutes ago"
    if mins < 6 * 60:
        hours = max(1, round(mins / 60))
        return "about an hour ago" if hours == 1 else f"about {say_number(hours)} hours ago"

    then = then.astimezone(now.tzinfo)
    days = (now.date() - then.date()).days
    part = _part_of_day(then)
    if days == 0:
        if part == "night":
            return "last night"
        return f"earlier this {part}" if part == _part_of_day(now) else f"this {part}"
    if days == 1:
        return "yesterday" if part == "night" else f"yesterday {part}"
    if days < 7:
        return f"on {then:%A}"
    if days < 14:
        return "last week"
    if days < 28:
        return "a couple of weeks ago"
    return "about a month ago" if days < 45 else "a while ago"


# --- helpers ----------------------------------------------------------------

def _entry(call: dict) -> dict:
    oc = call.get("outcome") or {}
    commitments = oc.get("commitments") or []
    if isinstance(commitments, dict):          # the webhook path stores a mapping
        commitments = [{"label": k, "value": v} for k, v in commitments.items()]
    return {
        "id": call["id"],
        "at": call.get("created_at"),
        "ended_at": call.get("ended_at"),
        "state": call.get("state"),
        "duration_secs": _duration(call.get("created_at"), call.get("ended_at")),
        "result": oc.get("result") or "",
        "summary": oc.get("summary") or "",
        "answered": oc.get("answered"),
        "commitments": [x for x in commitments if isinstance(x, dict) and x.get("label")],
    }


def _answered(c: dict) -> bool:
    """Older outcomes did not record this. A call with a summary that did not
    end in voicemail is taken as answered."""
    if c["answered"] is not None:
        return bool(c["answered"])
    return bool(c["summary"]) and c["result"] != "voicemail"


def _duration(start: str | None, end: str | None) -> int | None:
    if not (start and end):
        return None
    return max(0, int((_parse(end) - _parse(start)).total_seconds()))


def _parse(iso: str) -> datetime:
    t = datetime.fromisoformat(iso)
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def _part_of_day(t: datetime) -> str:
    if t.hour < 5:
        return "night"
    if t.hour < 12:
        return "morning"
    return "afternoon" if t.hour < 17 else "evening"


def _written(t: datetime, year: bool = False) -> str:
    """"Sunday 13 September, 2:06 AM EDT": for the agent to reason with, not to say."""
    day = f"{t:%A} {t.day} {t:%B}" + (f" {t.year}" if year else "")
    hour = t.hour % 12 or 12
    return f"{day}, {hour}:{t:%M} {'AM' if t.hour < 12 else 'PM'} {t:%Z}".strip()


def _label(key: str) -> str:
    return str(key).replace("_", " ").replace("-", " ").capitalize()


# --- dates people say out loud ------------------------------------------------
# Models get calendar arithmetic wrong mid-call, and a suggested date is only
# useful if it is the right one. So the days behind the phrases people use are
# worked out here, before she dials, and she proposes from these.

_ORDINALS = ["zeroth", "first", "second", "third", "fourth", "fifth", "sixth", "seventh",
             "eighth", "ninth", "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth",
             "fifteenth", "sixteenth", "seventeenth", "eighteenth", "nineteenth"]


def say_ordinal(n: int) -> str:
    """14 is "fourteenth", 21 is "twenty first", 30 is "thirtieth"."""
    if n < 20:
        return _ORDINALS[n]
    tens, ones = divmod(n, 10)
    word = {2: "twenty", 3: "thirty"}[tens]
    return f"{word} {_ORDINALS[ones]}" if ones else f"{word[:-1]}ieth"


def _spoken_day(d: date, today: date | None = None) -> str:
    """"Monday the fourteenth", naming the month only when it is not this one."""
    said = f"{d:%A} the {say_ordinal(d.day)}"
    if today and (d.year, d.month) == (today.year, today.month):
        return said
    return f"{said} of {d:%B}"


def _weekdays(first: date, last: date) -> list[date]:
    span = (first + timedelta(days=i) for i in range((last - first).days + 1))
    return [d for d in span if d.weekday() < 5]


def _first_weekday(year: int, month: int) -> date:
    d = date(year, month, 1)
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


def _last_weekday(year: int, month: int) -> date:
    d = date(year, month, monthrange(year, month)[1])
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


def _calendar(now: datetime) -> str:
    """The real dates behind what people say, as of today. Next week starts on
    the Monday after today, so on a Sunday it starts tomorrow. Only working
    days are listed as days to suggest."""
    today = now.date()

    def say(d: date) -> str:
        return _spoken_day(d, today)

    def run(first: date, last: date) -> str:
        return ", ".join(say(d) for d in _weekdays(first, last))

    monday = today + timedelta(days=7 - today.weekday())
    friday = monday + timedelta(days=4)
    lines = [f"Today is {_spoken_day(today)}.",
             f"Tomorrow: {say(today + timedelta(days=1))}."]
    if today.weekday() < 4:
        lines.append(f"The rest of this week: {run(today + timedelta(days=1), friday - timedelta(days=7))}.")
    lines += [
        f"Next week: {run(monday, friday)}.",
        f"Early next week: {say(monday)}.",
        f"Middle of next week: {say(monday + timedelta(days=2))}.",
        f"Late next week: {say(monday + timedelta(days=3))}, or {say(friday)}.",
        f"The week after next: {say(monday + timedelta(days=7))} to {say(friday + timedelta(days=7))}.",
    ]
    year, month = (today.year + 1, 1) if today.month == 12 else (today.year, today.month + 1)
    month_end = _last_weekday(today.year, today.month)
    if month_end > today:
        lines.append(f"End of this month: {say(month_end)}.")
    lines += [f"Start of next month: {say(_first_weekday(year, month))}.",
              f"End of next month: {say(_last_weekday(year, month))}."]
    return "\n".join(lines)
