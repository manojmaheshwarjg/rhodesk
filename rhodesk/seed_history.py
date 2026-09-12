"""Give the history layer something to compare.

Runs the desk twice: once reading the ledger as it stood N days ago, once
reading it as it stands now. Both are real runs through the real pipeline.
Nothing is fabricated, the ledger is simply read at two moments, which is what
would happen on its own if you left the desk running for a week.

    python seed_history.py          # 7 days apart
    python seed_history.py 14

Only meaningful with RHO_MODE=fixtures. Against a live Rho account the ledger
moves on its own and this is unnecessary.
"""
from __future__ import annotations

import sys

from rhodesk import config, db, pipeline


def main(days: int = 7) -> None:
    if config.RHO_MODE != "fixtures":
        print("RHO_MODE is not 'fixtures'; a live ledger moves on its own.")
        return

    db.init()
    print(f"Seeding two runs {days} days apart.\n")

    for offset in (days, 0):
        config.FIXTURE_DAYS_AGO = offset
        label = f"{offset} days ago" if offset else "today"
        print(f"--- reading the ledger as of {label} ---")
        result = pipeline.run_desk(
            lambda stage, detail: print(f"    {stage}: {detail}") if detail else None)
        print(f"    run {result['run_id']}: {result['companies']} counterparties, "
              f"{result['signals']} signals, {result['changes']} changes"
              + (f", DEGRADED ({', '.join(result['degraded'])})" if result["degraded"] else "")
              + "\n")

    config.FIXTURE_DAYS_AGO = 0


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
