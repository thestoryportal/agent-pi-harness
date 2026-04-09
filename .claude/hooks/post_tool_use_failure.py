#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""PostToolUseFailure hook: full traceback capture for debugging."""

import json, os, sys
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    from _base import Logger, emit_event, handle_health_check, read_stdin, run_hook
except Exception:
    import sys; sys.exit(2)

HOOK_NAME = "post_tool_use_failure.py"
handle_health_check(HOOK_NAME)

def main():
    import time
    logger = Logger("post_tool_use_failure")
    start_time = time.monotonic()

    d = read_stdin()
    tool_name = d.get("tool_name", "")
    tool_input = d.get("tool_input", {})
    tool_output = d.get("tool_output", {})
    command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
    error_text = str(tool_output.get("stderr", tool_output))[:1000] if isinstance(tool_output, dict) else str(tool_output)[:1000]
    payload = {"tool": tool_name, "command": command[:500], "error": error_text}
    elapsed = int((time.monotonic() - start_time) * 1000)
    emit_event("PostToolUseFailure", HOOK_NAME, 0, payload, elapsed)
    logger.log(f"FAILURE: {tool_name} — {error_text[:200]}")
    sys.exit(0)

if __name__ == "__main__":
    run_hook(main, HOOK_NAME, event_type="PostToolUseFailure")
