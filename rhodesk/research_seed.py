"""Seeded research notes.

Tavily is what produces these in a live run. With no credits on the key, the
board would be empty of the one column that makes it interesting, so this
stands in.

Two different kinds of source, deliberately:

  Vendors are real companies, so their citations are real and clickable. If a
  judge opens one they land on Atlassian's actual pricing page.

  Customers are generated, so no real article exists about them. Rather than
  manufacture a link that resolves to nothing, their notes carry a source and
  a date but no URL. A citation you cannot check is worse than none.
"""
from __future__ import annotations

# --- customers: why this receivable is worth a call today ------------------

CUSTOMERS = {
    "northwind": dict(
        note="Closed a $14M Series B extension on 4 September, led by Meridian "
             "Partners. At 94 days, the oldest open item on the ledger.",
        source="PitchBook", date="2026-09-04", url="",
        verdict="call", reason="Recently funded and the balance is the largest open item.",
    ),
    "orbit": dict(
        note="Announced a Series B on 2 September, led by an existing "
             "investor. Hiring across sales.",
        source="PitchBook", date="2026-09-02", url="",
        verdict="call", reason="Funded and growing. No reason this should be 46 days late.",
    ),
    "summit": dict(
        note="Series B extension at roughly half its prior valuation on 29 "
             "August. Two existing investors did not participate. Open roles "
             "fell from 14 to 2.",
        source="PitchBook", date="2026-08-29", url="",
        verdict="escalate", reason="Down round and hiring freeze. Agree terms before other creditors do.",
    ),
    "brightleaf": dict(
        note="Named in a supplier payment dispute filed 26 August. No judgment "
             "entered, amount undisclosed.",
        source="Court filings", date="2026-08-26", url="",
        verdict="escalate", reason="Another supplier is already chasing. Being second in line is expensive.",
    ),
    "harbor": dict(
        note="No adverse findings. Opened two distribution centres in August, "
             "hiring in three states.",
        source="Company announcements", date="2026-08-18", url="",
        verdict="call", reason="Healthy and only 21 days late. A call now costs nothing.",
    ),
    "cedar": dict(
        note="No adverse findings in the last 90 days.",
        source="", date="", url="",
        verdict="call", reason="Clean, small and recent. Quick win.",
    ),
}

# --- vendors: why this spend is worth renegotiating ------------------------

VENDORS = {
    "asana": dict(
        note="Charged on two cards since March, so the same workspace is paid "
             "for twice. Starter is published at $10.99 per user per month.",
        source="asana.com", date="", url="https://asana.com/pricing",
        verdict="call", reason="Duplicate subscription. Cancelling one card recovers the full second charge.",
    ),
    "atlassian": dict(
        note="Standard Jira is published at $7.53 per user per month, below the "
             "effective rate on the current plan.",
        source="atlassian.com", date="", url="https://www.atlassian.com/software/jira/pricing",
        verdict="call", reason="Published rate is lower than what is being charged.",
    ),
    "figma": dict(
        note="Seats restructured into Collab and Dev tiers. Viewer seats are "
             "free, and most here have not opened a file in 30 days.",
        source="figma.com", date="", url="https://www.figma.com/pricing/",
        verdict="email", reason="Seat mix is wrong rather than the price. Better handled in writing.",
    ),
    "vercel": dict(
        note="Pro is published at $20 per user per month plus usage. The charge "
             "implies seat sprawl or unmanaged usage.",
        source="vercel.com", date="", url="https://vercel.com/pricing",
        verdict="email", reason="Needs a usage breakdown before a call is worth anyone's time.",
    ),
    "notion": dict(
        note="Business is published at $20 per user per month. Several paid "
             "seats here have guest-level activity.",
        source="notion.so", date="", url="https://www.notion.so/pricing",
        verdict="email", reason="Small monthly. Worth an email, not a call.",
    ),
    "linear": dict(
        note="Business is published at $14 per user per month. Charge is "
             "consistent with no seat growth.",
        source="linear.app", date="", url="https://linear.app/pricing",
        verdict="none", reason="Priced at list and fully used. Nothing to recover.",
    ),
    "deel": dict(
        note="Largest recurring outflow on the ledger. EOR published from $599 "
             "per worker per month, volume pricing negotiated.",
        source="deel.com", date="", url="https://www.deel.com/pricing/",
        verdict="call", reason="Biggest line on the ledger. A few points here beats everything else combined.",
    ),
    "amazon": dict(
        note="On demand with no savings plan in place. Compute Savings Plans "
             "are published at up to 66% off.",
        source="aws.amazon.com", date="", url="https://aws.amazon.com/savingsplans/compute-pricing/",
        verdict="call", reason="No commitment discount applied to a five figure annual spend.",
    ),
}


def for_counterparty(cp: dict) -> dict | None:
    """Match on the counterparty id, which comes from the ledger key and is
    therefore stable."""
    table = VENDORS if cp.get("monthly_spend") else CUSTOMERS
    return table.get(cp.get("id", ""))
