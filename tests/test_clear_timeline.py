"""Clear timeline, the dev link under a counterparty's Timeline.

It exists so a demo can start fresh: after it, Rhonica's next call has to open
as a first call, with nothing of the old ones left in her context. It must not
touch anyone else's calls, or pull a call out from under a live conversation.
"""
from __future__ import annotations

import json
import os
import tempfile
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

from rhodesk import api, call_history, db  # noqa: E402
from rhodesk.pipeline import COUNTERPARTY_COLUMNS  # noqa: E402


def setup_module(_module=None):
    db.init()
    for cid in ("clear-me", "keep-me"):
        company = {
            "id": cid, "display_name": cid, "domain": "", "posture": "collect", "risk": "none",
            "outstanding": 100000, "open_invoices": 1, "oldest_days": 30, "monthly_spend": 0,
            "money_in": 0, "money_out": 0, "txn_count": 1, "ar_share": 0.0, "recurring": 0,
            "duplicate": 0,
        }
        db.upsert("counterparties", [{k: v for k, v in company.items() if k in COUNTERPARTY_COLUMNS}])


def call(cp_id, *, to="+15550000000", state="done", minutes_ago=30, script=None):
    call_id = uuid.uuid4().hex
    outcome = {"result": "commitment", "summary": "Agreed to pay on Friday.", "answered": True}
    db.upsert("calls", [{
        "id": call_id, "counterparty_id": cp_id, "posture": "collect", "state": state,
        "to_number": to, "brief": "{}", "transcript": "[]", "outcome": json.dumps(outcome),
        "provider_ref": f"sim_{call_id[:8]}", "simulated": 1,
        "created_at": (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).isoformat(),
        "ended_at": datetime.now(timezone.utc).isoformat() if state == "done" else None,
        "sim_plan": json.dumps({"script": script, "outcome": outcome} if script else {}),
    }])
    return call_id


def test_clearing_leaves_rhonica_nothing_to_follow_up_on():
    call("clear-me")
    call("clear-me", minutes_ago=90)
    assert "Agreed to pay on Friday" in call_history.agent_context({"id": "clear-me"})["call_history"]

    assert api.clear_timeline("clear-me") == {"cleared": 2}

    ctx = call_history.agent_context({"id": "clear-me", "contact_name": None})
    assert call_history.for_counterparty("clear-me") == []
    assert ctx["call_history"] == "No earlier calls. This is the first time you are calling them."
    assert ctx["opener"].startswith("Hey there, it's Rhonica from the accounts team at")
    assert api._last_call("clear-me", db.query("calls", order="created_at DESC")) is None


def test_it_touches_nothing_else():
    someone_else = call("keep-me")
    rehearsal = call("clear-me", to="browser")

    api.clear_timeline("clear-me")

    assert db.one("calls", someone_else) and db.one("calls", rehearsal)


def test_a_call_still_in_progress_is_not_cleared():
    live = call("clear-me", state="live", minutes_ago=0,
                script=[{"role": "agent", "text": "Hi"}] * 50)      # nowhere near over
    try:
        with pytest.raises(HTTPException) as refused:
            api.clear_timeline("clear-me")
        assert refused.value.status_code == 409
        assert db.one("calls", live)["state"] == "live"
    finally:
        db.set_fields("calls", live, state="done")


def test_an_unknown_counterparty_is_refused():
    with pytest.raises(HTTPException) as refused:
        api.clear_timeline("nobody")
    assert refused.value.status_code == 404
