"""Shared base for all ArhuGula hooks.

Provides: Logger, event emitter (JSONL fallback), stdin parser, health-check handler.

NOTE: This is a library module, not a standalone script. No PEP 723 shebang needed.
Only uses stdlib imports — all dependencies belong in the calling hook's PEP 723 block.
"""

import fcntl
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


DB_PATH = Path(PROJECT_DIR) / "apps" / "observe" / "events.db"


def _emit_to_jsonl(event: dict) -> None:
    """Write event to JSONL fallback log."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    events_file = LOGS_DIR / "events.jsonl"
    with open(events_file, "a") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.write(json.dumps(event) + "\n")
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def emit_event(
    event_type: str,
    hook_name: str,
    exit_code: int,
    payload: dict | None = None,
    duration_ms: int | None = None,
) -> None:
    """Emit a structured event to SQLite (preferred) or JSONL (fallback).

    SQLite path: attempt INSERT via apps.observe.db. On ImportError, skip
    retry and fall through to JSONL. On sqlite3.OperationalError, retry
    once after 50ms. On any other failure, fall through to JSONL.
    JSONL path: always available, used when DB is absent or write fails.
    """
    session_id = get_session_id()
    ts = datetime.now(timezone.utc).isoformat()
    payload_str = json.dumps(payload) if payload is not None else None

    event = {
        "event_type": event_type,
        "session_id": session_id,
        "timestamp": ts,
        "hook_name": hook_name,
        "exit_code": exit_code,
        "payload": payload_str,
        "duration_ms": duration_ms,
    }

    # Try SQLite if DB file exists
    if DB_PATH.exists():
        try:
            if PROJECT_DIR not in sys.path:
                sys.path.insert(0, PROJECT_DIR)
            from apps.observe.db import insert_event as db_insert
            db_insert(event_type, session_id, ts, hook_name, exit_code, payload_str, duration_ms, db_path=DB_PATH)
            return
        except ImportError:
            pass  # No retry on import failure, direct to JSONL
        except Exception:
            # Retry once after 50ms for transient errors (e.g., database locked)
            try:
                time.sleep(0.05)
                from apps.observe.db import insert_event as db_insert
                db_insert(event_type, session_id, ts, hook_name, exit_code, payload_str, duration_ms, db_path=DB_PATH)
                return
            except Exception:
                pass  # Fall through to JSONL

    _emit_to_jsonl(event)


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
    """Fail-open wrapper matching IndyDevDan's default. Logs crashes, does not block.

    Crash behavior:
    - Non-security hooks: log the crash, exit 1 (pass through — fail open)
    - Security-critical hooks: log the crash, exit 2 (block — always fail closed)

    When SP2 (Drive/Listen) ships unattended execution, add ARHUGULA_HOOK_MODE=closed
    env var to make all hooks fail-closed for unattended runs.
    """
    try:
        main_fn()
    except SystemExit:
        raise
    except BaseException as e:
        logger = Logger(hook_name)
        etype = event_type or hook_name.replace(".py", "").title().replace("_", "")
        if security_critical:
            logger.log(f"CRASH (fail-closed, security-critical): {type(e).__name__}: {e}")
            emit_event(etype, hook_name, 2, {"crash": str(e)})
            print(json.dumps({"error": f"Hook crashed: {hook_name}"}), file=sys.stderr)
            sys.exit(2)
        else:
            logger.log(f"CRASH (fail-open): {type(e).__name__}: {e}")
            emit_event(etype, hook_name, 1, {"crash": str(e)})
            sys.exit(1)
