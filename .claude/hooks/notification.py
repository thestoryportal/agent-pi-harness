#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Notification hook: route agent notifications."""

import json, os, sys
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    from _base import Logger, emit_event, handle_health_check, read_stdin, run_hook
except Exception:
    import sys; sys.exit(2)

HOOK_NAME = "notification.py"
handle_health_check(HOOK_NAME)

def main():
    import time
    logger = Logger("notification")
    start_time = time.monotonic()

    d = read_stdin()
    message = d.get("message", "")
    payload = {"message": message[:500]}
    elapsed = int((time.monotonic() - start_time) * 1000)
    emit_event("Notification", HOOK_NAME, 0, payload, elapsed)
    logger.log(f"Notification: {message[:100]}")
    sys.exit(0)

if __name__ == "__main__":
    run_hook(main, HOOK_NAME, event_type="Notification")
