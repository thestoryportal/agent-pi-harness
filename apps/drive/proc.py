"""List running Claude Code processes."""

import subprocess


def list_claude_processes() -> list[dict]:
    """List running Claude Code processes with PID and command."""
    result = subprocess.run(
        ["pgrep", "-fl", "claude"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return []
    processes = []
    for line in result.stdout.strip().split("\n"):
        if line.strip():
            parts = line.split(" ", 1)
            processes.append({"pid": parts[0], "command": parts[1] if len(parts) > 1 else ""})
    return processes
