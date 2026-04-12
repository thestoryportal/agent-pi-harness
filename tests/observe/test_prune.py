import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from apps.observe.db import init_db, insert_event, query_events


def test_prune_sqlite_deletes_old_events(tmp_path):
    db_path = tmp_path / "apps" / "observe" / "events.db"
    db_path.parent.mkdir(parents=True)
    init_db(db_path)

    # Insert old and new events
    insert_event("Old", "s1", "2026-04-01T00:00:00+00:00", "test.py", 0, db_path=db_path)
    insert_event("New", "s1", "2026-04-12T00:00:00+00:00", "test.py", 0, db_path=db_path)

    from apps.observe.prune import prune_sqlite
    cutoff = datetime(2026, 4, 10, tzinfo=timezone.utc)
    prune_sqlite(cutoff, db_path)

    events = query_events(db_path=db_path)
    assert len(events) == 1
    assert events[0]["event_type"] == "New"


def test_prune_jsonl_still_works(tmp_path):
    logs_dir = tmp_path / ".claude" / "logs"
    logs_dir.mkdir(parents=True)
    events_file = logs_dir / "events.jsonl"

    old_event = {"event_type": "Old", "timestamp": "2026-04-01T00:00:00+00:00"}
    new_event = {"event_type": "New", "timestamp": "2026-04-12T00:00:00+00:00"}
    events_file.write_text(json.dumps(old_event) + "\n" + json.dumps(new_event) + "\n")

    with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(tmp_path), "OBSERVE_RETENTION_DAYS": "7"}):
        from apps.observe.prune import main
        main()

    content = events_file.read_text().strip()
    lines = [json.loads(l) for l in content.split("\n") if l.strip()]
    assert len(lines) == 1
    assert lines[0]["event_type"] == "New"


def test_prune_both_sources(tmp_path):
    # Set up SQLite
    db_path = tmp_path / "apps" / "observe" / "events.db"
    db_path.parent.mkdir(parents=True)
    init_db(db_path)
    insert_event("OldDB", "s1", "2026-04-01T00:00:00+00:00", "test.py", 0, db_path=db_path)
    insert_event("NewDB", "s1", "2026-04-12T00:00:00+00:00", "test.py", 0, db_path=db_path)

    # Set up JSONL
    logs_dir = tmp_path / ".claude" / "logs"
    logs_dir.mkdir(parents=True)
    events_file = logs_dir / "events.jsonl"
    old_event = {"event_type": "OldJSONL", "timestamp": "2026-04-01T00:00:00+00:00"}
    new_event = {"event_type": "NewJSONL", "timestamp": "2026-04-12T00:00:00+00:00"}
    events_file.write_text(json.dumps(old_event) + "\n" + json.dumps(new_event) + "\n")

    with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(tmp_path), "OBSERVE_RETENTION_DAYS": "7"}):
        from apps.observe.prune import main
        main()

    # Check SQLite
    db_events = query_events(db_path=db_path)
    assert len(db_events) == 1
    assert db_events[0]["event_type"] == "NewDB"

    # Check JSONL
    content = events_file.read_text().strip()
    lines = [json.loads(l) for l in content.split("\n") if l.strip()]
    assert len(lines) == 1
    assert lines[0]["event_type"] == "NewJSONL"
