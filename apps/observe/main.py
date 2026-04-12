"""Observe — FastAPI event dashboard server for ArhuGula.

Usage: uv run apps/observe/main.py
"""

import asyncio
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from apps.observe.db import (
    init_db,
    query_events,
    get_event,
    get_max_id,
    get_events_since_id,
)
from apps.observe.broadcast import broadcaster


def create_app(db_path: str | Path | None = None) -> FastAPI:
    """Create the FastAPI app. db_path is configurable for testing."""
    app = FastAPI(title="ArhuGula Observe", version="0.1.0")

    _db_path = Path(db_path) if db_path else Path(__file__).parent / "events.db"

    @app.on_event("startup")
    async def startup():
        init_db(_db_path)
        asyncio.create_task(_poll_loop(_db_path))

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.get("/api/events")
    async def list_events(
        limit: int = Query(default=100, le=1000),
        offset: int = Query(default=0, ge=0),
        event_type: str | None = None,
        session_id: str | None = None,
        since: str | None = None,
    ):
        return query_events(
            limit=limit,
            offset=offset,
            event_type=event_type,
            session_id=session_id,
            since=since,
            db_path=_db_path,
        )

    @app.get("/api/events/{event_id}")
    async def get_single_event(event_id: int):
        event = get_event(event_id, db_path=_db_path)
        if not event:
            return JSONResponse(status_code=404, content={"error": "Event not found"})
        return event

    @app.websocket("/ws")
    async def websocket_endpoint(ws: WebSocket):
        await broadcaster.connect(ws)
        try:
            while True:
                await ws.receive_text()  # keepalive
        except WebSocketDisconnect:
            broadcaster.disconnect(ws)

    # Static files for dashboard — mount AFTER API routes
    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        app.mount("/", StaticFiles(directory=str(static_dir), html=True))

    return app


async def _poll_loop(db_path: Path) -> None:
    """Background task: poll SQLite for new events, broadcast to WS clients."""
    last_id = get_max_id(db_path=db_path)
    while True:
        await asyncio.sleep(1)
        try:
            new_events = get_events_since_id(last_id, db_path=db_path)
            for event in new_events:
                await broadcaster.broadcast(event)
                if event["id"] > last_id:
                    last_id = event["id"]
        except Exception:
            pass  # Transient DB errors should not crash the poll loop


if __name__ == "__main__":
    port = int(os.environ.get("OBSERVE_PORT", "8421"))
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=port)
