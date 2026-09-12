"""Desk settings: one persisted row that actually drives behaviour.

The approval threshold gates dialling, the guardrails are handed to the voice
agent verbatim in its brief, and the do-not-call list is enforced before a
call is placed. Changing a value here changes what the agent does, which is
the whole point of the screen.

`.env` supplies the first-run defaults; after that the stored row wins.
"""
from __future__ import annotations

import json

from . import config, db

KEY = "desk"

DEFAULTS: dict = {
    "company_name": config.COMPANY_NAME,
    "approval_threshold_cents": config.APPROVAL_THRESHOLD_CENTS,
    "overdue_days": config.OVERDUE_DAYS,
    # Voice and identity
    "voice_name": "Quinn",
    "tone": "measured",
    "disclose_ai": True,
    "announce_recording": True,
    # Negotiating room
    "payment_window_days": 21,
    "max_instalments": 2,
    "may_agree": [
        "A payment date within the window below",
        "A split into instalments, up to the limit below",
        "Re-sending the invoice to a second address",
    ],
    "must_not": [
        "Offer a discount or write off any amount",
        "Threaten collections, legal action or credit reporting",
        "Mention anything learned from public sources",
    ],
    # Safety
    "do_not_call": [],
    "demo_override_number": config.DEMO_OVERRIDE_NUMBER,
    "calls_per_run": 5,
}


def _ensure_table() -> None:
    with db.cursor() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS settings ("
                     "id TEXT PRIMARY KEY, value TEXT NOT NULL)")


def get() -> dict:
    _ensure_table()
    with db.cursor() as conn:
        row = conn.execute("SELECT value FROM settings WHERE id=?", (KEY,)).fetchone()
    stored = {}
    if row:
        try:
            stored = json.loads(row["value"])
        except (json.JSONDecodeError, TypeError):
            stored = {}
    return {**DEFAULTS, **stored}


def put(patch: dict) -> dict:
    """Merge a patch over the stored row. Unknown keys are dropped so the UI
    cannot inject arbitrary fields."""
    current = get()
    clean = {k: v for k, v in (patch or {}).items() if k in DEFAULTS}

    # Coerce the numeric fields rather than trusting the form.
    for key in ("approval_threshold_cents", "overdue_days",
                "payment_window_days", "max_instalments", "calls_per_run"):
        if key in clean:
            try:
                clean[key] = max(0, int(clean[key]))
            except (TypeError, ValueError):
                clean.pop(key)
    for key in ("may_agree", "must_not", "do_not_call"):
        if key in clean and not isinstance(clean[key], list):
            clean.pop(key)
    for key in ("disclose_ai", "announce_recording"):
        if key in clean:
            clean[key] = bool(clean[key])

    merged = {**current, **clean}
    _ensure_table()
    with db.cursor() as conn:
        conn.execute("INSERT INTO settings (id, value) VALUES (?,?) "
                     "ON CONFLICT(id) DO UPDATE SET value=excluded.value",
                     (KEY, json.dumps(merged)))
    return merged


def reset() -> dict:
    _ensure_table()
    with db.cursor() as conn:
        conn.execute("DELETE FROM settings WHERE id=?", (KEY,))
    return get()
