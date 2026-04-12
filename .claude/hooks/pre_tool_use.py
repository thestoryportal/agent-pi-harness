#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""PreToolUse hook: YAML-driven security rules with three-tier path protection.

Exit codes: 0=allow, 2=block. This is a security-critical hook — never exit 1.
Rules are loaded from patterns.yaml — add new rules there, not here.
"""

import fnmatch
import json
import os
import re
import shlex
import sys
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

PROJECT_ROOT = Path(PROJECT_DIR).resolve()

FLAG_ALIASES = {
    "--recursive": "-r", "--force": "-f", "--verbose": "-v",
    "--interactive": "-i", "--preserve": "-p", "--hard": "--hard",
}


def load_patterns() -> dict:
    patterns_path = Path(PROJECT_DIR) / ".claude" / "hooks" / "patterns.yaml"
    with open(patterns_path, "r") as f:
        return yaml.safe_load(f)


def is_within_project(path_str: str) -> bool:
    try:
        expanded = os.path.expanduser(os.path.expandvars(path_str))
        resolved = Path(expanded).resolve()
        return resolved == PROJECT_ROOT or resolved.is_relative_to(PROJECT_ROOT)
    except (OSError, ValueError):
        return False


def check_path_protection(file_path: str, protected_paths: list[str]) -> bool:
    expanded_file = os.path.expanduser(file_path)
    try:
        resolved_file = str(Path(expanded_file).resolve())
    except (OSError, ValueError):
        resolved_file = expanded_file
    for pattern in protected_paths:
        expanded_pattern = os.path.expanduser(pattern)
        abs_pattern = str(PROJECT_ROOT / expanded_pattern) if not Path(expanded_pattern).is_absolute() else expanded_pattern
        for fp in (file_path, expanded_file, resolved_file):
            if fnmatch.fnmatch(fp, abs_pattern) or fnmatch.fnmatch(fp, expanded_pattern):
                return True
            if abs_pattern.endswith("/") and fp.startswith(abs_pattern):
                return True
            if not abs_pattern.endswith("/") and fp.startswith(abs_pattern):
                return True
    return False


def check_env_pattern(text: str) -> bool:
    return bool(re.search(r"(^|\s|/)\.env(\.\w+)?(\s|$|\"|\')", text))


def normalize_command(command: str) -> str:
    try:
        tokens = shlex.split(command)
    except ValueError:
        return command
    if not tokens:
        return command
    base = os.path.basename(tokens[0])
    if base in ("env", "command") and len(tokens) > 1:
        base = os.path.basename(tokens[1])
        tokens = [base] + tokens[2:]
    else:
        tokens = [base] + tokens[1:]
    normalized = [FLAG_ALIASES.get(t, t) for t in tokens]
    return " ".join(normalized)


def check_bash_exclusions(command: str, exclusions: list[dict]) -> bool:
    for entry in exclusions:
        if re.search(entry["pattern"], command, re.IGNORECASE):
            return True
    return False


def check_bash_patterns(command: str, norm: str, patterns: list[dict]) -> tuple[str, str | None]:
    for entry in patterns:
        if re.search(entry["pattern"], command, re.IGNORECASE) or re.search(entry["pattern"], norm, re.IGNORECASE):
            if entry.get("ask"):
                return "ask", entry["reason"]
            return "block", entry["reason"]
    return "allow", None


def check_bash_command(command: str, rules: dict) -> tuple[str, str | None]:
    if check_bash_exclusions(command, rules.get("bashToolExclusions", [])):
        return "allow", None

    expanded = os.path.expanduser(os.path.expandvars(command))
    zero_paths = rules.get("zeroAccessPaths", [])
    for zap in zero_paths:
        exp_zap = os.path.expanduser(zap)
        if exp_zap in command or exp_zap in expanded or zap in command:
            return "block", f"Access to protected path: {zap}"
    if check_env_pattern(command) or check_env_pattern(expanded):
        return "block", "Access to protected path: .env"

    norm = normalize_command(command)
    result = check_bash_patterns(command, norm, rules.get("bashToolPatterns", []))
    if result[0] != "allow":
        return result

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

    no_delete = rules.get("noDeletePaths", [])
    if no_delete and re.search(r"\brm\s+", command):
        for nd_path in no_delete:
            if nd_path in command or nd_path in expanded:
                return "block", f"Delete blocked in accumulation-only path: {nd_path}"

    return "allow", None


def check_read(tool_input: dict, rules: dict) -> tuple[str, str | None]:
    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
    pattern = tool_input.get("pattern", "")
    check_str = file_path or pattern
    if not check_str:
        return "allow", None
    try:
        resolved = str(Path(os.path.expanduser(check_str)).resolve())
    except (OSError, ValueError):
        resolved = check_str

    zero_paths = rules.get("zeroAccessPaths", [])
    for zap in zero_paths:
        exp_zap = os.path.expanduser(zap)
        if exp_zap in resolved or exp_zap in check_str or zap in check_str:
            return "block", f"Read/search of protected path: {zap}"
    if check_env_pattern(resolved) or check_env_pattern(check_str):
        return "block", "Read/search of protected path: .env"

    return "allow", None


def check_write_edit(tool_name: str, tool_input: dict, rules: dict) -> tuple[str, str | None]:
    file_path = tool_input.get("file_path", "")
    if not file_path:
        return "allow", None
    try:
        resolved = str(Path(os.path.expanduser(file_path)).resolve())
    except (OSError, ValueError):
        return "block", "Write/Edit path unresolvable — fail closed"

    zero_paths = rules.get("zeroAccessPaths", [])
    for zap in zero_paths:
        exp_zap = os.path.expanduser(zap)
        if exp_zap in resolved or exp_zap in file_path or zap in file_path:
            return "block", f"Write/Edit to protected path: {zap}"
    if check_env_pattern(resolved) or check_env_pattern(file_path):
        return "block", "Write/Edit to protected path: .env"

    read_only = rules.get("readOnlyPaths", [])
    if check_path_protection(file_path, read_only) or check_path_protection(resolved, read_only):
        return "block", f"Write/Edit to read-only path: {file_path}"

    no_delete = rules.get("noDeletePaths", [])
    if tool_name == "Write" and (check_path_protection(file_path, no_delete) or check_path_protection(resolved, no_delete)):
        return "ask", f"Overwriting file in accumulation-only path. Confirm? ({file_path})"

    return "allow", None


def main():
    import time
    logger = Logger("pre_tool_use")
    start_time = time.monotonic()

    input_data = read_stdin()
    if not input_data or "tool_name" not in input_data:
        logger.log("BLOCKED: malformed or empty stdin (fail-closed)")
        emit_event("PreToolUse", HOOK_NAME, 2, {"error": "malformed stdin"})
        sys.exit(2)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    try:
        rules = load_patterns()
    except Exception as e:
        logger.log(f"BLOCKED: patterns.yaml load failed — {e} (fail-closed)")
        emit_event("PreToolUse", HOOK_NAME, 2, {"error": f"patterns.yaml: {e}"})
        print(json.dumps({"error": f"patterns.yaml load failed: {e}"}), file=sys.stderr)
        sys.exit(2)

    decision = "allow"
    reason = None

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        decision, reason = check_bash_command(command, rules)
    elif tool_name in ("Write", "Edit"):
        decision, reason = check_write_edit(tool_name, tool_input, rules)
    elif tool_name in ("Read", "Glob", "Grep"):
        decision, reason = check_read(tool_input, rules)

    elapsed = int((time.monotonic() - start_time) * 1000)

    payload = {"tool": tool_name, "decision": decision}
    if tool_name == "Bash":
        payload["command"] = tool_input.get("command", "")[:500]
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
