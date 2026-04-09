"""Shared base for all ArhuGula hooks.

Provides: Logger, event emitter (JSONL fallback), stdin parser, health-check handler.

NOTE: This is a library module, not a standalone script. No PEP 723 shebang needed.
Only uses stdlib imports — all dependencies belong in the calling hook's PEP 723 block.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
LOGS_DIR = Path(PROJECT_DIR) / ".claude" / "logs"


def get_session_id() -> str:
    """Resolve session ID lazily at call time (not import time).

    Priority: CLAUDE_SESSION_ID (built-in) > ARHUGULA_SESSION_ID (legacy) >
    session-start.json fallback > "unknown".
    """
    sid = os.environ.get("CLAUDE_SESSION_ID")
    if sid:
        return sid
    sid = os.environ.get("ARHUGULA_SESSION_ID")
    if sid:
        return sid
    try:
        meta_files = sorted(LOGS_DIR.glob("session-start-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if meta_files:
            meta = json.loads(meta_files[0].read_text())
            return meta.get("session_id", "unknown")
    except (json.JSONDecodeError, OSError):
        pass
    return "unknown"


class Logger:
    """Dual stderr + file logger."""

    def __init__(self, hook_name: str):
        self.hook_name = hook_name
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.log_file = LOGS_DIR / f"{hook_name}.log"

    def log(self, message: str) -> None:
        ts = datetime.now(timezone.utc).isoformat()
        line = f"[{ts}] [{self.hook_name}] {message}"
        print(line, file=sys.stderr)
        with open(self.log_file, "a") as f:
            f.write(line + "\n")


def read_stdin() -> dict:
    """Read and parse JSON from stdin. Returns empty dict on failure."""
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return {}


def emit_event(
    event_type: str,
    hook_name: str,
    exit_code: int,
    payload: dict | None = None,
    duration_ms: int | None = None,
) -> None:
    """Emit a structured event to JSONL fallback log.

    In sub-project 3 (Observe), this will attempt SQLite INSERT first
    with retry-once-then-JSONL fallback. For sub-project 1, JSONL only.
    The JSONL fallback uses a reduced schema: `id` column omitted
    (auto-increment meaningful only in SQLite context).
    """
    event = {
        "event_type": event_type,
        "session_id": get_session_id(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hook_name": hook_name,
        "exit_code": exit_code,
        "payload": json.dumps(payload) if payload is not None else None,
        "duration_ms": duration_ms,
    }
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    events_file = LOGS_DIR / "events.jsonl"
    with open(events_file, "a") as f:
        f.write(json.dumps(event) + "\n")


def hook_output(hook_event_name: str, additional_context: str = "") -> str:
    """Build the standard hookSpecificOutput JSON string."""
    output = {"hookSpecificOutput": {"hookEventName": hook_event_name}}
    if additional_context:
        output["hookSpecificOutput"]["additionalContext"] = additional_context
    return json.dumps(output)


def handle_health_check(hook_name: str) -> None:
    """If --health-check flag is present, print OK and exit 0."""
    if "--health-check" in sys.argv:
        print(f"OK:{hook_name}")
        sys.exit(0)


def run_hook(main_fn, hook_name: str, *, security_critical: bool = False, event_type: str = "") -> None:
    """Fail-closed wrapper. Catches ALL unhandled exceptions and exits 2.

    This ensures that a crash (missing dep, runtime error, KeyboardInterrupt,
    etc.) blocks the operation rather than silently allowing it. Security-critical
    hooks (pre_tool_use, permission_request) MUST pass security_critical=True.
    """
    try:
        main_fn()
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else 1
        if security_critical and code not in (0, 2):
            logger = Logger(hook_name)
            logger.log(f"COERCED exit {code} -> 2 (security-critical hook)")
            sys.exit(2)
        raise
    except BaseException as e:
        logger = Logger(hook_name)
        logger.log(f"CRASH (fail-closed): {type(e).__name__}: {e}")
        etype = event_type or hook_name.replace(".py", "").title().replace("_", "")
        emit_event(etype, hook_name, 2, {"crash": str(e)})
        print(json.dumps({"error": f"Hook crashed: {hook_name}"}), file=sys.stderr)
        sys.exit(2)
