"""SQLite store. One row per counterparty is the whole idea, so that is the
central table; signals and calls hang off it."""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from typing import Any, Iterable

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS counterparties (
    id                TEXT PRIMARY KEY,
    display_name      TEXT NOT NULL,
    aliases           TEXT NOT NULL DEFAULT '[]',
    domain            TEXT,
    sector            TEXT,
    resolution_note   TEXT,
    money_in          INTEGER NOT NULL DEFAULT 0,
    money_out         INTEGER NOT NULL DEFAULT 0,
    txn_count         INTEGER NOT NULL DEFAULT 0,
    open_invoices     INTEGER NOT NULL DEFAULT 0,
    outstanding       INTEGER NOT NULL DEFAULT 0,
    oldest_days       INTEGER,
    ar_share          REAL NOT NULL DEFAULT 0,
    recurring         INTEGER NOT NULL DEFAULT 0,
    duplicate         INTEGER NOT NULL DEFAULT 0,
    monthly_spend     INTEGER NOT NULL DEFAULT 0,
    posture           TEXT NOT NULL DEFAULT 'watch',
    recommendation    TEXT,
    rationale         TEXT,
    risk              TEXT NOT NULL DEFAULT 'none',
    contact_name      TEXT,
    contact_phone     TEXT,
    contact_email     TEXT,
    invoices          TEXT NOT NULL DEFAULT '[]',
    researched_at     TEXT,
    demo              INTEGER NOT NULL DEFAULT 0,
    first_seen_run    INTEGER,
    last_seen_run     INTEGER,
    first_seen_at     TEXT
);

CREATE TABLE IF NOT EXISTS signals (
    id              TEXT PRIMARY KEY,
    counterparty_id TEXT NOT NULL,
    severity        TEXT NOT NULL,
    title           TEXT NOT NULL,
    detail          TEXT,
    source_url      TEXT,
    source_name     TEXT,
    observed_at     TEXT,
    first_seen_run  INTEGER,
    last_seen_run   INTEGER,
    first_seen_at   TEXT,
    last_seen_at    TEXT,
    FOREIGN KEY (counterparty_id) REFERENCES counterparties(id)
);

CREATE TABLE IF NOT EXISTS calls (
    id               TEXT PRIMARY KEY,
    counterparty_id  TEXT NOT NULL,
    posture          TEXT,
    state            TEXT NOT NULL,
    to_number        TEXT,
    brief            TEXT NOT NULL DEFAULT '{}',
    transcript       TEXT NOT NULL DEFAULT '[]',
    outcome          TEXT NOT NULL DEFAULT '{}',
    provider_ref     TEXT,
    simulated        INTEGER NOT NULL DEFAULT 0,
    created_at       TEXT,
    ended_at         TEXT,
    sim_plan         TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (counterparty_id) REFERENCES counterparties(id)
);

CREATE TABLE IF NOT EXISTS runs (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at     TEXT,
    finished_at    TEXT,
    status         TEXT NOT NULL DEFAULT 'running',
    mode           TEXT,
    counterparties INTEGER NOT NULL DEFAULT 0,
    signals        INTEGER NOT NULL DEFAULT 0,
    new_signals    INTEGER NOT NULL DEFAULT 0,
    change_count   INTEGER NOT NULL DEFAULT 0,
    degraded       INTEGER NOT NULL DEFAULT 0,
    degraded_stages TEXT NOT NULL DEFAULT '',
    note           TEXT
);

CREATE TABLE IF NOT EXISTS run_events (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id  INTEGER,
    at      TEXT,
    stage   TEXT,
    detail  TEXT
);

-- One row per counterparty per run. This is what makes a delta possible:
-- without it every run is a fresh snapshot and nothing can be compared.
CREATE TABLE IF NOT EXISTS counterparty_history (
    run_id          INTEGER NOT NULL,
    counterparty_id TEXT NOT NULL,
    captured_at     TEXT,
    display_name    TEXT,
    domain          TEXT,
    posture         TEXT,
    risk            TEXT,
    outstanding     INTEGER NOT NULL DEFAULT 0,
    open_invoices   INTEGER NOT NULL DEFAULT 0,
    oldest_days     INTEGER,
    monthly_spend   INTEGER NOT NULL DEFAULT 0,
    money_in        INTEGER NOT NULL DEFAULT 0,
    money_out       INTEGER NOT NULL DEFAULT 0,
    txn_count       INTEGER NOT NULL DEFAULT 0,
    ar_share        REAL NOT NULL DEFAULT 0,
    recurring       INTEGER NOT NULL DEFAULT 0,
    duplicate       INTEGER NOT NULL DEFAULT 0,
    signal_count    INTEGER NOT NULL DEFAULT 0,
    member_keys     TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (run_id, counterparty_id)
);

-- The diff, computed once when a run finishes and stored, so the briefing is
-- a read and "what changed last Tuesday" stays answerable.
CREATE TABLE IF NOT EXISTS changes (
    id              TEXT PRIMARY KEY,
    run_id          INTEGER NOT NULL,
    prev_run_id     INTEGER,
    at              TEXT,
    kind            TEXT NOT NULL,
    weight          TEXT NOT NULL DEFAULT 'info',
    counterparty_id TEXT,
    display_name    TEXT,
    headline        TEXT NOT NULL,
    detail          TEXT,
    from_value      TEXT,
    to_value        TEXT,
    amount          INTEGER,
    source_url      TEXT
);

