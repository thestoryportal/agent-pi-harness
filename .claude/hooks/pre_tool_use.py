#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""PreToolUse hook: Read/Glob/Grep zero-access protection + MCP gates (catch-all).

Bash, Edit, and Write tools are handled by their own per-tool hooks
(bash_damage_control.py, edit_damage_control.py, write_damage_control.py).
This hook catches:
  - Read, Glob, Grep — blocks access to zeroAccessPaths
  - mcp__* (ALL namespaces) — blocks arbitrary-JS primitives (execute_script,
    eval, run_code, run_script, evaluate) regardless of MCP server namespace.
    SP14 round-3 extended the gate from only mcp__claude_in_chrome__* to all
    mcp__* tools after a security review found that a second Chrome MCP
    server under a different namespace could bypass the original gate.
    All segments of the tool name are checked, not just the last, to defeat
    depth-3 bypasses like mcp__claude_in_chrome__execute_script__v2.

Exit codes: 0=allow, 2=block. This is a security-critical hook — never exit 1.
"""

import fnmatch
import json
import os
import sys
import time
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    import yaml
    from _base import Logger, emit_event, handle_health_check, read_stdin, run_hook
except Exception:
    sys.exit(2)

HOOK_NAME = "pre_tool_use.py"
handle_health_check(HOOK_NAME)

PROJECT_ROOT = str(Path(PROJECT_DIR).resolve())


def is_glob_pattern(pattern: str) -> bool:
    return "*" in pattern or "?" in pattern or "[" in pattern


def match_path(file_path: str, pattern: str) -> bool:
    """Match file path against pattern, supporting prefix, glob, and relative patterns."""
    expanded_pattern = os.path.expanduser(pattern)
    normalized = os.path.normpath(file_path)
    expanded_normalized = os.path.expanduser(normalized)

    # Resolve relative patterns against project root
    if not os.path.isabs(expanded_pattern):
        abs_pattern = os.path.normpath(os.path.join(PROJECT_ROOT, expanded_pattern))
    else:
        abs_pattern = os.path.normpath(expanded_pattern)

    if is_glob_pattern(pattern):
        basename = os.path.basename(expanded_normalized)
        basename_lower = basename.lower()
        pattern_lower = pattern.lower()
        expanded_pattern_lower = expanded_pattern.lower()
        if fnmatch.fnmatch(basename_lower, expanded_pattern_lower):
            return True
        if fnmatch.fnmatch(basename_lower, pattern_lower):
            return True
        if fnmatch.fnmatch(expanded_normalized.lower(), expanded_pattern_lower):
            return True
        abs_pattern_lower = abs_pattern.lower()
        if fnmatch.fnmatch(expanded_normalized.lower(), abs_pattern_lower):
            return True
        return False
    else:
        if expanded_normalized.startswith(expanded_pattern) or expanded_normalized == expanded_pattern.rstrip("/"):
            return True
        if expanded_normalized.startswith(abs_pattern) or expanded_normalized == abs_pattern.rstrip("/"):
            return True
        return False


def check_read(tool_input: dict, rules: dict) -> tuple[str, str | None]:
    """Check Read/Glob/Grep tool inputs against zeroAccessPaths."""
    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
    pattern = tool_input.get("pattern", "")
    check_str = file_path or pattern
    if not check_str:
        return "allow", None

    for zero_path in rules.get("zeroAccessPaths", []):
        if match_path(check_str, zero_path):
            return "block", f"Read/search of protected path: {zero_path}"

    return "allow", None


# ============================================================================
# MCP TOOL GATES (SP14 round-3 hardening — namespace-agnostic)
# ============================================================================
# Any MCP tool (regardless of server namespace) whose name contains an
# arbitrary-JS execution primitive as a segment is blocked. The original
# SP14 hardening gated only mcp__claude_in_chrome__* tools; round-2 review
# found two bypasses:
#   1. Any other MCP server namespace exposing execute_script evaded the gate.
#   2. Depth-3 tool names like mcp__claude_in_chrome__execute_script__v2
#      had a final segment of "v2" which didn't match the blocked-suffix list.
# Round-3 fix: check EVERY segment of the tool name, not just the last, and
# apply the check to ALL mcp__* tools, not just the claude_in_chrome namespace.

# Segments in a tool name that indicate arbitrary JavaScript execution
# against a live browser. Matched case-insensitively against ANY segment
# of the tool name (not just the final one).
MCP_JS_EXEC_SEGMENTS = frozenset({
    "execute_script",
    "eval",
    "evaluate",
    "run_script",
    "run_code",
})


def check_mcp_tool(tool_name: str) -> tuple[str, str | None]:
    """Gate mcp__* tool invocations (all namespaces).

    Blocks any tool whose name contains an arbitrary-JS execution primitive
    as ANY segment. Passive Chrome MCP tools (navigate, click, screenshot,
    snapshot, etc.) pass through — they are still logged by post_tool_use
    so an auditor can review the session.
    """
    segments = [seg.lower() for seg in tool_name.split("__")]
    for seg in segments:
        if seg in MCP_JS_EXEC_SEGMENTS:
            return (
                "block",
                f"MCP arbitrary-JS primitive blocked: {tool_name}. "
                f"execute_script / eval against a live browser session is "
                f"an identity-exfiltration vector and has no allowlist.",
            )
    return "allow", None


def load_patterns() -> dict:
    patterns_path = Path(PROJECT_DIR) / ".claude" / "hooks" / "patterns.yaml"
    with open(patterns_path) as f:
        return yaml.safe_load(f)


def main():
    logger = Logger("pre_tool_use")
    start_time = time.monotonic()

    input_data = read_stdin()
    if not input_data or "tool_name" not in input_data:
        logger.log("BLOCKED: malformed or empty stdin (fail-closed)")
        emit_event("PreToolUse", HOOK_NAME, 2, {"error": "malformed stdin"})
        sys.exit(2)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # MCP tools (all namespaces): gate arbitrary-JS primitives BEFORE the
    # catch-all early exit. Only emit-and-exit if the tool is actually
    # blocked; passive MCP tools fall through to the catch-all early exit.
    if tool_name.startswith("mcp__"):
        decision, reason = check_mcp_tool(tool_name)
        if decision == "block":
            elapsed = int((time.monotonic() - start_time) * 1000)
            payload = {"tool": tool_name, "decision": decision, "reason": reason}
            emit_event("PreToolUse", HOOK_NAME, 2, payload, elapsed)
            logger.log(f"BLOCKED: {tool_name} — {reason}")
            print(json.dumps({"error": reason}), file=sys.stderr)
            sys.exit(2)
        # Passive MCP tools are allowed and logged via post_tool_use;
        # fall through to the catch-all early exit below.

    # Only handle Read, Glob, Grep — other tools have their own hooks
    if tool_name not in ("Read", "Glob", "Grep"):
        sys.exit(0)

    try:
        rules = load_patterns()
    except Exception as e:
        logger.log(f"BLOCKED: patterns.yaml load failed — {e} (fail-closed)")
        emit_event("PreToolUse", HOOK_NAME, 2, {"error": f"patterns.yaml: {e}"})
        print(json.dumps({"error": f"patterns.yaml load failed: {e}"}), file=sys.stderr)
        sys.exit(2)

    decision, reason = check_read(tool_input, rules)
    elapsed = int((time.monotonic() - start_time) * 1000)

    payload = {"tool": tool_name, "decision": decision}
    if reason:
        payload["reason"] = reason

    if decision == "block":
        emit_event("PreToolUse", HOOK_NAME, 2, payload, elapsed)
        logger.log(f"BLOCKED: {tool_name} — {reason}")
        print(json.dumps({"error": reason}), file=sys.stderr)
        sys.exit(2)
    else:
        emit_event("PreToolUse", HOOK_NAME, 0, payload, elapsed)
        logger.log(f"ALLOW: {tool_name}")
        sys.exit(0)


if __name__ == "__main__":
    run_hook(main, HOOK_NAME, security_critical=True, event_type="PreToolUse")
