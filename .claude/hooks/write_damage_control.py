#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""PreToolUse hook: Write tool damage control.

Blocks writes to protected files via zeroAccessPaths, readOnlyPaths, and noDeletePaths.
noDeletePaths trigger ask (overwrite confirmation) rather than block.
Adapted from disler/claude-code-damage-control write-tool-damage-control.py.

Exit codes: 0=allow (or ask via JSON), 2=block.
This is a security-critical hook — never exit 1.
"""

import json
import os
import sys
import time
from pathlib import Path, PurePath
from typing import Any

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    import yaml
    from _base import Logger, emit_event, handle_health_check, read_stdin, run_hook
except Exception:
    sys.exit(2)

HOOK_NAME = "write_damage_control.py"
handle_health_check(HOOK_NAME)

PROJECT_ROOT = str(Path(PROJECT_DIR).resolve())


def is_glob_pattern(pattern: str) -> bool:
    return "*" in pattern or "?" in pattern or "[" in pattern


def match_path(file_path: str, pattern: str) -> bool:
    """Match file path against pattern using path-segment-aware matching.

    SP2 AR1 (2026-04-13): uses pathlib.PurePath.match() instead of
    fnmatch.fnmatch() for glob patterns. PurePath.match() treats `/` as
    a path separator, so `.claude/hooks/*.py` does NOT match
    `.claude/hooks/utils/tts/foo.py`. The prior fnmatch-based form
    over-matched subdirectory files because `*` greedily consumed across
    path boundaries.

    Resolves symlinks to prevent traversal bypass via pre-existing symlinks.
    """
    expanded_pattern = os.path.expanduser(pattern)
    normalized = os.path.normpath(file_path)
    expanded_normalized = os.path.expanduser(normalized)
    # Resolve symlinks to catch traversal (e.g., symlink -> ~/.aws/credentials)
    try:
        resolved = str(Path(expanded_normalized).resolve())
    except (OSError, ValueError):
        resolved = expanded_normalized

    # Resolve relative patterns against project root
    if not os.path.isabs(expanded_pattern):
        abs_pattern = os.path.normpath(os.path.join(PROJECT_ROOT, expanded_pattern))
    else:
        abs_pattern = os.path.normpath(expanded_pattern)

    if is_glob_pattern(pattern):
        # Path-segment-aware glob matching via PurePath.match().
        try:
            if PurePath(expanded_normalized).match(expanded_pattern, case_sensitive=False):
                return True
            if PurePath(expanded_normalized).match(abs_pattern, case_sensitive=False):
                return True
            if PurePath(resolved).match(expanded_pattern, case_sensitive=False):
                return True
            if PurePath(resolved).match(abs_pattern, case_sensitive=False):
                return True
        except ValueError:
            # Invalid pattern — fail closed (return False means no match;
            # the caller's next rule may still block)
            pass
        return False
    else:
        if expanded_normalized.startswith(expanded_pattern) or expanded_normalized == expanded_pattern.rstrip("/"):
            return True
        if expanded_normalized.startswith(abs_pattern) or expanded_normalized == abs_pattern.rstrip("/"):
            return True
        # Also check resolved path (follows symlinks)
        if resolved.startswith(expanded_pattern) or resolved == expanded_pattern.rstrip("/"):
            return True
        if resolved.startswith(abs_pattern) or resolved == abs_pattern.rstrip("/"):
            return True
        return False


def check_path(file_path: str, rules: dict[str, Any]) -> tuple[str, str | None]:
    """Check if file_path is blocked. Returns (decision, reason)."""
    # Check zero-access paths first (no access at all)
    for zero_path in rules.get("zeroAccessPaths", []):
        if match_path(file_path, zero_path):
            return "block", f"Write blocked: zero-access path {zero_path}"

    # Check read-only paths (writes not allowed)
    for readonly in rules.get("readOnlyPaths", []):
        if match_path(file_path, readonly):
            return "block", f"Write blocked: read-only path {readonly}"

    # Check no-delete paths (overwrite triggers ask)
    for no_delete in rules.get("noDeletePaths", []):
        if match_path(file_path, no_delete):
            return "ask", f"Overwriting file in accumulation-only path. Confirm? ({file_path})"

    return "allow", None


def load_patterns() -> dict:
    patterns_path = Path(PROJECT_DIR) / ".claude" / "hooks" / "patterns.yaml"
    with open(patterns_path) as f:
        return yaml.safe_load(f)


def main():
    logger = Logger("write_damage_control")
    start_time = time.monotonic()

    input_data = read_stdin()
    if not input_data or "tool_name" not in input_data:
        logger.log("BLOCKED: malformed or empty stdin (fail-closed)")
        emit_event("PreToolUse", HOOK_NAME, 2, {"error": "malformed stdin"})
        sys.exit(2)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only check Write tool
    if tool_name != "Write":
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    try:
        rules = load_patterns()
    except Exception as e:
        logger.log(f"BLOCKED: patterns.yaml load failed — {e} (fail-closed)")
        emit_event("PreToolUse", HOOK_NAME, 2, {"error": f"patterns.yaml: {e}"})
        print(json.dumps({"error": f"patterns.yaml load failed: {e}"}), file=sys.stderr)
        sys.exit(2)

    decision, reason = check_path(file_path, rules)
    elapsed = int((time.monotonic() - start_time) * 1000)

    payload = {"tool": tool_name, "decision": decision, "file_path": file_path}
    if reason:
        payload["reason"] = reason

    if decision == "ask":
        emit_event("PreToolUse", HOOK_NAME, 0, payload, elapsed)
        logger.log(f"ASK: {tool_name} — {reason}")
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": reason,
            }
        }))
        sys.exit(0)
    elif decision == "block":
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
