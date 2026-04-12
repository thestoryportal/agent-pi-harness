import tempfile
from unittest.mock import patch
from fastapi.testclient import TestClient


@patch.dict("os.environ", {"LISTEN_API_KEY": "test-key", "LISTEN_PORT": "8420"})
def test_create_job():
    from apps.listen.main import create_app
    with tempfile.TemporaryDirectory() as tmp:
        app = create_app(jobs_dir=tmp)
        client = TestClient(app)
        response = client.post(
            "/job",
            json={"command": "echo hello", "args": []},
            headers={"X-API-Key": "test-key"},
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["status"] in ("pending", "running")


@patch.dict("os.environ", {"LISTEN_API_KEY": "test-key"})
def test_list_jobs():
    from apps.listen.main import create_app
    with tempfile.TemporaryDirectory() as tmp:
        app = create_app(jobs_dir=tmp)
        client = TestClient(app)
        headers = {"X-API-Key": "test-key"}
        client.post("/job", json={"command": "cmd1"}, headers=headers)
        client.post("/job", json={"command": "cmd2"}, headers=headers)
        response = client.get("/jobs", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) == 2


@patch.dict("os.environ", {"LISTEN_API_KEY": "test-key"})
def test_get_job():
    from apps.listen.main import create_app
    with tempfile.TemporaryDirectory() as tmp:
        app = create_app(jobs_dir=tmp)
        client = TestClient(app)
        headers = {"X-API-Key": "test-key"}
        create_resp = client.post("/job", json={"command": "cmd1"}, headers=headers)
        job_id = create_resp.json()["id"]
        response = client.get(f"/job/{job_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["command"] == "cmd1"


@patch.dict("os.environ", {"LISTEN_API_KEY": "test-key"})
def test_delete_job():
    from apps.listen.main import create_app
    with tempfile.TemporaryDirectory() as tmp:
        app = create_app(jobs_dir=tmp)
        client = TestClient(app)
        headers = {"X-API-Key": "test-key"}
        create_resp = client.post("/job", json={"command": "cmd1"}, headers=headers)
        job_id = create_resp.json()["id"]
        response = client.delete(f"/job/{job_id}", headers=headers)
        assert response.status_code == 200
