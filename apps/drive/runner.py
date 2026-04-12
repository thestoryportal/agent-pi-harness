"""Execute commands in tmux sessions with Sentinel wrapping."""

import subprocess

from apps.drive.sentinel import generate_token, wrap_command


def run_command(session_name: str, cmd: str) -> str | None:
    """Run a command in a tmux session with Sentinel wrapping.

    Returns the Sentinel token for polling, or None on failure.
    """
    token = generate_token()
    wrapped = wrap_command(cmd, token)
    result = subprocess.run(
        ["tmux", "send-keys", "-t", session_name, wrapped, "Enter"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    return token


def send_text(session_name: str, text: str) -> bool:
    """Send raw text to a tmux session (no Sentinel wrapping)."""
    result = subprocess.run(
        ["tmux", "send-keys", "-t", session_name, text, "Enter"],
        capture_output=True, text=True,
    )
    return result.returncode == 0
