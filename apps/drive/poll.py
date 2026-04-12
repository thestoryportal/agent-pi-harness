"""Poll tmux sessions for Sentinel completion tokens."""

import subprocess

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
    Note: returns None indefinitely for dead sessions (tmux session
    no longer exists). Callers should handle timeout externally.
    """
    output = capture_pane(session_name)
    exit_code = parse_sentinel(output, token)
    if exit_code is not None:
        try:
            from apps.observe.db import emit_observe_event
            emit_observe_event(
                "session.completed", "drive", exit_code,
                {"tmux_session": session_name, "sentinel": f"__DONE_{token}:{exit_code}"},
            )
        except Exception:
            pass
    return exit_code