"""

INDEXES = """
CREATE INDEX IF NOT EXISTS idx_signals_cp ON signals(counterparty_id);
CREATE INDEX IF NOT EXISTS idx_calls_cp ON calls(counterparty_id);
CREATE INDEX IF NOT EXISTS idx_hist_run ON counterparty_history(run_id);
CREATE INDEX IF NOT EXISTS idx_changes_run ON changes(run_id);
CREATE INDEX IF NOT EXISTS idx_signals_seen ON signals(last_seen_run);
"""

JSON_COLUMNS = {
    "counterparties": {"aliases", "invoices"},
    "signals": set(),
    "calls": {"brief", "transcript", "outcome", "sim_plan"},
}


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(config.DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


@contextmanager
def cursor():
    conn = connect()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


# Columns added after the first version shipped. A database created before
# them is migrated in place rather than thrown away, because the history it
# holds is the point.
_ADDED_COLUMNS = {
    "counterparties": {
        "first_seen_run": "INTEGER",
        "last_seen_run": "INTEGER",
        "first_seen_at": "TEXT",
    },
    "runs": {
        "degraded": "INTEGER NOT NULL DEFAULT 0",
        "degraded_stages": "TEXT NOT NULL DEFAULT ''",
    },
    "counterparty_history": {
        "member_keys": "TEXT NOT NULL DEFAULT ''",
    },
    "signals": {
        "first_seen_run": "INTEGER",
        "last_seen_run": "INTEGER",
        "first_seen_at": "TEXT",
        "last_seen_at": "TEXT",
    },
}


def _migrate(conn: sqlite3.Connection) -> None:
    def columns(table: str) -> set[str]:
        return {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}

    # `runs` used to be a stage log. It is now the run record, and the stage
    # log moved to run_events. The old rows were progress chatter, so dropping
    # them costs nothing.
    if "stage" in columns("runs"):
        conn.execute("DROP TABLE runs")
        conn.executescript(
            [stmt for stmt in SCHEMA.split(";")
             if "CREATE TABLE IF NOT EXISTS runs" in stmt][0] + ";")

    for table, wanted in _ADDED_COLUMNS.items():
        have = columns(table)
        for name, decl in wanted.items():
            if name not in have:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {name} {decl}")


def init() -> None:
    with cursor() as conn:
        conn.executescript(SCHEMA)
        _migrate(conn)
        conn.executescript(INDEXES)


def reset() -> None:
    """Wipe everything, history included. Only for starting over by hand;
    a run no longer calls this."""
    with cursor() as conn:
        for table in ("signals", "calls", "counterparties", "runs", "run_events",
                      "counterparty_history", "changes"):
            conn.execute(f"DELETE FROM {table}")


def _decode(table: str, row: sqlite3.Row) -> dict:
    out = dict(row)
    for col in JSON_COLUMNS.get(table, set()):
        if out.get(col):
            try:
                out[col] = json.loads(out[col])
            except (json.JSONDecodeError, TypeError):
                out[col] = []
    return out


def _encode(table: str, data: dict) -> dict:
    out = dict(data)
    for col in JSON_COLUMNS.get(table, set()):
        if col in out and not isinstance(out[col], str):
            out[col] = json.dumps(out[col])
    return out


def upsert(table: str, rows: Iterable[dict]) -> None:
    rows = [_encode(table, r) for r in rows]
    if not rows:
        return
    cols = list(dict.fromkeys(k for r in rows for k in r))
    for r in rows:
        for c in cols:
            r.setdefault(c, None)
    placeholders = ",".join("?" for _ in cols)
    assignments = ",".join(f"{c}=excluded.{c}" for c in cols if c != "id")
    sql = (f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders}) "
           f"ON CONFLICT(id) DO UPDATE SET {assignments}")
    with cursor() as conn:
        conn.executemany(sql, [[r[c] for c in cols] for r in rows])


def query(table: str, where: str = "", params: tuple = (), order: str = "") -> list[dict]:
    sql = f"SELECT * FROM {table}"
    if where:
        sql += f" WHERE {where}"
    if order:
        sql += f" ORDER BY {order}"
    with cursor() as conn:
        return [_decode(table, r) for r in conn.execute(sql, params).fetchall()]


def one(table: str, row_id: str) -> dict | None:
    rows = query(table, "id = ?", (row_id,))
    return rows[0] if rows else None


def set_fields(table: str, row_id: str, **fields: Any) -> None:
    if not fields:
        return
    fields = _encode(table, fields)
    sets = ",".join(f"{k}=?" for k in fields)
    with cursor() as conn:
        conn.execute(f"UPDATE {table} SET {sets} WHERE id=?",
                     (*fields.values(), row_id))


def log_run(stage: str, detail: str, run_id: int | None = None) -> None:
    from datetime import datetime, timezone
    with cursor() as conn:
        conn.execute("INSERT INTO run_events (run_id, at, stage, detail) VALUES (?,?,?,?)",
                     (run_id, datetime.now(timezone.utc).isoformat(), stage, detail))


def execute(sql: str, params: tuple = ()) -> None:
    with cursor() as conn:
        conn.execute(sql, params)


def rows(sql: str, params: tuple = ()) -> list[dict]:
    """Escape hatch for the history queries, which join and aggregate in ways
    the table helpers above deliberately do not."""
    with cursor() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]


def scalar(sql: str, params: tuple = ()) -> Any:
    with cursor() as conn:
        row = conn.execute(sql, params).fetchone()
    return row[0] if row else None
