"""Tmux session management — create, list, kill."""

import json
import os
import subprocess
from datetime import datetime, timezone


def _emit_observe(event_type: str, payload: dict) -> None:
    """Emit lifecycle event to Observe SQLite. Silently skips if unavailable."""
    try:
        from apps.observe.db import insert_event
        session_id = os.environ.get("ARHUGULA_SESSION_ID", "unknown")
        insert_event(
            event_type=event_type,
            session_id=session_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            hook_name="drive",
            exit_code=0 if event_type == "session.spawned" else 1,
            payload=json.dumps(payload),
        )
    except Exception:
        pass


def create_session(name: str) -> bool:
    """Create a detached tmux session."""
    result = subprocess.run(
        ["tmux", "new-session", "-d", "-s", name],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        _emit_observe("session.spawned", {"tmux_session": name})
    return result.returncode == 0


def list_sessions() -> list[str]:
    """List active tmux session names."""
    result = subprocess.run(
        ["tmux", "list-sessions", "-F", "#{session_name}"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return []
    return [s.strip() for s in result.stdout.strip().split("\n") if s.strip()]


def kill_session(name: str) -> bool:
    """Kill a tmux session by name."""
    result = subprocess.run(
        ["tmux", "kill-session", "-t", name],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        _emit_observe("session.failed", {"tmux_session": name, "reason": "killed"})
    return result.returncode == 0
