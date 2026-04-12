"""SQLite event store with WAL mode for ArhuGula Observe.

Canonical schema from spec Section 9.1. WAL mode set at creation (non-negotiable).
PRAGMA busy_timeout=500 on every connection as write-lock backstop.
"""

import json
import os
import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).parent / "events.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type  TEXT    NOT NULL,
    session_id  TEXT    NOT NULL,
    timestamp   TEXT    NOT NULL,
    hook_name   TEXT    NOT NULL,
    exit_code   INTEGER NOT NULL,
    payload     TEXT,
    duration_ms INTEGER
)
"""


def get_connection(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Get a connection with WAL mode and busy_timeout."""
    conn = sqlite3.connect(str(db_path), isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=500")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Initialize the events database. Creates file and table if needed."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection(db_path)
    conn.execute(_SCHEMA)
    return conn


def insert_event(
    event_type: str,
    session_id: str,
    timestamp: str,
    hook_name: str,
    exit_code: int,
    payload: str | None = None,
    duration_ms: int | None = None,
    db_path: Path = DEFAULT_DB_PATH,
) -> int:
    """Insert an event and return the new row id."""
    conn = get_connection(db_path)
    try:
        cursor = conn.execute(
            "INSERT INTO events (event_type, session_id, timestamp, hook_name, exit_code, payload, duration_ms) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (event_type, session_id, timestamp, hook_name, exit_code, payload, duration_ms),
        )
        return cursor.lastrowid
    finally:
        conn.close()


def query_events(
    limit: int = 100,
    offset: int = 0,
    event_type: str | None = None,
    session_id: str | None = None,
    since: str | None = None,
    db_path: Path = DEFAULT_DB_PATH,
) -> list[dict]:
    """Query events with optional filters. Returns list of dicts, newest first."""
    conn = get_connection(db_path)
    try:
        clauses = []
        params: list = []
        if event_type:
            clauses.append("event_type = ?")
            params.append(event_type)
        if session_id:
            clauses.append("session_id = ?")
            params.append(session_id)
        if since:
            clauses.append("timestamp >= ?")
            params.append(since)

        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"SELECT * FROM events {where} ORDER BY id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = conn.execute(sql, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_event(event_id: int, db_path: Path = DEFAULT_DB_PATH) -> dict | None:
    """Get a single event by id."""
    conn = get_connection(db_path)
    try:
        row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def delete_before(cutoff: str, db_path: Path = DEFAULT_DB_PATH) -> int:
    """Delete events older than cutoff timestamp. Returns count deleted."""
    conn = get_connection(db_path)
    try:
        cursor = conn.execute("DELETE FROM events WHERE timestamp < ?", (cutoff,))
        return cursor.rowcount
    finally:
        conn.close()


def vacuum(db_path: Path = DEFAULT_DB_PATH) -> None:
    """Run VACUUM to reclaim disk space. Call separately from delete_before."""
    conn = get_connection(db_path)
    try:
        conn.execute("VACUUM")
    finally:
        conn.close()


def get_session_id() -> str:
    """Resolve session ID using the same priority chain as _base.py.

    CLAUDE_SESSION_ID > ARHUGULA_SESSION_ID > "unknown".
    """
    return os.environ.get("CLAUDE_SESSION_ID") or os.environ.get("ARHUGULA_SESSION_ID") or "unknown"


def emit_observe_event(
    event_type: str,
    hook_name: str,
    exit_code: int,
    payload: dict | None = None,
    duration_ms: int | None = None,
    db_path: Path = DEFAULT_DB_PATH,
) -> None:
    """High-level emit: resolves session_id, serializes payload, inserts.

    Used by Drive and other app-layer code that can't import _base.py.
    Silently skips if DB doesn't exist or insert fails.
    """
    if not db_path.exists():
        return
    try:
        from datetime import datetime, timezone
        insert_event(
            event_type=event_type,
            session_id=get_session_id(),
            timestamp=datetime.now(timezone.utc).isoformat(),
            hook_name=hook_name,
            exit_code=exit_code,
            payload=json.dumps(payload) if payload else None,
            duration_ms=duration_ms,
            db_path=db_path,
        )
    except Exception:
        pass  # Observability failures must never block app operations


def get_max_id(db_path: Path = DEFAULT_DB_PATH) -> int:
    """Get the maximum event id, or 0 if no events."""
    conn = get_connection(db_path)
    try:
        row = conn.execute("SELECT COALESCE(MAX(id), 0) FROM events").fetchone()
        return row[0]
    finally:
        conn.close()


def get_events_since_id(last_id: int, db_path: Path = DEFAULT_DB_PATH) -> list[dict]:
    """Get events with id > last_id, ordered by id ASC (for broadcasting)."""
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            "SELECT * FROM events WHERE id > ? ORDER BY id ASC", (last_id,)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
