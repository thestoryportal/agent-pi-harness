#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""PostToolUse hook: validate output + emit metadata event.

Validators (run after Write/Edit/Bash that affect .py or .sql files):
  - ruff: lint Python files, block on errors for self-correction
  - schema: check SQL for public schema, bare TIMESTAMP, ENUM usage

Self-correction: output {"decision": "block", "reason": "..."} on stdout
with exit 0. Claude reads the reason and fixes the issue automatically.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    from _base import Logger, emit_event, handle_health_check, read_stdin, run_hook
except Exception:
    sys.exit(2)

HOOK_NAME = "post_tool_use.py"
handle_health_check(HOOK_NAME)


def extract_file_path(tool_name: str, tool_input: dict) -> str | None:
    if tool_name in ("Write", "Edit"):
        return tool_input.get("file_path", "")
    if tool_name == "Bash":
        cmd = tool_input.get("command", "")
        for marker in ["> ", ">> ", "tee "]:
            if marker in cmd:
                parts = cmd.split(marker)
                if len(parts) > 1:
                    candidate = parts[-1].strip().split()[0].strip("'\"")
                    if candidate.endswith(".py") or candidate.endswith(".sql"):
                        return candidate
    return None


def validate_ruff(file_path: str, logger: Logger) -> dict | None:
    if not file_path.endswith(".py"):
        return None
    abs_path = Path(file_path) if Path(file_path).is_absolute() else Path(PROJECT_DIR) / file_path
    if not abs_path.exists():
        return None
    try:
        result = subprocess.run(
            ["ruff", "check", str(abs_path), "--output-format", "json"],
            capture_output=True, text=True, timeout=10,
        )
    except FileNotFoundError:
        logger.log("ruff not found on PATH, skipping lint validation")
        return None
    except subprocess.TimeoutExpired:
        logger.log("ruff timed out, skipping")
        return None

    if result.returncode == 0:
        return None

    try:
        errors = json.loads(result.stdout)
    except json.JSONDecodeError:
        errors = []

    if not errors:
        return None

    MAX_ERRORS = 5
    summary_lines = []
    for err in errors[:MAX_ERRORS]:
        code = err.get("code", "?")
        msg = err.get("message", "?")
        row = err.get("location", {}).get("row", "?")
        summary_lines.append(f"  line {row}: {code} {msg}")
    if len(errors) > MAX_ERRORS:
        summary_lines.append(f"  ... and {len(errors) - MAX_ERRORS} more errors")

    return {
        "decision": "block",
        "reason": f"Ruff lint errors in {file_path}:\n" + "\n".join(summary_lines),
    }


SQL_CHECKS = [
    (
        r"\bCREATE\s+TABLE\s+public\.",
        "public schema not allowed. Use the project's designated schema.",
    ),
    (
        r"\bALTER\s+TABLE\s+public\.",
        "public schema not allowed.",
    ),
    (
        r"\bCREATE\s+TYPE\s+.*\s+AS\s+ENUM",
        "PostgreSQL ENUMs not allowed. Use CHECK constraints.",
    ),
    (
        r"\bTIMESTAMP\b(?!\s*TZ|\s*WITH\s+TIME\s+ZONE)",
        "Use TIMESTAMPTZ, not bare TIMESTAMP.",
    ),
]


def validate_sql(file_path: str, tool_input: dict) -> dict | None:
    if not file_path.endswith(".sql"):
        return None

    content = tool_input.get("content", "")
    if not content:
        abs_path = Path(file_path) if Path(file_path).is_absolute() else Path(PROJECT_DIR) / file_path
        if abs_path.exists():
            try:
                content = abs_path.read_text()
            except OSError:
                return None
    if not content:
        return None

    violations = []
    for pattern, message in SQL_CHECKS:
        if re.search(pattern, content, re.IGNORECASE):
            violations.append(message)

    if not violations:
        return None

    return {
        "decision": "block",
        "reason": f"SQL convention violations in {file_path}:\n"
        + "\n".join(f"  - {v}" for v in violations),
    }


def main():
    import time
    logger = Logger("post_tool_use")
    start_time = time.monotonic()

    d = read_stdin()
    tool_name = d.get("tool_name", "")
    tool_input = d.get("tool_input", {})
    tool_output = d.get("tool_output", {})
    tool_exit_code = tool_output.get("exit_code") if isinstance(tool_output, dict) else None
    stdout_preview = str(tool_output.get("stdout", ""))[:500] if isinstance(tool_output, dict) else ""

    file_path = extract_file_path(tool_name, tool_input)

    validation_result = None
    if file_path:
        validation_result = validate_ruff(file_path, logger)
        if not validation_result:
            validation_result = validate_sql(file_path, tool_input)

    payload = {"tool": tool_name, "exit_code": tool_exit_code, "output_preview": stdout_preview}
    if file_path:
        payload["validated_file"] = file_path
    if validation_result:
        payload["validation"] = validation_result["decision"]
        payload["validation_reason"] = validation_result["reason"][:500]

    elapsed = int((time.monotonic() - start_time) * 1000)
    emit_event("PostToolUse", HOOK_NAME, 0, payload, elapsed)

    if validation_result:
        logger.log(f"BLOCK: {tool_name} — {validation_result['reason'][:200]}")
        print(json.dumps(validation_result))
        sys.exit(0)

    logger.log(f"PostToolUse: {tool_name} (exit={tool_exit_code})")
    sys.exit(0)


if __name__ == "__main__":
    run_hook(main, HOOK_NAME, event_type="PostToolUse")
