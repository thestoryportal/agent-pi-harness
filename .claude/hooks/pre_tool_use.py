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
  - mcp__claude_in_chrome__* — blocks arbitrary-JS primitives (execute_script,
    eval) because Chrome MCP tools run against the user's real browser session
    (cookies, localStorage, authenticated identities) with no other hook
    coverage. SP14 added claude-bowser which depends on these tools.

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
# CHROME MCP TOOL GATES (SP14 hardening)
# ============================================================================
# claude-bowser drives the user's real Chrome via mcp__claude_in_chrome__*
# tools. These tools are NOT covered by bash_damage_control.py because
# they are MCP-invoked, not Bash-invoked. Any arbitrary-JS primitive reached
# this way has the user's full authenticated identity (Gmail, GitHub,
# banking, etc.). Block execute_script / eval outright.

# Tools that execute arbitrary JavaScript in the browser context —
# always blocked. Matched as the final segment of the tool name so
# variants like `mcp__claude_in_chrome__execute_script` and
# `mcp__claude-in-chrome__execute_script` both resolve.
MCP_CHROME_BLOCKED_SUFFIXES = (
    "execute_script",
    "eval",
    "evaluate",
    "run_script",
    "run_code",
)


def check_mcp_chrome(tool_name: str) -> tuple[str, str | None]:
    """Gate mcp__claude_in_chrome__* tool invocations.

    Blocks any tool whose final name segment is an arbitrary-JS execution
    primitive. All other Chrome MCP tools (navigate, click, screenshot,
    etc.) pass through — they are still logged by post_tool_use so an
    auditor can review the session.
    """
    parts = tool_name.split("__")
    if len(parts) < 2:
        return "allow", None
    suffix = parts[-1].lower()
    if suffix in MCP_CHROME_BLOCKED_SUFFIXES:
        return (
            "block",
            f"Chrome MCP arbitrary-JS primitive blocked: {tool_name}. "
            f"execute_script / eval on the user's real browser session is "
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

    # Chrome MCP tools: gate arbitrary-JS primitives BEFORE the catch-all
    # early exit. Other Chrome MCP tools pass through as log-only.
    if tool_name.startswith("mcp__claude_in_chrome") or tool_name.startswith("mcp__claude-in-chrome"):
        decision, reason = check_mcp_chrome(tool_name)
        elapsed = int((time.monotonic() - start_time) * 1000)
        payload = {"tool": tool_name, "decision": decision}
        if reason:
            payload["reason"] = reason
        if decision == "block":
            emit_event("PreToolUse", HOOK_NAME, 2, payload, elapsed)
            logger.log(f"BLOCKED: {tool_name} — {reason}")
            print(json.dumps({"error": reason}), file=sys.stderr)
            sys.exit(2)
        emit_event("PreToolUse", HOOK_NAME, 0, payload, elapsed)
        logger.log(f"ALLOW: {tool_name}")
        sys.exit(0)

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
