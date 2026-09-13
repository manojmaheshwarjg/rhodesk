"""A counterparty's call history: what the Timeline modal shows, and what
Rhonica is told before a follow-up call."""
from __future__ import annotations

import json
import os
import tempfile
import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

from rhodesk import call_history, db  # noqa: E402
from rhodesk.pipeline import COUNTERPARTY_COLUMNS  # noqa: E402

NY = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")
NOW = datetime(2026, 9, 13, 15, 0, tzinfo=NY)        # a Sunday, 3 PM


def setup_module(_module=None):
    db.init()
    for cid in ("hist-none", "hist-calls"):
        company = {
            "id": cid, "display_name": cid, "domain": "", "posture": "collect", "risk": "none",
            "outstanding": 5920000, "open_invoices": 1, "oldest_days": 94, "monthly_spend": 0,
            "money_in": 0, "money_out": 0, "txn_count": 1, "ar_share": 0.0, "recurring": 0,
            "duplicate": 0,
        }
        db.upsert("counterparties", [{k: v for k, v in company.items() if k in COUNTERPARTY_COLUMNS}])


def call(cp_id, at, *, to="+15550000000", summary="", result="none", answered=True,
         secs=120, commitments=()):
    db.upsert("calls", [{
        "id": uuid.uuid4().hex, "counterparty_id": cp_id, "posture": "collect", "state": "done",
        "to_number": to, "brief": "{}", "transcript": "[]",
        "outcome": json.dumps({"result": result, "summary": summary, "answered": answered,
                               "commitments": list(commitments)}),
        "provider_ref": "", "simulated": 1,
        "created_at": at.astimezone(UTC).isoformat(),
        "ended_at": (at + timedelta(seconds=secs)).astimezone(UTC).isoformat(),
        "sim_plan": "{}",
    }])


def test_how_long_ago_reads_like_a_person_on_the_phone():
    ago = lambda **kw: call_history.say_ago(NOW - timedelta(**kw), NOW)  # noqa: E731
    assert ago(minutes=4) == "a few minutes ago"
    assert ago(minutes=22) == "about twenty minutes ago"
    assert ago(minutes=70) == "about an hour ago"
    assert ago(hours=2) == "about two hours ago"
    assert ago(hours=8) == "this morning"
    assert ago(hours=25) == "yesterday afternoon"
    assert ago(days=3) == "on Thursday"
    assert ago(days=9) == "last week"


def test_a_first_call_opens_with_the_full_introduction():
    assert call_history.opener("Sam", "FusionTech", None, None, NOW) == (
        "Hey Sam, it's Rhonica. I'm an AI assistant calling from FusionTech, "
        "and I should mention this call is being recorded. Is now a good time for a quick chat?")


def test_a_follow_up_hours_later_acknowledges_the_last_call():
    spoke = {"at": (NOW - timedelta(hours=2)).isoformat()}
    assert call_history.opener("Sam", "FusionTech", spoke, spoke, NOW) == (
        "Hey Sam, it's Rhonica again, the AI assistant from FusionTech. "
        "We spoke about two hours ago, and I should mention this call is being recorded too. "
        "Is now still a good time for a quick chat?")


def test_a_follow_up_the_next_day_asks_afresh():
    spoke = {"at": (NOW - timedelta(hours=25)).isoformat()}
    line = call_history.opener("Sam", "FusionTech", spoke, spoke, NOW)
    assert "We spoke yesterday afternoon" in line
    assert line.endswith("Is now a good time for a quick chat?")


def test_after_an_unanswered_call_she_does_not_claim_they_spoke():
    """Nobody picked up, so they have never heard her introduce herself."""
    tried = {"at": (NOW - timedelta(days=3)).isoformat()}
    line = call_history.opener("Sam", "FusionTech", None, tried, NOW)
    assert line.startswith("Hey Sam, it's Rhonica. I'm an AI assistant calling from FusionTech. "
                           "I tried you on Thursday, and I should mention this call is being recorded.")
    assert "We spoke" not in line


def test_history_is_newest_first_and_leaves_out_rehearsals():
    call("hist-calls", NOW - timedelta(days=2), summary="Asked to be called back Monday.",
         result="callback")
    call("hist-calls", NOW - timedelta(hours=2), summary="Agreed to pay on Friday.",
         result="commitment", commitments=[{"label": "payment_date", "value": "Friday the eighteenth"}])
    call("hist-calls", NOW - timedelta(hours=1), to="browser", summary="Operator rehearsal.")

    calls = call_history.for_counterparty("hist-calls")

    assert [c["summary"] for c in calls] == ["Agreed to pay on Friday.", "Asked to be called back Monday."]
    assert calls[0]["duration_secs"] == 120


def test_rhonica_is_told_the_time_and_what_happened():
    ctx = call_history.agent_context({"id": "hist-calls", "contact_name": "Sam"}, now=NOW)

    assert ctx["now"] == "Sunday 13 September 2026, 3:00 PM EDT"
    latest, earlier = ctx["call_history"].splitlines()
    assert latest == ("- Sunday 13 September, 1:00 PM EDT (about two hours ago), answered, "
                      "lasted 2:00: Agreed to pay on Friday. Agreed: Payment date: Friday the eighteenth.")
    assert earlier.startswith("- Friday 11 September, 3:00 PM EDT (on Friday), answered")
    assert "rehearsal" not in ctx["call_history"]
    assert ctx["opener"].startswith("Hey Sam, it's Rhonica again")


def test_with_no_calls_she_knows_it_is_the_first():
    ctx = call_history.agent_context({"id": "hist-none", "contact_name": None}, now=NOW)
    assert ctx["call_history"] == "No earlier calls. This is the first time you are calling them."
    assert ctx["opener"].startswith("Hey there, it's Rhonica. I'm an AI assistant")


def test_every_opener_says_she_is_an_ai_and_the_call_is_being_recorded():
    """Whatever the history, the first line carries both disclosures."""
    recent = {"at": (NOW - timedelta(hours=2)).isoformat()}
    older = {"at": (NOW - timedelta(days=3)).isoformat()}
    for spoke, tried in ((None, None), (recent, recent), (older, older), (None, older)):
        line = call_history.opener("Sam", "FusionTech", spoke, tried, NOW)
        assert "AI assistant" in line, line
        assert "this call is being recorded" in line, line
