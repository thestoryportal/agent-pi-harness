#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""PostToolUse hook: validate output, emit metadata event."""

import json, os, sys
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    from _base import Logger, emit_event, handle_health_check, read_stdin, run_hook
except Exception:
    import sys; sys.exit(2)

HOOK_NAME = "post_tool_use.py"
handle_health_check(HOOK_NAME)

def main():
    import time
    logger = Logger("post_tool_use")
    start_time = time.monotonic()

    d = read_stdin()
    tool_name = d.get("tool_name", "")
    tool_output = d.get("tool_output", {})
    tool_exit_code = tool_output.get("exit_code") if isinstance(tool_output, dict) else None
    stdout_preview = str(tool_output.get("stdout", ""))[:500] if isinstance(tool_output, dict) else ""
    payload = {"tool": tool_name, "exit_code": tool_exit_code, "output_preview": stdout_preview}
    elapsed = int((time.monotonic() - start_time) * 1000)
    emit_event("PostToolUse", HOOK_NAME, 0, payload, elapsed)
    logger.log(f"PostToolUse: {tool_name} (exit={tool_exit_code})")
    sys.exit(0)

if __name__ == "__main__":
    run_hook(main, HOOK_NAME, event_type="PostToolUse")
