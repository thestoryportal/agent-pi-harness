#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""PostToolUse hook: validate output + emit metadata event.

Validators (run after Write/Edit/Bash that affect supported file types):
  - ruff: lint Python files, block on errors for self-correction
  - schema: check SQL for public schema, bare TIMESTAMP, ENUM usage
  - csv: parse and balance validation for CSV files (via external validator)
  - html: structure and image validation for HTML files (via external validator)

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
                    if candidate.endswith((".py", ".sql", ".csv", ".html")):
                        return candidate
    return None


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


def validate_external(file_path: str, validator_name: str, hook_data: dict, logger: Logger) -> dict | None:
    """Run a standalone validator script from .claude/hooks/validators/ via subprocess."""
    # S-01: Sanitize validator_name to prevent path traversal
    validator_name = Path(validator_name).name
    validators_dir = (Path(PROJECT_DIR) / ".claude" / "hooks" / "validators").resolve()
    validator_script = (validators_dir / validator_name).resolve()
    if not validator_script.parent == validators_dir:
        logger.log(f"SECURITY: {validator_name} escapes validators directory, blocked")
        return None
    if not validator_script.exists():
        logger.log(f"{validator_name} not found, skipping")
        return None

    # S-03: Strip potentially sensitive content before passing to subprocess
    # N-01: Use the caller's extracted file_path (handles Bash redirection),
    # not hook_data's tool_input.file_path (missing for Bash tool calls)
    safe_data = {
        "tool_name": hook_data.get("tool_name", ""),
        "tool_input": {"file_path": file_path},
    }

    try:
        result = subprocess.run(
            ["uv", "run", str(validator_script)],
            input=json.dumps(safe_data),
            capture_output=True, text=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        logger.log(f"{validator_name} timed out, skipping")
        return None
    except Exception as e:
        logger.log(f"{validator_name} error: {e}")
        return None

    if not result.stdout.strip():
        return None
    try:
        out = json.loads(result.stdout)
        if out.get("decision") == "block":
            return out
    except json.JSONDecodeError:
        pass
    return None


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
        if file_path.endswith(".py"):
            validation_result = validate_external(file_path, "ruff_validator.py", d, logger)
            if not validation_result:
                validation_result = validate_external(file_path, "ty_validator.py", d, logger)
        if not validation_result and file_path.endswith(".sql"):
            validation_result = validate_sql(file_path, tool_input)
        if not validation_result and file_path.endswith(".csv"):
            validation_result = validate_external(file_path, "csv_single_validator.py", d, logger)
        if not validation_result and file_path.endswith(".html"):
            validation_result = validate_external(file_path, "html_validator.py", d, logger)

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
