#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""PreToolUse hook: intercept destructive operations, gate mv/cp by path.

Exit codes: 0=allow, 2=block. This is a security-critical hook — never exit 1.
"""

import json
import os
import re
import shlex
import sys
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    from _base import Logger, emit_event, handle_health_check, read_stdin, run_hook
except Exception:
    import sys; sys.exit(2)

HOOK_NAME = "pre_tool_use.py"
handle_health_check(HOOK_NAME)

ZERO_ACCESS_PATHS = [
    os.path.expanduser("~/.ssh"), "~/.ssh", "$HOME/.ssh", "${HOME}/.ssh",
    os.path.expanduser("~/.aws"), "~/.aws", "$HOME/.aws", "${HOME}/.aws",
    os.path.expanduser("~/.gnupg"), "~/.gnupg", "$HOME/.gnupg", "${HOME}/.gnupg",
    os.path.expanduser("~/.config/gh"), "~/.config/gh",
]

IMMUTABLE_PATHS = [
    ".claude/hooks/",
    ".claude/settings.json",
    ".claude/logs/",
]

ENV_PATTERN = re.compile(r"(^|\s|/)\.env(\s|$|\"|\')")

DANGEROUS_PATTERNS = [
    (r"\brm\s+.*-[a-z]*r[a-z]*f", "recursive force delete"),
    (r"\brm\s+.*-[a-z]*f[a-z]*r", "recursive force delete"),
    (r"\brm\s+-rf\s+[/~]", "destructive rm at root/home"),
    (r"\bgit\s+push\s+.*--force", "force push"),
    (r"\bgit\s+push\s+-f\b", "force push"),
    (r"\bgit\s+reset\s+--hard", "hard reset"),
    (r"\bgit\s+clean\s+-[a-z]*f", "git clean force"),
    (r"\bDROP\s+(TABLE|DATABASE)\b", "SQL DROP"),
    (r"\bDELETE\s+FROM\s+\w+\s*;", "unguarded DELETE"),
    (r"\bcurl\s+.*\|\s*(bash|sh|zsh)", "pipe to shell"),
    (r"\bchmod\s+777\b", "world-writable permissions"),
    (r"\bchown\s+-R\b", "recursive chown"),
]

PROJECT_ROOT = Path(PROJECT_DIR).resolve()

SHELL_COMPOSITION_MARKERS = [";", "&&", "||", "|", "`", "$(", "<<", ">>"]

FLAG_ALIASES = {
    "--recursive": "-r", "--force": "-f", "--verbose": "-v",
    "--interactive": "-i", "--preserve": "-p", "--hard": "--hard",
}


def is_within_project(path_str: str) -> bool:
    try:
        expanded = os.path.expanduser(os.path.expandvars(path_str))
        resolved = Path(expanded).resolve()
        return resolved == PROJECT_ROOT or resolved.is_relative_to(PROJECT_ROOT)
    except (OSError, ValueError):
        return False


def touches_zero_access(command: str) -> str | None:
    expanded = os.path.expanduser(os.path.expandvars(command))
    for zap in ZERO_ACCESS_PATHS:
        if zap in command or zap in expanded:
            return zap
    if ENV_PATTERN.search(command) or ENV_PATTERN.search(expanded):
        return ".env"
    return None


def touches_immutable(path_str: str) -> str | None:
    for imm in IMMUTABLE_PATHS:
        if imm in path_str:
            return imm
    return None


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


def check_bash_command(command: str) -> tuple[str, str | None]:
    for marker in SHELL_COMPOSITION_MARKERS:
        if marker in command:
            return "block", f"Shell composition detected ({marker}) — fail closed"

    zap = touches_zero_access(command)
    if zap:
        return "block", f"Access to protected path: {zap}"

    norm = normalize_command(command)

    for pattern, description in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE) or re.search(pattern, norm, re.IGNORECASE):
            return "block", f"Dangerous operation: {description}"

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

    return "allow", None


def check_read(tool_input: dict) -> tuple[str, str | None]:
    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
    pattern = tool_input.get("pattern", "")
    check_str = file_path or pattern
    if not check_str:
        return "allow", None
    try:
        resolved = str(Path(os.path.expanduser(check_str)).resolve())
    except (OSError, ValueError):
        resolved = check_str
    zap = touches_zero_access(resolved)
    if not zap:
        zap = touches_zero_access(check_str)
    if zap:
        return "block", f"Read/search of protected path: {zap}"
    return "allow", None


def check_write_edit(tool_input: dict) -> tuple[str, str | None]:
    file_path = tool_input.get("file_path", "")
    if not file_path:
        return "allow", None
    try:
        resolved = str(Path(os.path.expanduser(file_path)).resolve())
    except (OSError, ValueError):
        return "block", f"Write/Edit path unresolvable — fail closed"
    zap = touches_zero_access(resolved)
    if zap:
        return "block", f"Write/Edit to protected path (resolved): {zap}"
    imm = touches_immutable(file_path) or touches_immutable(resolved)
    if imm:
        return "block", f"Write/Edit to immutable harness path: {imm}"
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

    decision = "allow"
    reason = None

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        decision, reason = check_bash_command(command)
    elif tool_name in ("Write", "Edit"):
        decision, reason = check_write_edit(tool_input)
    elif tool_name in ("Read", "Glob", "Grep"):
        decision, reason = check_read(tool_input)

    exit_code = 0 if decision == "allow" else 2
    elapsed = int((time.monotonic() - start_time) * 1000)

    payload = {"tool": tool_name, "decision": decision}
    if tool_name == "Bash":
        payload["command"] = tool_input.get("command", "")[:500]
    if reason:
        payload["reason"] = reason

    emit_event("PreToolUse", HOOK_NAME, exit_code, payload, elapsed)

    if decision == "block":
        logger.log(f"BLOCKED: {tool_name} — {reason}")
        print(json.dumps({"error": reason}), file=sys.stderr)
        sys.exit(2)
    else:
        logger.log(f"ALLOW: {tool_name}")
        sys.exit(0)


if __name__ == "__main__":
    run_hook(main, HOOK_NAME, security_critical=True, event_type="PreToolUse")
