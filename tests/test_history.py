"""Tests for the history layer.

The diff is the part of the desk with real logic and no model in it, so it is
the part worth pinning down.
"""
from __future__ import annotations

import os
import tempfile

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

from rhodesk import db, history  # noqa: E402


def setup_module(_module=None):
    db.init()
    db.reset()


def snapshot(run_id, companies, counts=None):
    """Mirrors what run_desk stores: the table takes only real columns, the
    snapshot takes the whole company."""
    from rhodesk.pipeline import COUNTERPARTY_COLUMNS
    db.upsert("counterparties", [
        {**{k: v for k, v in c.items() if k in COUNTERPARTY_COLUMNS},
         "first_seen_run": run_id, "last_seen_run": run_id} for c in companies])
    history.capture(run_id, companies, counts or {})


def cp(cid, **over):
    base = {
        "id": cid, "display_name": cid.replace("-", " ").title(), "domain": "",
        "posture": "watch", "risk": "none", "outstanding": 0, "open_invoices": 0,
        "oldest_days": 0, "monthly_spend": 0, "money_in": 0, "money_out": 0,
        "txn_count": 1, "ar_share": 0.0, "recurring": 0, "duplicate": 0,
    }
    base.update(over)
    return base


def kinds(changes):
    return {c["kind"] for c in changes}


def by_kind(changes, kind):
    return [c for c in changes if c["kind"] == kind]


def test_first_run_reports_nothing():
    """28 counterparties appearing at once is not news, it is the first run."""
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", outstanding=100_00)])
    history.finish_run(r1)
    assert history.diff(r1, None) == []


def test_posture_change_is_reported():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", posture="watch", outstanding=500_00)])
    history.finish_run(r1)

    r2 = history.start_run()
    snapshot(r2, [cp("acme", posture="collect", outstanding=500_00)])
    history.finish_run(r2)

    changes = history.diff(r2, r1)
    posture = by_kind(changes, "posture")
    assert len(posture) == 1
    assert posture[0]["from_value"] == "watch"
    assert posture[0]["to_value"] == "collect"
    assert posture[0]["weight"] == "attention"


def test_escalation_to_cover_is_urgent():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", posture="collect", outstanding=500_00)])
    history.finish_run(r1)

    r2 = history.start_run()
    snapshot(r2, [cp("acme", posture="cover", outstanding=500_00)])
    history.finish_run(r2)

    assert by_kind(history.diff(r2, r1), "posture")[0]["weight"] == "urgent"


def test_aging_band_crossing():
    """29 to 31 days matters. 31 to 33 does not."""
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", outstanding=500_00, oldest_days=29),
                  cp("beta", outstanding=500_00, oldest_days=31)])
    history.finish_run(r1)

    r2 = history.start_run()
    snapshot(r2, [cp("acme", outstanding=500_00, oldest_days=31),
                  cp("beta", outstanding=500_00, oldest_days=33)])
    history.finish_run(r2)

    aging = by_kind(history.diff(r2, r1), "aging")
    assert [a["counterparty_id"] for a in aging] == ["acme"]
    assert aging[0]["weight"] == "attention"


def test_ninety_days_is_urgent():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", outstanding=500_00, oldest_days=88)])
    history.finish_run(r1)
    r2 = history.start_run()
    snapshot(r2, [cp("acme", outstanding=500_00, oldest_days=91)])
    history.finish_run(r2)
    assert by_kind(history.diff(r2, r1), "aging")[0]["weight"] == "urgent"


def test_paid_off_is_good_news():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", outstanding=1_200_00, open_invoices=2)])
    history.finish_run(r1)
    r2 = history.start_run()
    snapshot(r2, [cp("acme", outstanding=0, open_invoices=0)])
    history.finish_run(r2)

    cleared = by_kind(history.diff(r2, r1), "cleared")
    assert len(cleared) == 1
    assert cleared[0]["weight"] == "good"
    assert cleared[0]["amount"] == 1_200_00


def test_immaterial_movement_is_ignored():
    """A $12 change on a $5,000 balance is not a briefing item."""
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", outstanding=5_000_00)])
    history.finish_run(r1)
    r2 = history.start_run()
    snapshot(r2, [cp("acme", outstanding=5_012_00)])
    history.finish_run(r2)
    assert by_kind(history.diff(r2, r1), "outstanding") == []


def test_material_movement_is_reported():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", outstanding=5_000_00)])
    history.finish_run(r1)
    r2 = history.start_run()
    snapshot(r2, [cp("acme", outstanding=8_000_00)])
    history.finish_run(r2)
    moved = by_kind(history.diff(r2, r1), "outstanding")
    assert len(moved) == 1
    assert moved[0]["amount"] == 3_000_00


def test_appeared_and_disappeared():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme"), cp("gone", outstanding=100_00)])
    history.finish_run(r1)
    r2 = history.start_run()
    snapshot(r2, [cp("acme"), cp("fresh", outstanding=900_00)])
    history.finish_run(r2)

    changes = history.diff(r2, r1)
    assert [c["counterparty_id"] for c in by_kind(changes, "appeared")] == ["fresh"]
    assert [c["counterparty_id"] for c in by_kind(changes, "disappeared")] == ["gone"]


