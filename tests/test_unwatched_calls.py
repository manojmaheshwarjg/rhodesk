"""A call nobody is watching still has to finish.

The call modal finishes a call while it is open. Close the page mid-call and,
before this, nothing did until the Calls tab was opened: the board and the
Timeline kept saying "On a call now", and Rhonica's next call did not know the
last one had happened.
"""
from __future__ import annotations

import json
import os
import tempfile
import uuid
from datetime import datetime, timedelta, timezone

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

from rhodesk import api, call_history, db, voice  # noqa: E402
from rhodesk.pipeline import COUNTERPARTY_COLUMNS  # noqa: E402


def setup_module(_module=None):
    db.init()
    db.reset()
    for cid in ("walked-away", "quiet"):
        company = {
            "id": cid, "display_name": cid, "domain": "", "posture": "collect", "risk": "none",
            "outstanding": 100000, "open_invoices": 1, "oldest_days": 30, "monthly_spend": 0,
            "money_in": 0, "money_out": 0, "txn_count": 1, "ar_share": 0.0, "recurring": 0,
            "duplicate": 0,
        }
        db.upsert("counterparties", [{k: v for k, v in company.items() if k in COUNTERPARTY_COLUMNS}])


def left_open(cp_id, *, to="+15550000000", ref=None, minutes_ago=10):
    """A call placed and then left alone. Its script ran out long ago."""
    call_id = uuid.uuid4().hex
    plan = {"script": [{"role": "agent", "text": "Hi"}, {"role": "human", "text": "Friday works"}],
            "outcome": {"result": "commitment", "summary": "Agreed to pay on Friday.",
                        "answered": True, "commitments": []}}
    db.upsert("calls", [{
        "id": call_id, "counterparty_id": cp_id, "posture": "collect", "state": "live",
        "to_number": to, "brief": "{}", "transcript": "[]", "outcome": "{}",
        "provider_ref": ref or f"sim_{call_id[:8]}", "simulated": 0 if ref else 1,
        "created_at": (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).isoformat(),
        "ended_at": None, "sim_plan": "{}" if ref else json.dumps(plan),
    }])
    return call_id


def test_opening_the_timeline_finishes_a_call_nobody_watched():
    call_id = left_open("walked-away")

    shown = api.counterparty_calls("walked-away")["calls"][0]

    assert shown["id"] == call_id and shown["state"] == "done"
    assert shown["summary"] == "Agreed to pay on Friday."


def test_loading_the_board_finishes_it_too():
    call_id = left_open("walked-away")

    api.board()

    assert db.one("calls", call_id)["state"] == "done"


def test_rhonicas_next_call_knows_about_it():
    """What a single call, the batch and the browser session each do before
    they build her variables."""
    left_open("walked-away")

    api._finish_open_calls("walked-away")

    assert "Agreed to pay on Friday" in call_history.agent_context({"id": "walked-away"})["call_history"]


def test_elevenlabs_is_only_asked_when_a_real_call_is_open(monkeypatch):
    asked = []
    monkeypatch.setattr(voice, "reconcile", lambda **kw: asked.append(kw))

    api._finish_open_calls("quiet")
    assert asked == []                              # nothing open: one query, no request

    real = left_open("quiet", ref="conv_quietcall")
    try:
        api._finish_open_calls("quiet")
        assert asked == [{"force": False}]          # and it respects the one-second limit
    finally:
        db.set_fields("calls", real, state="done", provider_status="done")


def test_a_rehearsal_left_open_is_not_treated_as_a_call():
    rehearsal = left_open("quiet", to="browser")

    api._finish_open_calls("quiet")

    assert db.one("calls", rehearsal)["state"] == "live"
