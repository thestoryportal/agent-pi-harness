import threading
from datetime import datetime, timezone

from apps.observe.db import (
    init_db,
    insert_event,
    query_events,
    get_event,
    delete_before,
    vacuum,
    get_max_id,
    get_events_since_id,
)


def test_init_creates_wal_db(tmp_path):
    db_path = tmp_path / "events.db"
    conn = init_db(db_path)
    mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
    assert mode == "wal"
    conn.close()


def test_insert_and_query_roundtrip(tmp_path):
    db_path = tmp_path / "events.db"
    init_db(db_path)
    row_id = insert_event(
        event_type="PreToolUse",
        session_id="sess-001",
        timestamp="2026-04-12T00:00:00Z",
        hook_name="pre_tool_use.py",
        exit_code=0,
        payload='{"tool": "Bash"}',
        duration_ms=12,
        db_path=db_path,
    )
    assert row_id == 1
    events = query_events(db_path=db_path)
    assert len(events) == 1
    assert events[0]["event_type"] == "PreToolUse"
    assert events[0]["session_id"] == "sess-001"
    assert events[0]["payload"] == '{"tool": "Bash"}'
    assert events[0]["duration_ms"] == 12


def test_query_with_filters(tmp_path):
    db_path = tmp_path / "events.db"
    init_db(db_path)
    insert_event("PreToolUse", "s1", "2026-04-12T01:00:00Z", "pre_tool_use.py", 0, db_path=db_path)
    insert_event("PostToolUse", "s1", "2026-04-12T02:00:00Z", "post_tool_use.py", 0, db_path=db_path)
    insert_event("PreToolUse", "s2", "2026-04-12T03:00:00Z", "pre_tool_use.py", 2, db_path=db_path)

    by_type = query_events(event_type="PreToolUse", db_path=db_path)
    assert len(by_type) == 2

    by_session = query_events(session_id="s2", db_path=db_path)
    assert len(by_session) == 1

    by_since = query_events(since="2026-04-12T02:00:00Z", db_path=db_path)
    assert len(by_since) == 2


def test_query_limit_offset(tmp_path):
    db_path = tmp_path / "events.db"
    init_db(db_path)
    for i in range(10):
        insert_event("Test", "s1", f"2026-04-12T{i:02d}:00:00Z", "test.py", 0, db_path=db_path)

    page1 = query_events(limit=3, offset=0, db_path=db_path)
    assert len(page1) == 3
    page2 = query_events(limit=3, offset=3, db_path=db_path)
    assert len(page2) == 3
    assert page1[0]["id"] != page2[0]["id"]


def test_delete_before_cutoff(tmp_path):
    db_path = tmp_path / "events.db"
    init_db(db_path)
    insert_event("Old", "s1", "2026-04-01T00:00:00Z", "test.py", 0, db_path=db_path)
    insert_event("New", "s1", "2026-04-12T00:00:00Z", "test.py", 0, db_path=db_path)

    deleted = delete_before("2026-04-10T00:00:00Z", db_path=db_path)
    assert deleted == 1
    remaining = query_events(db_path=db_path)
    assert len(remaining) == 1
    assert remaining[0]["event_type"] == "New"


def test_vacuum(tmp_path):
    db_path = tmp_path / "events.db"
    init_db(db_path)
    insert_event("Test", "s1", "2026-04-12T00:00:00Z", "test.py", 0, db_path=db_path)
    delete_before("2026-04-13T00:00:00Z", db_path=db_path)
    vacuum(db_path=db_path)
    events = query_events(db_path=db_path)
    assert len(events) == 0


def test_concurrent_writes(tmp_path):
    db_path = tmp_path / "events.db"
    init_db(db_path)
    errors = []

    def writer(thread_id):
        try:
            for i in range(10):
                insert_event(
                    f"Thread{thread_id}",
                    f"s-{thread_id}",
                    f"2026-04-12T00:{thread_id:02d}:{i:02d}Z",
                    "test.py",
                    0,
                    db_path=db_path,
                )
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=writer, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(errors) == 0
    events = query_events(limit=200, db_path=db_path)
    assert len(events) == 100


def test_get_event(tmp_path):
    db_path = tmp_path / "events.db"
    init_db(db_path)
    row_id = insert_event("Test", "s1", "2026-04-12T00:00:00Z", "test.py", 0, db_path=db_path)
    event = get_event(row_id, db_path=db_path)
    assert event is not None
    assert event["event_type"] == "Test"
    assert get_event(9999, db_path=db_path) is None


def test_get_max_id_and_since(tmp_path):
    db_path = tmp_path / "events.db"
    init_db(db_path)
    assert get_max_id(db_path=db_path) == 0
    insert_event("A", "s1", "2026-04-12T00:00:00Z", "test.py", 0, db_path=db_path)
    insert_event("B", "s1", "2026-04-12T01:00:00Z", "test.py", 0, db_path=db_path)
    assert get_max_id(db_path=db_path) == 2
    new = get_events_since_id(1, db_path=db_path)
    assert len(new) == 1
    assert new[0]["event_type"] == "B"