def test_duplicate_detection_fires_once():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("asana", duplicate=0, monthly_spend=200_00)])
    history.finish_run(r1)
    r2 = history.start_run()
    snapshot(r2, [cp("asana", duplicate=1, monthly_spend=200_00)])
    history.finish_run(r2)
    assert len(by_kind(history.diff(r2, r1), "duplicate")) == 1

    r3 = history.start_run()
    snapshot(r3, [cp("asana", duplicate=1, monthly_spend=200_00)])
    history.finish_run(r3)
    assert by_kind(history.diff(r3, r2), "duplicate") == []


def test_new_signals_only():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", outstanding=100_00)])
    history.finish_run(r1)
    r2 = history.start_run()
    snapshot(r2, [cp("acme", outstanding=100_00)])
    history.finish_run(r2)

    sig = {"id": "s1", "counterparty_id": "acme", "severity": "severe",
           "title": "Down round", "detail": "Half the prior valuation.",
           "source_url": "https://example.com/x"}
    changes = history.diff(r2, r1, [sig])
    found = by_kind(changes, "signal")
    assert len(found) == 1
    assert found[0]["weight"] == "urgent"
    assert found[0]["source_url"] == "https://example.com/x"

    # the same signal seen again is not a change
    assert by_kind(history.diff(r2, r1, []), "signal") == []


def test_urgent_sorts_first():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("a", outstanding=100_00, oldest_days=10),
                  cp("b", outstanding=100_00, posture="watch")])
    history.finish_run(r1)
    r2 = history.start_run()
    snapshot(r2, [cp("a", outstanding=100_00, oldest_days=95),
                  cp("b", outstanding=100_00, posture="collect")])
    history.finish_run(r2)
    changes = history.diff(r2, r1)
    assert changes[0]["weight"] == "urgent"


def test_rename_keeps_identity():
    """A resolver that changes its mind must not orphan a counterparty."""
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("amazon-web-services", display_name="Amazon Web Services",
                     domain="amazon.com")])
    history.finish_run(r1)

    incoming = [{"id": "amazon-com-inc", "display_name": "Amazon.com, Inc.",
                 "domain": "amazon.com", "aliases": ["AWS"]}]
    carried = history.carry_identity(incoming, r1)
    assert carried[0]["id"] == "amazon-web-services"
    assert carried[0]["renamed_from"] == "Amazon Web Services"


def test_rename_by_alias_when_no_domain():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme-corp", display_name="Acme Corp", domain="")])
    history.finish_run(r1)

    incoming = [{"id": "acme-corporation", "display_name": "Acme Corporation",
                 "domain": "", "aliases": ["Acme Corp", "ACME"]}]
    carried = history.carry_identity(incoming, r1)
    assert carried[0]["id"] == "acme-corp"


def test_unrelated_companies_are_not_merged():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("northwind", display_name="Northwind", domain="northwind.com")])
    history.finish_run(r1)

    incoming = [{"id": "summit", "display_name": "Summit Analytics",
                 "domain": "summit.io", "aliases": []}]
    carried = history.carry_identity(incoming, r1)
    assert carried[0]["id"] == "summit"
    assert "renamed_from" not in carried[0]


def test_changes_are_stored_and_readable():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", posture="watch", outstanding=500_00)])
    history.finish_run(r1)
    r2 = history.start_run()
    snapshot(r2, [cp("acme", posture="collect", outstanding=500_00)])
    changes = history.diff(r2, r1)
    history.store(changes)
    history.finish_run(r2, change_count=len(changes))

    read_back = history.changes_for(r2)
    assert len(read_back) == len(changes)
    assert read_back[0]["kind"] == "posture"

    # storing twice must not duplicate: change ids are deterministic
    history.store(history.diff(r2, r1))
    assert len(history.changes_for(r2)) == len(changes)


def test_degraded_run_suppresses_identity_churn():
    """If entity resolution could not run, the counterparty set is an artefact
    of our outage. Reporting it as news would be reporting our own failure as
    the customer's."""
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("amazon", display_name="Amazon.com, Inc.", outstanding=0)])
    history.finish_run(r1)

    r2 = history.start_run()
    snapshot(r2, [cp("aws"), cp("amzn-aws"), cp("amazon-web")])
    history.mark_degraded(r2, ["resolve"])
    history.finish_run(r2, degraded=True)

    changes = history.diff(r2, r1)
    assert by_kind(changes, "appeared") == []
    assert by_kind(changes, "disappeared") == []
    assert len(by_kind(changes, "degraded")) == 1


def test_healthy_run_still_reports_identity_changes():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("amazon")])
    history.finish_run(r1)
    r2 = history.start_run()
    snapshot(r2, [cp("amazon"), cp("stripe", outstanding=400_00)])
    history.finish_run(r2)
    assert len(by_kind(history.diff(r2, r1), "appeared")) == 1


