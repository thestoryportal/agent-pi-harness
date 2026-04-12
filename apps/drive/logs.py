"""Tail tmux session output."""

import subprocess


def tail_logs(session_name: str, lines: int = 50) -> str:
    """Get the last N lines of a tmux session."""
    result = subprocess.run(
        ["tmux", "capture-pane", "-t", session_name, "-p", "-S", f"-{lines}"],
        capture_output=True, text=True,
    )
    return result.stdout if result.returncode == 0 else ""
