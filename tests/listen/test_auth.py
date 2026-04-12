from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.listen.auth import require_api_key


app = FastAPI()


@app.get("/test")
async def health_endpoint():
    return {"ok": True}


app.middleware("http")(require_api_key)


@patch.dict("os.environ", {"LISTEN_API_KEY": "test-secret-key"})
def test_valid_api_key():
    client = TestClient(app)
    response = client.get("/test", headers={"X-API-Key": "test-secret-key"})
    assert response.status_code == 200


@patch.dict("os.environ", {"LISTEN_API_KEY": "test-secret-key"})
def test_missing_api_key():
    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 401


@patch.dict("os.environ", {"LISTEN_API_KEY": "test-secret-key"})
def test_wrong_api_key():
    client = TestClient(app)
    response = client.get("/test", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 403
