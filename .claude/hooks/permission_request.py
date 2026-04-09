#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""PermissionRequest hook: gate permission escalation requests.

Exit 0 for both allow and deny — the JSON payload communicates the decision.
The runtime ignores stdout on exit 2, so structured deny requires exit 0.
"""

import json, os, sys
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    from _base import Logger, emit_event, handle_health_check, read_stdin, run_hook
except Exception:
    import sys; sys.exit(2)

HOOK_NAME = "permission_request.py"
handle_health_check(HOOK_NAME)

ALLOWED_TOOLS = {"Write", "Edit", "Glob", "Grep"}

ALLOWED_BASH_PREFIXES = ["mkdir", "uv", "find", "grep", "npm", "ls", "chmod", "touch", "mv", "cp", "git"]

def main():
    import time
    logger = Logger("permission_request")
    start_time = time.monotonic()

    d = read_stdin()
    tool_name = d.get("tool_name", "")
    tool_input = d.get("tool_input", {})

    if tool_name in ALLOWED_TOOLS:
        decision = "allow"
    elif tool_name == "Bash":
        command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
        cmd_base = command.strip().split()[0] if command.strip() else ""
        if cmd_base in ALLOWED_BASH_PREFIXES:
            decision = "allow"
        else:
            decision = "block"
    else:
        decision = "block"

    payload = {"tool": tool_name, "decision": decision}
    elapsed = int((time.monotonic() - start_time) * 1000)
    emit_event("PermissionRequest", HOOK_NAME, 0, payload, elapsed)

    if decision == "block":
        logger.log(f"BLOCKED permission: {tool_name}")
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PermissionRequest", "decision": {"behavior": "deny", "message": f"Permission denied: {tool_name}"}}}))
    else:
        logger.log(f"ALLOW permission: {tool_name}")
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PermissionRequest", "decision": {"behavior": "allow"}}}))
    sys.exit(0)

if __name__ == "__main__":
    run_hook(main, HOOK_NAME, security_critical=True, event_type="PermissionRequest")
