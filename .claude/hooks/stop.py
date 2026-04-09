#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Stop hook: session cleanup, full state capture."""

import json, os, sys
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    from _base import Logger, emit_event, handle_health_check, read_stdin, run_hook
except Exception:
    import sys; sys.exit(2)

HOOK_NAME = "stop.py"
handle_health_check(HOOK_NAME)

def main():
    import time
    logger = Logger("stop")
    start_time = time.monotonic()

    d = read_stdin()
    stop_hook_active = d.get("stop_hook_active", False)
    last_message = d.get("last_assistant_message", "")
    payload = {"stop_hook_active": stop_hook_active, "last_message_preview": last_message[:500]}
    elapsed = int((time.monotonic() - start_time) * 1000)
    emit_event("Stop", HOOK_NAME, 0, payload, elapsed)
    logger.log(f"Stop: active={stop_hook_active}")
    sys.exit(0)

if __name__ == "__main__":
    run_hook(main, HOOK_NAME, event_type="Stop")