def test_signal_key_ignores_the_headline():
    """The model rewords the same story every run. Keying on the page it came
    from is what stops the briefing drowning in its own noise."""
    from rhodesk.pipeline import signal_key
    a = signal_key("acme", "Acme cuts 1,600 jobs", "https://reuters.com/x/y")
    b = signal_key("acme", "Acme to lay off 1,600 staff", "https://www.reuters.com/x/y/")
    assert a == b


def test_signal_key_separates_different_stories():
    from rhodesk.pipeline import signal_key
    a = signal_key("acme", "Layoffs", "https://reuters.com/a")
    b = signal_key("acme", "Layoffs", "https://reuters.com/b")
    assert a != b


def test_signal_key_separates_counterparties():
    from rhodesk.pipeline import signal_key
    assert (signal_key("acme", "Layoffs", "https://reuters.com/a")
            != signal_key("beta", "Layoffs", "https://reuters.com/a"))


def test_signal_key_falls_back_to_title_without_a_source():
    from rhodesk.pipeline import signal_key
    assert signal_key("acme", "No public news", "") == signal_key("acme", "no public news!", "")


def test_research_outage_does_not_become_good_news():
    """Tavily running out of credits made every risk read 'high to none'.
    Silence from a service we could not reach is not the same as silence in
    the world."""
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", risk="high", posture="cover", outstanding=900_00)])
    history.finish_run(r1)

    r2 = history.start_run()
    snapshot(r2, [cp("acme", risk="none", posture="collect", outstanding=900_00)])
    history.mark_degraded(r2, ["research"])
    history.finish_run(r2, degraded=True)

    changes = history.diff(r2, r1)
    assert by_kind(changes, "risk") == []
    assert by_kind(changes, "posture") == []
    assert by_kind(changes, "signal") == []
    assert len(by_kind(changes, "degraded")) == 1


def test_research_outage_still_reports_the_ledger():
    """The ledger does not depend on the outside world, so money and ageing
    survive a research outage."""
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", outstanding=900_00, oldest_days=55, risk="high")])
    history.finish_run(r1)

    r2 = history.start_run()
    snapshot(r2, [cp("acme", outstanding=0, oldest_days=0, risk="none")])
    history.mark_degraded(r2, ["research"])
    history.finish_run(r2, degraded=True)

    changes = history.diff(r2, r1)
    assert len(by_kind(changes, "cleared")) == 1
    assert by_kind(changes, "risk") == []


def test_degradation_in_either_run_suppresses_both_ways():
    """A healthy run compared against a broken one is still a broken
    comparison."""
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", risk="none")])
    history.mark_degraded(r1, ["research"])
    history.finish_run(r1, degraded=True)

    r2 = history.start_run()
    snapshot(r2, [cp("acme", risk="high")])
    history.finish_run(r2)

    assert by_kind(history.diff(r2, r1), "risk") == []


def test_both_stages_degraded_gives_two_explanations():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", risk="high")])
    history.finish_run(r1)
    r2 = history.start_run()
    snapshot(r2, [cp("beta", risk="none")])
    history.mark_degraded(r2, ["resolve", "research"])
    history.finish_run(r2, degraded=True)

    changes = history.diff(r2, r1)
    assert len(by_kind(changes, "degraded")) == 2
    assert by_kind(changes, "appeared") == []
    assert by_kind(changes, "disappeared") == []


def test_healthy_run_reports_risk_normally():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme", risk="none")])
    history.finish_run(r1)
    r2 = history.start_run()
    snapshot(r2, [cp("acme", risk="high")])
    history.finish_run(r2)
    risk = by_kind(history.diff(r2, r1), "risk")
    assert len(risk) == 1
    assert risk[0]["weight"] == "urgent"


def test_merged_counterparty_is_not_a_departure():
    """The resolver regroups more often than companies actually go away."""
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("aws", display_name="AWS", monthly_spend=400_00),
                  cp("amzn", display_name="Amzn AWS", monthly_spend=100_00)])
    history.finish_run(r1)

    r2 = history.start_run()
    merged = cp("amzn", display_name="Amazon.com, Inc.", monthly_spend=500_00)
    merged["member_key_ids"] = ["amzn", "aws"]
    snapshot(r2, [merged])
    history.finish_run(r2)

    changes = history.diff(r2, r1)
    assert by_kind(changes, "disappeared") == []
    merges = by_kind(changes, "merged")
    assert len(merges) == 1
    assert merges[0]["counterparty_id"] == "aws"
    assert "Amazon.com, Inc." in merges[0]["headline"]


def test_a_real_departure_is_still_reported():
    setup_module()
    r1 = history.start_run()
    snapshot(r1, [cp("acme"), cp("gone")])
    history.finish_run(r1)
    r2 = history.start_run()
    snapshot(r2, [cp("acme")])
    history.finish_run(r2)
    changes = history.diff(r2, r1)
    assert [c["counterparty_id"] for c in by_kind(changes, "disappeared")] == ["gone"]
    assert by_kind(changes, "merged") == []
