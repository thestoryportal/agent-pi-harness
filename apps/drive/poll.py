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
    """
    output = capture_pane(session_name)
    return parse_sentinel(output, token)
