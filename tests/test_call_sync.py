"""How the call modal learns that a phone call has ended.

There is no webhook, so the app asks ElevenLabs. These pin the things that
made the screen slow or wrong: waiting for "done" when "processing" already
means nobody is on the line, writing the summary inside the poll, summarising
a transcript ElevenLabs had not attached yet, and asking again straight after
being told to slow down.
"""
from __future__ import annotations

import json
import os
import tempfile
import threading
import time
import uuid

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

from rhodesk import db, voice  # noqa: E402
from rhodesk.pipeline import COUNTERPARTY_COLUMNS  # noqa: E402


def setup_module(_module=None):
    db.init()
    db.reset()
    acme = {
        "id": "acme", "display_name": "Acme", "domain": "", "posture": "collect",
        "risk": "none", "outstanding": 100000, "open_invoices": 1, "oldest_days": 30,
        "monthly_spend": 0, "money_in": 0, "money_out": 0, "txn_count": 1,
        "ar_share": 0.0, "recurring": 0, "duplicate": 0,
    }
    db.upsert("counterparties", [{k: v for k, v in acme.items() if k in COUNTERPARTY_COLUMNS}])


def place(state="live", transcript=(), provider_status=None):
    call_id = uuid.uuid4().hex
    db.upsert("calls", [{
        "id": call_id, "counterparty_id": "acme", "posture": "collect", "state": state,
        "to_number": "+15550000000", "brief": "{}", "transcript": json.dumps(list(transcript)),
        "outcome": "{}", "provider_ref": f"conv_{call_id[:12]}", "simulated": 0,
        "created_at": voice._now(), "ended_at": None, "sim_plan": "{}",
        "provider_status": provider_status,
    }])
    return db.one("calls", call_id)


def elevenlabs_says(monkeypatch, status, turns):
    """Stand in for ElevenLabs. Returns the list of conversations it was asked for."""
    asked = []

    class Fake:
        live = True

        def fetch_conversation(self, ref):
            asked.append(ref)
            return {"status": status,
                    "metadata": {"accepted_time_unix_secs": 1},
                    "transcript": [{"role": r, "message": m} for r, m in turns]}

    monkeypatch.setattr(voice, "VoiceClient", Fake)
    return asked


def summary_counts_turns(monkeypatch):
    monkeypatch.setattr(voice, "extract_outcome",
                        lambda turns, name: {"result": "commitment", "summary": f"{len(turns)} turns"})


def written(call_id, timeout=3.0):
    """Wait for the background write-up to land."""
    stop = time.monotonic() + timeout
    while time.monotonic() < stop:
        row = db.one("calls", call_id)
        if row["state"] == "done" and call_id not in voice._writing:
            return row
        time.sleep(0.01)
    raise AssertionError(f"write-up never finished, state is {db.one('calls', call_id)['state']}")


def test_processing_means_the_call_has_ended(monkeypatch):
    """The regression. The screen waited for "done", which only arrives once
    ElevenLabs finishes its own analysis: 14 to 20 seconds after the hangup."""
    summary_counts_turns(monkeypatch)
    elevenlabs_says(monkeypatch, "processing", [("agent", "Hi"), ("user", "We'll pay Friday")])
    call = place()

    changed = voice.sync_call(call, force=True)

    assert changed["state"] == "wrapping" and changed["ended_at"]
    assert written(call["id"])["outcome"]["summary"] == "2 turns"


def test_the_summary_does_not_hold_up_the_poll(monkeypatch):
    """The poll that notices the end returns straight away and the screen says
    Rhonica is writing the summary; the summary itself lands afterwards."""
    release = threading.Event()

    def slow_summary(turns, name):
        release.wait(2)
        return {"result": "none", "summary": "slow"}

    monkeypatch.setattr(voice, "extract_outcome", slow_summary)
    elevenlabs_says(monkeypatch, "processing", [("agent", "Hi")])
    call = place()

    started = time.monotonic()
    assert voice.sync_call(call, force=True)["state"] == "wrapping"
    assert time.monotonic() - started < 0.5
    assert db.one("calls", call["id"])["state"] == "wrapping"

    release.set()
    assert written(call["id"])["outcome"]["summary"] == "slow"


