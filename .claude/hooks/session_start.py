#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["python-dotenv>=1.0.0"]
# ///
"""SessionStart hook: .env whitelist, session_id generation, health check for all hooks."""

import json
import os
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
    import sys; sys.exit(2)

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
    "session_start.py", "setup.py", "pre_tool_use.py", "post_tool_use.py",
    "notification.py", "stop.py", "user_prompt_submit.py", "pre_compact.py",
    "subagent_start.py", "subagent_stop.py", "session_end.py",
    "permission_request.py", "post_tool_use_failure.py",
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


def main():
    import time
    logger = Logger("session_start")
    start_time = time.monotonic()

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
    if safe_env:
        env_summary = ", ".join(f"{k}={v}" for k, v in safe_env.items())
        context_parts.append(f"Environment: {env_summary}")
    context_parts.append(f"All {len(REQUIRED_HOOKS)} hooks passed health check.")

    elapsed = int((time.monotonic() - start_time) * 1000)
    emit_event("SessionStart", HOOK_NAME, 0, {"session_id": session_id}, elapsed)

    print(json.dumps({"message": "\n".join(context_parts)}))
    sys.exit(0)


if __name__ == "__main__":
    run_hook(main, HOOK_NAME, event_type="SessionStart")
