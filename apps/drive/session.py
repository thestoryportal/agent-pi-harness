"""Tmux session management — create, list, kill."""

import subprocess


def create_session(name: str) -> bool:
    """Create a detached tmux session."""
    result = subprocess.run(
        ["tmux", "new-session", "-d", "-s", name],
        capture_output=True, text=True,
    )
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
    return result.returncode == 0
