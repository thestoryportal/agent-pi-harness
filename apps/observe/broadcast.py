"""WebSocket broadcaster for real-time event streaming."""

import json
import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class Broadcaster:
    """Manages connected WebSocket clients and broadcasts events."""

    def __init__(self):
        self._clients: set[WebSocket] = set()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self._clients.add(ws)

    def disconnect(self, ws: WebSocket) -> None:
        self._clients.discard(ws)

    async def broadcast(self, event: dict) -> None:
        """Send event to all connected clients. Remove disconnected ones."""
        dead = set()
        message = json.dumps(event)
        for ws in self._clients:
            try:
                await ws.send_text(message)
            except Exception:
                dead.add(ws)
        self._clients -= dead

    @property
    def client_count(self) -> int:
        return len(self._clients)


broadcaster = Broadcaster()
