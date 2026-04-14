#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["python-dotenv>=1.0.0"]
# ///
"""SessionStart hook: .env whitelist, session_id generation, health check for all hooks."""

import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    from dotenv import dotenv_values
    from _base import Logger, emit_event, handle_health_check, hook_output, read_stdin, run_hook
except Exception:
    sys.exit(2)

HOOK_NAME = "session_start.py"
handle_health_check(HOOK_NAME)


def load_env_whitelist(logger) -> dict[str, str]:
    """Load .env, return only variables marked with # INJECT in .env.example."""
    env_example = Path(PROJECT_DIR) / ".env.example"
    env_file = Path(PROJECT_DIR) / ".env"

    if not env_file.exists():
        logger.log(".env not found, skipping env injection")
        return {}

    inject_keys: set[str] = set()
    if env_example.exists():
        for line in env_example.read_text().splitlines():
            if "# INJECT" in line and "=" in line.split("#")[0]:
                key = line.split("=")[0].strip()
                if key:
                    inject_keys.add(key)

    SECRET_PATTERNS = {"KEY", "TOKEN", "SECRET", "PASSWORD", "CREDENTIAL", "AUTH"}

    all_values = dotenv_values(env_file)

    # Only load INJECT-marked, non-secret vars into os.environ.
    # Secrets stay out of the process environment entirely — they're not
    # inherited by child processes (hooks, subagents, Drive sessions).
    safe_values = {}
    for k, v in all_values.items():
        if k in inject_keys and v:
            if any(pat in k.upper() for pat in SECRET_PATTERNS):
                logger.log(f"DENIED injection of {k} (matches secret denylist)")
                continue
            safe_values[k] = v
            os.environ[k] = v

    logger.log(f"Loaded {len(all_values)} env vars, {len(safe_values)} whitelisted for injection")
    return safe_values


def resolve_session_id(logger) -> str:
    """Use CLAUDE_SESSION_ID (built-in) or generate UUID4 as fallback."""
    session_id = os.environ.get("CLAUDE_SESSION_ID", str(uuid.uuid4()))
    started_at = datetime.now(timezone.utc).isoformat()
    os.environ["ARHUGULA_SESSION_ID"] = session_id

    session_meta = Path(PROJECT_DIR) / ".claude" / "logs" / f"session-start-{session_id}.json"
    session_meta.parent.mkdir(parents=True, exist_ok=True)
    with open(session_meta, "w") as f:
        json.dump({"session_id": session_id, "started_at": started_at}, f)

    logger.log(f"Session ID: {session_id}")
    return session_id


REQUIRED_HOOKS = [
    "session_start.py", "setup_init.py", "setup_maintenance.py",
    "pre_tool_use.py", "post_tool_use.py",
    "notification.py", "stop.py", "user_prompt_submit.py", "pre_compact.py",
    "subagent_start.py", "subagent_stop.py", "session_end.py",
    "permission_request.py", "post_tool_use_failure.py",
    # Note: bash/edit/write_damage_control.py moved to
    # .claude/skills/damage-control/hooks/damage-control-python/ during
    # SP2 Phase E (2026-04-13). They are no longer at the project hooks/
    # location and so are not validated by this health check, which only
    # walks the project hooks directory. The skill-located copies are
    # still loaded by settings.json PreToolUse matchers and are
    # transitively exercised on every tool call.
]


def run_health_checks(logger) -> list[str]:
    """Dry-run --health-check on all required hook files. Returns list of failures."""
    hooks_dir = Path(PROJECT_DIR) / ".claude" / "hooks"
    failures = []

    for hook_name in REQUIRED_HOOKS:
        hook_file = hooks_dir / hook_name
        if not hook_file.exists():
            failures.append(hook_name)
            logger.log(f"MISSING: {hook_name}")
            continue
        if not os.access(hook_file, os.X_OK):
            failures.append(hook_file.name)
            logger.log(f"NOT EXECUTABLE: {hook_file.name}")
            continue
        try:
            result = subprocess.run(
                ["uv", "run", str(hook_file), "--health-check"],
                capture_output=True, text=True, timeout=10,
                env={**os.environ, "CLAUDE_PROJECT_DIR": PROJECT_DIR},
            )
            if result.returncode != 0:
                failures.append(hook_file.name)
                logger.log(f"FAIL: {hook_file.name} (exit {result.returncode})")
            else:
                logger.log(f"OK: {hook_file.name}")
        except subprocess.TimeoutExpired:
            failures.append(hook_file.name)
            logger.log(f"TIMEOUT: {hook_file.name}")

    return failures


