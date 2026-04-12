#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""
Type Checker Validator for Claude Code PostToolUse Hook

Runs `uvx ty check <file_path>` for type checking on single Python files.

Outputs JSON decision for Claude Code PostToolUse hook:
- {"decision": "block", "reason": "..."} to block and retry
- {} to allow completion
"""
import json
import logging
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / "ty_validator.log"
PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

_fd = os.open(LOG_FILE, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
os.close(_fd)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(LOG_FILE, mode='a')]
)
logger = logging.getLogger(__name__)


def main():
    logger.info("=" * 50)
    logger.info("TY VALIDATOR POSTTOOLUSE HOOK TRIGGERED")

    try:
        stdin_data = sys.stdin.read()
        if stdin_data.strip():
            hook_input = json.loads(stdin_data)
            logger.info(f"hook_input keys: {list(hook_input.keys())}")
        else:
            hook_input = {}
    except json.JSONDecodeError:
        hook_input = {}

    file_path = hook_input.get("tool_input", {}).get("file_path", "")
    logger.info(f"file_path: {file_path}")

    if not file_path.endswith(".py"):
        logger.info("Skipping non-Python file")
        print(json.dumps({}))
        return

    resolved = Path(file_path).resolve()
    if not str(resolved).startswith(str(Path(PROJECT_DIR).resolve()) + "/"):
        logger.info(f"Skipping file outside project: {resolved}")
        print(json.dumps({}))
        return

    # Skip sub-packages with their own pyproject.toml (e.g. mcp/just-prompt/)
    # ty can't resolve their dependencies from the project root
    rel = resolved.relative_to(Path(PROJECT_DIR).resolve())
    for parent in rel.parents:
        candidate = Path(PROJECT_DIR).resolve() / parent / "pyproject.toml"
        if parent != Path(".") and candidate.exists():
            logger.info(f"Skipping sub-package file: {resolved} (has own pyproject.toml at {candidate})")
            print(json.dumps({}))
            return

    logger.info(f"Running: uvx ty check {file_path}")
    try:
        result = subprocess.run(
            ["uvx", "ty", "check", file_path],
            capture_output=True,
            text=True,
            timeout=20
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if stdout:
            for line in stdout.split('\n')[:20]:
                logger.info(f"  {line}")

        if result.returncode == 0:
            logger.info("RESULT: PASS - Type check successful")
            print(json.dumps({}))
        else:
            logger.info(f"RESULT: BLOCK (exit code {result.returncode})")
            if stderr:
                for line in stderr.split('\n')[:10]:
                    logger.info(f"  ERROR: {line}")
            error_output = stdout or stderr or "Type check failed"
            print(json.dumps({
                "decision": "block",
                "reason": f"Type check failed:\n{error_output[:500]}"
            }))

    except subprocess.TimeoutExpired:
        logger.info("RESULT: PASS (timeout, fail-open)")
        print(json.dumps({}))
    except FileNotFoundError:
        logger.info("RESULT: PASS (uvx ty not found, skipping)")
        print(json.dumps({}))


if __name__ == "__main__":
    main()
