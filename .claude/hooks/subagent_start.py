#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""SubagentStart hook: log subagent initialization."""

import json, os, sys
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    from _base import Logger, emit_event, handle_health_check, read_stdin, run_hook
except Exception:
    import sys; sys.exit(2)

HOOK_NAME = "subagent_start.py"
handle_health_check(HOOK_NAME)

def main():
    import time
    logger = Logger("subagent_start")
    start_time = time.monotonic()

    d = read_stdin()
    agent_id = d.get("agent_id", "unknown")
    agent_type = d.get("agent_type", "unknown")
    payload = {"agent_id": agent_id, "agent_type": agent_type}
    elapsed = int((time.monotonic() - start_time) * 1000)
    emit_event("SubagentStart", HOOK_NAME, 0, payload, elapsed)
    logger.log(f"SubagentStart: {agent_id} ({agent_type})")
    sys.exit(0)

if __name__ == "__main__":
    run_hook(main, HOOK_NAME, event_type="SubagentStart")
