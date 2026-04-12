import tempfile
from pathlib import Path
from fastapi.testclient import TestClient

from apps.observe.db import init_db, insert_event


def test_health_endpoint():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "events.db"
        from apps.observe.main import create_app
        app = create_app(db_path=db_path)
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_get_events_empty():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "events.db"
        init_db(db_path)
        from apps.observe.main import create_app
        app = create_app(db_path=db_path)
        client = TestClient(app)
        response = client.get("/api/events")
        assert response.status_code == 200
        assert response.json() == []


def test_get_events_after_insert():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "events.db"
        init_db(db_path)
        insert_event("TestEvent", "s1", "2026-04-12T00:00:00Z", "test.py", 0, db_path=db_path)
        from apps.observe.main import create_app
        app = create_app(db_path=db_path)
        client = TestClient(app)
        response = client.get("/api/events")
        assert response.status_code == 200
        events = response.json()
        assert len(events) == 1
        assert events[0]["event_type"] == "TestEvent"


def test_get_events_with_filters():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "events.db"
        init_db(db_path)
        insert_event("PreToolUse", "s1", "2026-04-12T01:00:00Z", "pre.py", 0, db_path=db_path)
        insert_event("PostToolUse", "s2", "2026-04-12T02:00:00Z", "post.py", 0, db_path=db_path)
        from apps.observe.main import create_app
        app = create_app(db_path=db_path)
        client = TestClient(app)

        response = client.get("/api/events?event_type=PreToolUse")
        assert len(response.json()) == 1

        response = client.get("/api/events?session_id=s2")
        assert len(response.json()) == 1


def test_get_single_event():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "events.db"
        init_db(db_path)
        row_id = insert_event("Test", "s1", "2026-04-12T00:00:00Z", "test.py", 0, db_path=db_path)
        from apps.observe.main import create_app
        app = create_app(db_path=db_path)
        client = TestClient(app)
        response = client.get(f"/api/events/{row_id}")
        assert response.status_code == 200
        assert response.json()["event_type"] == "Test"


def test_get_missing_event_404():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "events.db"
        init_db(db_path)
        from apps.observe.main import create_app
        app = create_app(db_path=db_path)
        client = TestClient(app)
        response = client.get("/api/events/9999")
        assert response.status_code == 404
