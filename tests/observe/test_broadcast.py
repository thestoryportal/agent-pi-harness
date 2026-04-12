import asyncio
import json
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from apps.observe.broadcast import Broadcaster


@pytest.mark.asyncio(loop_scope="function")
async def test_broadcaster_connect_disconnect():
    b = Broadcaster()
    ws = AsyncMock()
    await b.connect(ws)
    assert b.client_count == 1
    b.disconnect(ws)
    assert b.client_count == 0


@pytest.mark.asyncio(loop_scope="function")
async def test_broadcaster_sends_to_all_clients():
    b = Broadcaster()
    ws1 = AsyncMock()
    ws2 = AsyncMock()
    await b.connect(ws1)
    await b.connect(ws2)
    await b.broadcast({"event_type": "Test"})
    ws1.send_text.assert_called_once()
    ws2.send_text.assert_called_once()
    msg = json.loads(ws1.send_text.call_args[0][0])
    assert msg["event_type"] == "Test"


@pytest.mark.asyncio(loop_scope="function")
async def test_broadcaster_removes_dead_clients():
    b = Broadcaster()
    ws_alive = AsyncMock()
    ws_dead = AsyncMock()
    ws_dead.send_text.side_effect = Exception("disconnected")
    await b.connect(ws_alive)
    await b.connect(ws_dead)
    assert b.client_count == 2
    await b.broadcast({"event_type": "Test"})
    assert b.client_count == 1


def test_ws_endpoint_connects():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "events.db"
        from apps.observe.main import create_app
        from fastapi.testclient import TestClient
        app = create_app(db_path=db_path)
        client = TestClient(app)
        with client.websocket_connect("/ws") as ws:
            # Connection succeeds — that's the test
            pass