def test_a_live_call_streams_its_transcript(monkeypatch):
    elevenlabs_says(monkeypatch, "in-progress", [("agent", "Hi"), ("user", "Hello")])
    call = place()

    changed = voice.sync_call(call, force=True)

    assert "state" not in changed
    assert len(changed["transcript"]) == 2 and changed["connected_at"]
    assert db.one("calls", call["id"])["state"] == "live"


def test_a_transcript_that_grows_after_the_summary_is_rewritten(monkeypatch):
    """The summary starts while ElevenLabs is still processing. If a turn
    arrives after that, the summary is redone on the full conversation."""
    summary_counts_turns(monkeypatch)
    elevenlabs_says(monkeypatch, "done", [("agent", "Hi"), ("user", "Friday"), ("agent", "Great")])
    call = place(state="done", provider_status="processing",
                 transcript=[{"role": "agent", "text": "Hi"}, {"role": "human", "text": "Friday"}])

    assert voice.sync_call(call, force=True)["state"] == "wrapping"

    row = written(call["id"])
    assert row["outcome"]["summary"] == "3 turns"
    assert row["provider_status"] == "done"


def test_a_finished_call_is_never_fetched_again(monkeypatch):
    asked = elevenlabs_says(monkeypatch, "done", [])
    call = place(state="done", provider_status="done")

    assert voice.sync_call(call, force=True) is None
    assert asked == []


def test_a_429_makes_that_conversation_wait(monkeypatch):
    class TooManyRequests:
        status_code = 429

    class Client:
        def get(self, *args, **kwargs):
            return TooManyRequests()

    class Live(voice.VoiceClient):
        live = True

    monkeypatch.setattr(voice, "_http_client", lambda: Client())
    call = place()
    ref = call["provider_ref"]

    assert Live().fetch_conversation(ref) is None
    assert voice._blocked_until[ref] > time.monotonic()

    asked = elevenlabs_says(monkeypatch, "in-progress", [("agent", "Hi")])
    assert voice.sync_call(call, force=True) is None
    assert asked == []


def test_an_empty_transcript_at_processing_is_not_summarised(monkeypatch):
    """The second regression. ElevenLabs had not attached the transcript at
    "processing", so a real 21-turn call was recorded as "No conversation
    recorded". The summary now waits for the transcript to arrive."""
    summary_counts_turns(monkeypatch)
    elevenlabs_says(monkeypatch, "processing", [])
    call = place()

    assert voice.sync_call(call, force=True)["state"] == "wrapping"
    time.sleep(0.05)
    row = db.one("calls", call["id"])
    assert row["state"] == "wrapping" and row["outcome"] == {}
    assert call["id"] not in voice._writing

    # Another poll while ElevenLabs is still processing starts nothing either.
    assert voice.sync_call(row, force=True) is None
    time.sleep(0.05)
    assert db.one("calls", call["id"])["state"] == "wrapping"

    elevenlabs_says(monkeypatch, "done", [("agent", "Hi"), ("user", "Friday works")])
    voice.sync_call(db.one("calls", call["id"]), force=True)
    assert written(call["id"])["outcome"]["summary"] == "2 turns"


def test_a_call_nobody_spoke_on_is_summarised_once_elevenlabs_is_done(monkeypatch):
    """Silence is only believed once ElevenLabs says it has finished."""
    summary_counts_turns(monkeypatch)
    elevenlabs_says(monkeypatch, "processing", [])
    call = place()
    voice.sync_call(call, force=True)

    elevenlabs_says(monkeypatch, "done", [])
    voice.sync_call(db.one("calls", call["id"]), force=True)

    row = written(call["id"])
    assert row["outcome"]["summary"] == "0 turns"
    assert row["provider_status"] == "done"
