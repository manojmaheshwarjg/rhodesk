"""A sector is a sector, not the name resolver's doubts about the data."""
from __future__ import annotations

import os
import tempfile

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

from rhodesk.pipeline import clean_sector  # noqa: E402


def test_a_hedge_in_brackets_is_dropped():
    assert clean_sector("Retail (Sample Data)") == "Retail"
    assert clean_sector("Consulting (fictional)") == "Consulting"
    assert clean_sector("Logistics (demo company)") == "Logistics"


def test_real_sectors_are_left_alone():
    assert clean_sector("Manufacturing / Software Services") == "Manufacturing / Software Services"
    assert clean_sector("Accounting (Tax & Audit)") == "Accounting (Tax & Audit)"
    assert clean_sector("") == ""
    assert clean_sector(None) == ""
