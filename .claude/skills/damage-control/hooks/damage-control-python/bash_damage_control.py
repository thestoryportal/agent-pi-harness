#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""PreToolUse hook: Bash tool damage control.

Blocks dangerous bash commands and enforces path protection via patterns.yaml.
Adapted from disler/claude-code-damage-control bash-tool-damage-control.py.

Exit codes: 0=allow (or ask via JSON), 2=block.
This is a security-critical hook — never exit 1.
"""

import fnmatch
import json
import os
import re
import shlex
import sys
import time
from pathlib import Path
from typing import Any

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    import yaml
    from _base import Logger, emit_event, handle_health_check, read_stdin, run_hook
except Exception:
    sys.exit(2)

HOOK_NAME = "bash_damage_control.py"
handle_health_check(HOOK_NAME)

PROJECT_ROOT = str(Path(PROJECT_DIR).resolve())


# ============================================================================
# OPERATION PATTERNS — for fine-grained read-only path enforcement
# {path} is replaced with the escaped path at runtime
# ============================================================================

WRITE_PATTERNS = [
    (r'>\s*{path}', "write"),
    (r'\btee\s+(?!.*-a).*{path}', "write"),
]

APPEND_PATTERNS = [
    (r'>>\s*{path}', "append"),
    (r'\btee\s+-a\s+.*{path}', "append"),
    (r'\btee\s+.*-a.*{path}', "append"),
]

EDIT_PATTERNS = [
    (r'\bsed\s+-i.*{path}', "edit"),
    (r'\bperl\s+-[^\s]*i.*{path}', "edit"),
    (r'\bawk\s+-i\s+inplace.*{path}', "edit"),
]

MOVE_COPY_PATTERNS = [
    (r'\bmv\s+.*\s+{path}', "move"),
    (r'\bcp\s+.*\s+{path}', "copy"),
]

DELETE_PATTERNS = [
    (r'\brm\s+.*{path}', "delete"),
    (r'\bunlink\s+.*{path}', "delete"),
    (r'\brmdir\s+.*{path}', "delete"),
    (r'\bshred\s+.*{path}', "delete"),
    (r'\bfind\s+.*{path}.*-delete', "find-delete"),
]

PERMISSION_PATTERNS = [
    (r'\bchmod\s+.*{path}', "chmod"),
    (r'\bchown\s+.*{path}', "chown"),
    (r'\bchgrp\s+.*{path}', "chgrp"),
]

TRUNCATE_PATTERNS = [
    (r'\btruncate\s+.*{path}', "truncate"),
    (r':\s*>\s*{path}', "truncate"),
]

# Combined patterns for read-only paths (block ALL modifications)
READ_ONLY_BLOCKED = (
    WRITE_PATTERNS
    + APPEND_PATTERNS
    + EDIT_PATTERNS
    + MOVE_COPY_PATTERNS
    + DELETE_PATTERNS
    + PERMISSION_PATTERNS
    + TRUNCATE_PATTERNS
)

# Patterns for no-delete paths (block ONLY delete operations)
NO_DELETE_BLOCKED = DELETE_PATTERNS


# ============================================================================
# GLOB PATTERN SUPPORT
# ============================================================================

def is_glob_pattern(pattern: str) -> bool:
    return "*" in pattern or "?" in pattern or "[" in pattern


def glob_to_regex(glob_pattern: str) -> str:
    result = ""
    for char in glob_pattern:
        if char == "*":
            result += r"[^\s/]*"
        elif char == "?":
            result += r"[^\s/]"
        elif char in r"\.^$+{}[]|()":
            result += "\\" + char
        else:
            result += char
    return result


# ============================================================================
# PATH CHECKING
# ============================================================================

def check_path_patterns(
    command: str, path: str, patterns: list[tuple[str, str]], path_type: str
) -> tuple[bool, str]:
    if is_glob_pattern(path):
        glob_regex = glob_to_regex(path)
        for pattern_template, operation in patterns:
            try:
                cmd_prefix = pattern_template.replace("{path}", "")
                if cmd_prefix and re.search(cmd_prefix + glob_regex, command, re.IGNORECASE):
                    return True, f"Blocked: {operation} operation on {path_type} {path}"
            except re.error:
                continue
    else:
        expanded = os.path.expanduser(path)
        escaped_expanded = re.escape(expanded)
        escaped_original = re.escape(path)
        for pattern_template, operation in patterns:
            pattern_expanded = pattern_template.replace("{path}", escaped_expanded)
            pattern_original = pattern_template.replace("{path}", escaped_original)
            try:
                if re.search(pattern_expanded, command) or re.search(pattern_original, command):
                    return True, f"Blocked: {operation} operation on {path_type} {path}"
            except re.error:
                continue
    return False, ""


def is_within_project(path_str: str) -> bool:
    try:
        expanded = os.path.expanduser(os.path.expandvars(path_str))
        resolved = Path(expanded).resolve()
        return resolved == PROJECT_ROOT or resolved.is_relative_to(PROJECT_ROOT)
    except (OSError, ValueError):
        return False


# ============================================================================
# COMMAND CHECKING
# ============================================================================

def split_chained_commands(command: str) -> list[str]:
    """Split a command on shell operators to check each sub-command independently.

    Prevents exclusion bypass via chaining: 'cat .env.example && cat .env'
    """
    # Split on &&, ||, ; and | (pipe) — preserving quoted strings
    parts = []
    try:
        # Use shlex to respect quoting, then rejoin and split on operators
        # Simple approach: split on unquoted operators
        current = []
        in_single = False
        in_double = False
        i = 0
        while i < len(command):
            c = command[i]
            if c == "'" and not in_double:
                in_single = not in_single
            elif c == '"' and not in_single:
                in_double = not in_double
            elif not in_single and not in_double:
                # Check for &&, ||, ;
                if c == ';' or (c == '&' and i + 1 < len(command) and command[i + 1] == '&'):
                    parts.append(''.join(current).strip())
                    current = []
                    if c == '&':
                        i += 1  # skip second &
                    i += 1
                    continue
                elif c == '|':
                    # Double pipe (||) — logical OR, command boundary
                    if i + 1 < len(command) and command[i + 1] == '|':
                        parts.append(''.join(current).strip())
                        current = []
                        i += 2
                        continue
                    # Single pipe (|) — shell pipeline. Round-10 S-01 fix:
                    # the RHS of a pipe is a separate command that must be
                    # checked independently, otherwise an allowlisted LHS
                    # (e.g., `cat .claude/hooks/session_start.py`) exempts
                    # the RHS (e.g., `tee .claude/hooks/pre_tool_use.py`)
                    # from all path-protection checks. The docstring
                    # already said `|` was handled; now the implementation
                    # actually does it.
                    parts.append(''.join(current).strip())
                    current = []
                    i += 1
                    continue
            current.append(c)
            i += 1
        remainder = ''.join(current).strip()
        if remainder:
            parts.append(remainder)
    except Exception:
        parts = [command]
    return parts if parts else [command]


def check_command(command: str, rules: dict[str, Any]) -> tuple[str, str | None]:
    """Check if command should be blocked, ask-gated, or allowed.

    Returns: (decision, reason) where decision is "block", "ask", or "allow".
    Splits chained commands (&&, ||, ;) and checks each sub-command independently
    to prevent exclusion bypass via chaining.
    """
    # Split chained commands and check each independently
    sub_commands = split_chained_commands(command)
    for sub_cmd in sub_commands:
        decision, reason = _check_single_command(sub_cmd, rules)
        if decision != "allow":
            return decision, reason
    return "allow", None


def _check_single_command(command: str, rules: dict[str, Any]) -> tuple[str, str | None]:
    """Check a single (non-chained) command against all rules."""
    # 0. Check exclusions first (allowlist)
    for entry in rules.get("bashToolExclusions", []):
        if re.search(entry["pattern"], command, re.IGNORECASE):
            return "allow", None

    # 1. Check bashToolPatterns (may block or ask)
    # Per-rule case sensitivity: default is IGNORECASE (safer for most
    # commands), but rules may set `case_sensitive: true` to opt out.
    # This is required for rules that distinguish between uppercase and
    # lowercase short flags where the two forms mean different things
    # (e.g., curl -K config vs curl -k insecure). Added in SP14 round-9.
    for item in rules.get("bashToolPatterns", []):
        pattern = item.get("pattern", "")
        reason = item.get("reason", "Blocked by pattern")
        should_ask = item.get("ask", False)
        case_sensitive = item.get("case_sensitive", False)
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            if re.search(pattern, command, flags):
                if should_ask:
                    return "ask", reason
                return "block", f"Blocked: {reason}"
        except re.error:
            continue

    # 2. Check for ANY access to zero-access paths (including reads)
    # Extract path-like tokens from command for glob basename matching
    try:
        cmd_tokens = shlex.split(command)
    except ValueError:
        cmd_tokens = command.split()

    # E1 (SP2 Phase F, 2026-04-13): filter pathExclusions from the
    # zero-access candidates. Tokens whose basename matches a pathExclusion
    # entry (e.g. .env.example) are NOT considered zero-access candidates.
    # Token-level filtering (not command-level) ensures `cat .env .env.example`
    # still blocks on .env because the exclusion only removes the .env.example
    # token from the candidate set, not the whole command.
    exclusion_patterns = rules.get("pathExclusions", [])
    if exclusion_patterns:
        def _matches_exclusion(token: str) -> bool:
            bn_lower = os.path.basename(token).lower()
            try:
                expanded_bn = os.path.basename(os.path.expanduser(token)).lower()
            except (OSError, ValueError):
                expanded_bn = bn_lower
            for excl in exclusion_patterns:
                excl_lower = excl.lower()
                if fnmatch.fnmatch(bn_lower, excl_lower) or fnmatch.fnmatch(expanded_bn, excl_lower):
                    return True
            return False
        cmd_tokens = [t for t in cmd_tokens if not _matches_exclusion(t)]

    token_basenames = [os.path.basename(t) for t in cmd_tokens if t and not t.startswith("-")]

    for zero_path in rules.get("zeroAccessPaths", []):
        if is_glob_pattern(zero_path):
            expanded_zp = os.path.expanduser(zero_path)
            # Check each token's basename against the glob pattern (catches /full/path/to/secret.key)
            for basename in token_basenames:
                if fnmatch.fnmatch(basename.lower(), zero_path.lower()) or fnmatch.fnmatch(basename.lower(), expanded_zp.lower()):
                    return "block", f"Blocked: zero-access pattern {zero_path} (no operations allowed)"
            # Also check full token paths against the glob
            for token in cmd_tokens:
                if fnmatch.fnmatch(os.path.basename(os.path.expanduser(token)).lower(), zero_path.lower()):
                    return "block", f"Blocked: zero-access pattern {zero_path} (no operations allowed)"
        else:
            expanded_zap = os.path.expanduser(zero_path)
            escaped_expanded = re.escape(expanded_zap)
            escaped_original = re.escape(zero_path)
            # E1 (SP2 Phase F, 2026-04-13): non-glob zero-access substring
            # check iterates FILTERED cmd_tokens instead of the raw command
            # string. The previous re.search(command) form had a false-
            # positive on `head .env.example` because the literal `.env`
            # appears as a substring of `.env.example` in the raw command,
            # which fired the zero-access block even though `.env.example`
            # had been removed from the cmd_tokens candidate set by the
            # pathExclusions filter above. Token-level checking is
            # equivalent for all practical cases (a substring match in
            # the raw command string always corresponds to a substring
            # match in some token, since shlex preserves token boundaries
            # exactly) and respects pathExclusions correctly.
            for token in cmd_tokens:
                if re.search(escaped_expanded, token) or re.search(escaped_original, token):
                    return "block", f"Blocked: zero-access path {zero_path} (no operations allowed)"

    # 3. Check for modifications to read-only paths (reads allowed)
    for readonly in rules.get("readOnlyPaths", []):
        blocked, reason = check_path_patterns(command, readonly, READ_ONLY_BLOCKED, "read-only path")
        if blocked:
            return "block", reason

    # 4. Check for deletions on no-delete paths (read/write/edit allowed)
    for no_delete in rules.get("noDeletePaths", []):
        blocked, reason = check_path_patterns(command, no_delete, NO_DELETE_BLOCKED, "no-delete path")
        if blocked:
            return "block", reason

    # 5. Check mv/cp/ln paths are within project
    for cmd in ["mv", "cp", "ln"]:
        match = re.search(rf"\b{cmd}\s+(.+)", command)
        if match:
            try:
                args = shlex.split(match.group(1))
            except ValueError:
                return "block", f"{cmd} unparseable arguments — fail closed"
            paths = [a for a in args if not a.startswith("-")]
            for p in paths:
                if not is_within_project(p):
                    return "block", f"{cmd} path outside project: {p}"
            if cmd == "ln" and paths:
                target = os.path.realpath(os.path.expanduser(paths[0]))
                for zap in rules.get("zeroAccessPaths", []):
                    expanded_zap = os.path.expanduser(zap)
                    if target.startswith(expanded_zap.rstrip("/")) or target == expanded_zap.rstrip("/"):
                        return "block", f"ln target resolves to zero-access path: {zap}"
    return "allow", None


def load_patterns() -> dict:
    patterns_path = Path(PROJECT_DIR) / ".claude" / "skills" / "damage-control" / "patterns.yaml"
    with open(patterns_path) as f:
        return yaml.safe_load(f)


def main():
    logger = Logger("bash_damage_control")
    start_time = time.monotonic()

    input_data = read_stdin()
    if not input_data or "tool_name" not in input_data:
        logger.log("BLOCKED: malformed or empty stdin (fail-closed)")
        emit_event("PreToolUse", HOOK_NAME, 2, {"error": "malformed stdin"})
        sys.exit(2)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only check Bash commands
    if tool_name != "Bash":
        sys.exit(0)

    command = tool_input.get("command", "")
    if not command:
        sys.exit(0)

    try:
        rules = load_patterns()
    except Exception as e:
        logger.log(f"BLOCKED: patterns.yaml load failed — {e} (fail-closed)")
        emit_event("PreToolUse", HOOK_NAME, 2, {"error": f"patterns.yaml: {e}"})
        print(json.dumps({"error": f"patterns.yaml load failed: {e}"}), file=sys.stderr)
        sys.exit(2)

    decision, reason = check_command(command, rules)
    elapsed = int((time.monotonic() - start_time) * 1000)

    payload = {"tool": tool_name, "decision": decision, "command": command[:500]}
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
