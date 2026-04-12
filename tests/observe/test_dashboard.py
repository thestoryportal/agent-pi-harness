import tempfile
from pathlib import Path
from fastapi.testclient import TestClient

from apps.observe.db import init_db


def test_index_html_served():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "events.db"
        init_db(db_path)
        from apps.observe.main import create_app
        app = create_app(db_path=db_path)
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert "ArhuGula Observe" in response.text


def test_api_routes_not_shadowed():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "events.db"
        init_db(db_path)
        from apps.observe.main import create_app
        app = create_app(db_path=db_path)
        client = TestClient(app)
        response = client.get("/api/events")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
