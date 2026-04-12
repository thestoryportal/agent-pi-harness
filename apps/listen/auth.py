"""API key authentication middleware for Listen."""

import os
from fastapi import Request
from fastapi.responses import JSONResponse


async def require_api_key(request: Request, call_next):
    """Middleware: require X-API-Key header matching LISTEN_API_KEY env var."""
    expected_key = os.environ.get("LISTEN_API_KEY")
    if not expected_key:
        return JSONResponse(
            status_code=500,
            content={"error": "LISTEN_API_KEY not configured — refusing to serve without auth"},
        )

    provided_key = request.headers.get("X-API-Key")
    if not provided_key:
        return JSONResponse(status_code=401, content={"error": "Missing X-API-Key header"})
    if provided_key != expected_key:
        return JSONResponse(status_code=403, content={"error": "Invalid API key"})

    return await call_next(request)
