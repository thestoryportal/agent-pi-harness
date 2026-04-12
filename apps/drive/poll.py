"""Poll tmux sessions for Sentinel completion tokens."""

import json
import os
import subprocess
from datetime import datetime, timezone

from apps.drive.sentinel import parse_sentinel


def capture_pane(session_name: str, lines: int = 500) -> str:
    """Capture the last N lines of a tmux pane."""
    result = subprocess.run(
        ["tmux", "capture-pane", "-t", session_name, "-p", "-S", f"-{lines}"],
        capture_output=True, text=True,
    )
    return result.stdout if result.returncode == 0 else ""


def poll_session(session_name: str, token: str) -> int | None:
    """Poll a session for Sentinel completion.

    Returns exit code (int) if done, None if still running.
    Emits session.completed to Observe when done.
    """
    output = capture_pane(session_name)
    exit_code = parse_sentinel(output, token)
    if exit_code is not None:
        try:
            from apps.observe.db import insert_event
            session_id = os.environ.get("ARHUGULA_SESSION_ID", "unknown")
            insert_event(
                event_type="session.completed",
                session_id=session_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                hook_name="drive",
                exit_code=exit_code,
                payload=json.dumps({
                    "tmux_session": session_name,
                    "sentinel": f"__DONE_{token}:{exit_code}",
                }),
            )
        except Exception:
            pass
    return exit_code