def get_git_context(logger) -> list[str]:
    """Collect git state for session context injection."""
    lines = []
    def run(cmd):
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                cwd=PROJECT_DIR, timeout=5,
            )
            return result.stdout.strip()
        except (subprocess.TimeoutExpired, OSError):
            return ""

    branch = run("git rev-parse --abbrev-ref HEAD")
    if branch:
        lines.append(f"Branch: {branch}")

    dirty_count = run("git status --porcelain | wc -l").strip()
    if dirty_count and int(dirty_count) > 0:
        lines.append(f"Dirty files: {dirty_count}")
        dirty_files = run("git status --porcelain")
        if dirty_files:
            lines.append(f"Changes:\n{dirty_files}")

    recent = run("git log --oneline -5")
    if recent:
        lines.append(f"Recent commits:\n{recent}")

    diff_stat = run("git diff --stat")
    if diff_stat:
        lines.append(f"Diff summary:\n{diff_stat}")

    return lines


def detect_environment() -> str:
    """Detect local vs production from DATABASE_URL."""
    db_url = os.environ.get("DATABASE_URL", "")
    if not db_url:
        return "UNKNOWN — DATABASE_URL not set"
    local_hosts = ["localhost", "127.0.0.1", "host.docker.internal"]
    if any(h in db_url for h in local_hosts):
        return "LOCAL"
    return "PRODUCTION — Exercise extreme caution"


SAFE_PATH_RE = re.compile(r'\A[A-Za-z0-9/_. -]+\Z')


def validate_project_dir(logger) -> bool:
    """Reject CLAUDE_PROJECT_DIR if it contains unsafe characters.

    Hook commands in settings.json and command frontmatter interpolate
    $CLAUDE_PROJECT_DIR via the shell. Only alphanumerics, slashes,
    underscores, dots, spaces, and hyphens are allowed. Everything else
    (quotes, backslash, $, backticks, glob chars, etc.) is rejected.
    Allowlist approach — safer than enumerating every dangerous character.
    """
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return True
    if not SAFE_PATH_RE.match(project_dir):
        logger.log(f"SECURITY: CLAUDE_PROJECT_DIR contains unsafe characters: {project_dir!r}")
        return False
    return True


def main():
    import time
    logger = Logger("session_start")
    start_time = time.monotonic()

    # S-04: Validate CLAUDE_PROJECT_DIR before any hooks use it in shell commands
    if not validate_project_dir(logger):
        msg = "CLAUDE_PROJECT_DIR contains shell metacharacters — session blocked"
        logger.log(msg)
        print(f"BLOCKED: {msg}", file=sys.stderr)
        emit_event("SessionStart", HOOK_NAME, 2, {"reason": "unsafe_project_dir"})
        sys.exit(2)

    input_data = read_stdin()
    session_id = resolve_session_id(logger)
    safe_env = load_env_whitelist(logger)

    failures = run_health_checks(logger)
    if failures:
        msg = f"Hook health check failed: {', '.join(failures)}"
        logger.log(msg)
        print(f"BLOCKED: {msg}", file=sys.stderr)
        emit_event("SessionStart", HOOK_NAME, 2, {"failures": failures})
        sys.exit(2)

    context_parts = [f"Session ID: {session_id}"]

    env_mode = detect_environment()
    context_parts.append(f"Environment: {env_mode}")

    git_lines = get_git_context(logger)
    if git_lines:
        context_parts.extend(git_lines)

    if safe_env:
        env_summary = ", ".join(f"{k}={v}" for k, v in safe_env.items())
        context_parts.append(f"Injected env: {env_summary}")

    context_parts.append(f"All {len(REQUIRED_HOOKS)} hooks passed health check.")

    elapsed = int((time.monotonic() - start_time) * 1000)
    emit_event("SessionStart", HOOK_NAME, 0, {"session_id": session_id}, elapsed)

    print(hook_output("SessionStart", "\n".join(context_parts)))
    sys.exit(0)


if __name__ == "__main__":
    run_hook(main, HOOK_NAME, event_type="SessionStart")
