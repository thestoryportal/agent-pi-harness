#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""SessionEnd hook: teardown, session duration calculation."""

import json, os, sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    from _base import Logger, emit_event, get_session_id, handle_health_check, read_stdin, run_hook
except Exception:
    import sys; sys.exit(2)

HOOK_NAME = "session_end.py"
handle_health_check(HOOK_NAME)

def main():
    import time
    logger = Logger("session_end")
    start_time = time.monotonic()

    d = read_stdin()
    session_id = get_session_id()

    session_duration_ms = None
    session_meta = Path(PROJECT_DIR) / ".claude" / "logs" / f"session-start-{session_id}.json"
    if session_meta.exists():
        try:
            meta = json.loads(session_meta.read_text())
            started_at = datetime.fromisoformat(meta["started_at"])
            now = datetime.now(timezone.utc)
            session_duration_ms = int((now - started_at).total_seconds() * 1000)
        except (json.JSONDecodeError, KeyError, ValueError):
            logger.log("WARNING: could not compute session duration")

    payload = {"session_id": session_id, "session_duration_ms": session_duration_ms}
    elapsed = int((time.monotonic() - start_time) * 1000)
    emit_event("SessionEnd", HOOK_NAME, 0, payload, elapsed)
    logger.log(f"SessionEnd: {session_id} (duration: {session_duration_ms}ms)")
    sys.exit(0)

if __name__ == "__main__":
    run_hook(main, HOOK_NAME, event_type="SessionEnd")
