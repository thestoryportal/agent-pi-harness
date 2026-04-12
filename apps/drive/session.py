"""Tmux session management — create, list, kill."""

import subprocess


def _emit(event_type: str, exit_code: int, payload: dict) -> None:
    """Emit lifecycle event to Observe. Silently skips if unavailable."""
    try:
        from apps.observe.db import emit_observe_event
        emit_observe_event(event_type, "drive", exit_code, payload)
    except Exception:
        pass


def create_session(name: str) -> bool:
    """Create a detached tmux session."""
    result = subprocess.run(
        ["tmux", "new-session", "-d", "-s", name],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        _emit("session.spawned", 0, {"tmux_session": name})
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
        _emit("session.failed", 0, {"tmux_session": name, "reason": "killed"})
    return result.returncode == 0
