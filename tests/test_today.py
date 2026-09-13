"""Tests for the briefing's editing decisions.

Today is an edit of the changes feed, so what it leaves out matters as much as
what it keeps.
"""
from __future__ import annotations

import os
import tempfile

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

from rhodesk import today  # noqa: E402


def test_duplicate_company_name_is_trimmed():
    assert today._headline(
        "Summit Analytics", "Summit Analytics raises Series B at reduced valuation"
    ) == "Summit Analytics · Raises Series B at reduced valuation"


def test_headline_that_does_not_repeat_is_left_alone():
    assert today._headline("Northwind Traders", "Past 90 days") == \
        "Northwind Traders · Past 90 days"


def test_a_headline_that_is_only_the_name_survives():
    """Trimming must never produce an empty headline."""
    assert today._headline("Acme", "Acme") == "Acme · Acme"


def test_unreachable_counterparties_collapse_to_one_row():
    """With no contact enrichment nearly every counterparty has no phone. One
    row per counterparty would be twelve identical lines, not a briefing."""
    queue = {"items": [
        {"id": f"c{i}", "display_name": f"C{i}", "posture": "collect",
         "outstanding": 100_00, "contact_phone": None,
         "contact_email": "a@b.com" if i < 2 else None}
        for i in range(5)
    ]}
    rows = today._needs_you(queue, {"approval_threshold_cents": 10_000_00})
    unreachable = [r for r in rows if r["kind"] == "unreachable"]
    assert len(unreachable) == 1
    assert "5 in the queue" in unreachable[0]["title"]
    assert "2 have an email" in unreachable[0]["detail"]


def test_cover_leads_and_is_urgent():
    queue = {"items": [
        {"id": "a", "display_name": "A", "posture": "collect",
         "outstanding": 90_000_00, "contact_phone": "+1", "contact_email": None},
        {"id": "b", "display_name": "B", "posture": "cover",
         "outstanding": 100_00, "contact_phone": "+1", "contact_email": None},
    ]}
    rows = today._needs_you(queue, {"approval_threshold_cents": 25_000_00})
    assert rows[0]["kind"] == "escalate"
    assert rows[0]["weight"] == "urgent"


def test_cover_is_not_also_listed_as_needing_approval():
    """A counterparty in distress needs escalating, not approving. Listing it
    twice makes the briefing look longer than the work actually is."""
    queue = {"items": [
        {"id": "b", "display_name": "B", "posture": "cover",
         "outstanding": 90_000_00, "contact_phone": "+1", "contact_email": None},
    ]}
    rows = today._needs_you(queue, {"approval_threshold_cents": 25_000_00})
    assert [r["kind"] for r in rows] == ["escalate"]


def test_below_threshold_needs_nothing():
    queue = {"items": [
        {"id": "a", "display_name": "A", "posture": "collect",
         "outstanding": 100_00, "contact_phone": "+1", "contact_email": None},
    ]}
    assert today._needs_you(queue, {"approval_threshold_cents": 25_000_00}) == []


def test_a_failing_service_is_something_a_person_must_know():
    rows = today._degraded({"tavily": {"last_error": "432: credits exhausted"}})
    assert len(rows) == 1
    assert rows[0]["weight"] == "urgent"
    assert "Research is failing" == rows[0]["title"]


def test_healthy_services_raise_nothing():
    assert today._degraded({"tavily": {"live": True}, "llm": {"live": True}}) == []
