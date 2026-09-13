"""The clock that runs the desk.

Research is not something an operator should have to remember. It runs at a
fixed hour, qualifies the ledger, and leaves a notification saying what came
back. The board then reads as of that run rather than as of whenever somebody
last pressed a button.

One thread, one job. It holds the same lock the manual trigger uses, so a
scheduled run and a hand-started one can never overlap.
"""
from __future__ import annotations

import threading
import uuid
from datetime import datetime, timedelta, timezone

from . import config, db

_thread: threading.Thread | None = None
_stop = threading.Event()
_state: dict = {"last_fired": None, "next_due": None, "running": False}

TICK_SECONDS = 20


def next_due(now: datetime | None = None) -> datetime:
    """The next occurrence of the configured hour, in local time."""
    now = (now or datetime.now(timezone.utc)).astimezone()
    due = now.replace(hour=config.RESEARCH_HOUR, minute=0, second=0, microsecond=0)
    if due <= now:
        due += timedelta(days=1)
    return due


def notify(title: str, detail: str = "", kind: str = "research",
           run_id: int | None = None) -> None:
    db.upsert("notifications", [{
        "id": uuid.uuid4().hex, "at": datetime.now(timezone.utc).isoformat(),
        "kind": kind, "title": title, "detail": detail,
        "run_id": run_id, "read_at": None,
    }])


def run_once(trigger: str = "schedule") -> dict:
    """Research the whole ledger, then say what is now worth calling."""
    from . import api, pipeline

    if not api._run_lock.acquire(blocking=False):
        return {"ran": False, "reason": "a run is already in progress"}
    _state["running"] = True
    try:
        result = pipeline.run_desk()
    except Exception as exc:  # noqa: BLE001 - a failed run still gets reported
        notify("Research failed", str(exc)[:240], kind="error")
        return {"ran": False, "reason": str(exc)[:240]}
    finally:
        _state["running"] = False
        api._run_lock.release()

    scope = _qualified()
    notify(
        f"{len(scope['call'])} counterparties qualified to call",
        _summarise(scope, result),
        run_id=result.get("run_id"),
    )
    _state["last_fired"] = datetime.now(timezone.utc).isoformat()
    return {"ran": True, "trigger": trigger, **result, "qualified": len(scope["call"])}


def _qualified() -> dict:
    from . import history

    current = history.current_run()
    where, params = ("last_seen_run = ?", (current,)) if current else ("", ())
    rows = db.query("counterparties", where, params, "outstanding DESC")
    return {
        "call": [r for r in rows if (r.get("verdict") or "none") in ("call", "escalate")],
        "escalate": [r for r in rows if (r.get("verdict") or "") == "escalate"],
    }


def _summarise(scope: dict, result: dict) -> str:
    names = ", ".join(r["display_name"] for r in scope["call"][:4])
    more = len(scope["call"]) - 4
    parts = []
    if names:
        parts.append(names + (f" and {more} more" if more > 0 else ""))
    if scope["escalate"]:
        parts.append(f"{len(scope['escalate'])} showing distress and marked to escalate")
    if result.get("degraded"):
        parts.append("some stages were degraded, so this run is incomplete")
    if not parts:
        return "Nothing qualified this run."
    return ". ".join(p[0].upper() + p[1:] for p in parts) + "."


def _loop() -> None:
    _state["next_due"] = next_due().isoformat()
    while not _stop.is_set():
        due = datetime.fromisoformat(_state["next_due"])
        if datetime.now(timezone.utc).astimezone() >= due:
            run_once()
            _state["next_due"] = next_due().isoformat()
        _stop.wait(TICK_SECONDS)


def start() -> None:
    global _thread
    if not config.SCHEDULER_ENABLED or (_thread and _thread.is_alive()):
        return
    _stop.clear()
    _thread = threading.Thread(target=_loop, name="rhodesk-scheduler", daemon=True)
    _thread.start()


def status() -> dict:
    return {
        "enabled": config.SCHEDULER_ENABLED,
        "hour": config.RESEARCH_HOUR,
        "next_due": _state["next_due"] or next_due().isoformat(),
        "last_fired": _state["last_fired"],
        "running": _state["running"],
    }
