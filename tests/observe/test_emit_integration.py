import json
import sqlite3
from pathlib import Path
from unittest.mock import patch, MagicMock

from apps.observe.db import init_db, query_events


def test_emit_writes_to_sqlite_when_db_exists(tmp_path):
    """When events.db exists, emit_event writes to SQLite."""
    db_path = tmp_path / "apps" / "observe" / "events.db"
    db_path.parent.mkdir(parents=True)
    init_db(db_path)

    with patch("_base.DB_PATH", db_path), \
         patch("_base.PROJECT_DIR", str(tmp_path)):
        # Re-import to pick up patched values
        import importlib
        import _base
        importlib.reload(_base)

        _base.DB_PATH = db_path
        _base.emit_event("TestEvent", "test.py", 0, {"key": "value"}, 42)

    events = query_events(db_path=db_path)
    assert len(events) == 1
    assert events[0]["event_type"] == "TestEvent"
    assert events[0]["hook_name"] == "test.py"
    assert events[0]["exit_code"] == 0
    assert '"key": "value"' in events[0]["payload"]
    assert events[0]["duration_ms"] == 42


def test_emit_falls_back_to_jsonl_when_no_db(tmp_path):
    """When events.db doesn't exist, emit_event writes to JSONL."""
    logs_dir = tmp_path / "logs"
    fake_db = tmp_path / "nonexistent" / "events.db"

    with patch("_base.DB_PATH", fake_db), \
         patch("_base.LOGS_DIR", logs_dir):
        import _base
        _base.DB_PATH = fake_db
        _base.LOGS_DIR = logs_dir
        _base.emit_event("FallbackEvent", "test.py", 1)

    jsonl = logs_dir / "events.jsonl"
    assert jsonl.exists()
    line = json.loads(jsonl.read_text().strip())
    assert line["event_type"] == "FallbackEvent"


def test_emit_falls_back_on_sqlite_error(tmp_path):
    """When SQLite INSERT fails, emit_event retries once then falls back to JSONL."""
    db_path = tmp_path / "apps" / "observe" / "events.db"
    db_path.parent.mkdir(parents=True)
    init_db(db_path)
    logs_dir = tmp_path / "logs"

    with patch("_base.DB_PATH", db_path), \
         patch("_base.LOGS_DIR", logs_dir), \
         patch("_base.PROJECT_DIR", str(tmp_path)), \
         patch("apps.observe.db.insert_event", side_effect=sqlite3.OperationalError("database is locked")):
        import _base
        _base.DB_PATH = db_path
        _base.LOGS_DIR = logs_dir
        _base.emit_event("ErrorEvent", "test.py", 2)

    jsonl = logs_dir / "events.jsonl"
    assert jsonl.exists()
    line = json.loads(jsonl.read_text().strip())
    assert line["event_type"] == "ErrorEvent"


def test_emit_import_error_no_retry(tmp_path):
    """On ImportError, emit_event goes directly to JSONL without retry."""
    db_path = tmp_path / "apps" / "observe" / "events.db"
    db_path.parent.mkdir(parents=True)
    db_path.touch()  # File exists but import will fail
    logs_dir = tmp_path / "logs"

    with patch("_base.DB_PATH", db_path), \
         patch("_base.LOGS_DIR", logs_dir), \
         patch("_base.PROJECT_DIR", "/nonexistent/path"):
        import _base
        _base.DB_PATH = db_path
        _base.LOGS_DIR = logs_dir
        _base.PROJECT_DIR = "/nonexistent/path"
        _base.emit_event("ImportFailEvent", "test.py", 0)

    jsonl = logs_dir / "events.jsonl"
    assert jsonl.exists()
    line = json.loads(jsonl.read_text().strip())
    assert line["event_type"] == "ImportFailEvent"
