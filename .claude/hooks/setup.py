#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Setup hook: run uv sync, npm install on claude --init."""

import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    from _base import Logger, emit_event, handle_health_check, hook_output, read_stdin, run_hook
except Exception:
    import sys; sys.exit(2)

HOOK_NAME = "setup.py"
handle_health_check(HOOK_NAME)


def run_cmd(cmd: list[str], label: str, logger) -> bool:
    logger.log(f"Running: {label}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_DIR)
    if result.returncode != 0:
        logger.log(f"FAILED: {label} — {result.stderr[:500]}")
        return False
    logger.log(f"OK: {label}")
    return True


def main():
    import time
    logger = Logger("setup")
    start_time = time.monotonic()

    input_data = read_stdin()
    actions = []
    has_failure = False

    if run_cmd(["uv", "sync"], "uv sync", logger):
        actions.append("Python dependencies synced")
    else:
        actions.append("FAILED: uv sync")
        has_failure = True

    if Path(PROJECT_DIR, "package.json").exists():
        if run_cmd(["npm", "install"], "npm install", logger):
            actions.append("Node dependencies installed")
        else:
            actions.append("FAILED: npm install")
            has_failure = True

    db_path = Path(PROJECT_DIR) / "apps" / "observe" / "events.db"
    if db_path.parent.exists() and not db_path.exists():
        logger.log("db init: creating Observe SQLite database")
        try:
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("""CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                session_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                hook_name TEXT NOT NULL,
                exit_code INTEGER NOT NULL,
                payload TEXT,
                duration_ms INTEGER
            )""")
            conn.commit()
            conn.close()
            actions.append("Observe database initialized (WAL mode)")
        except Exception as e:
            logger.log(f"db init skipped: {e}")
            actions.append(f"db init skipped: {e}")
    else:
        actions.append("db init skipped (Observe app not yet present)")

    exit_code = 2 if has_failure else 0
    elapsed = int((time.monotonic() - start_time) * 1000)
    emit_event("Setup", HOOK_NAME, exit_code, {"actions": actions}, elapsed)

    summary = ("Setup FAILED:\n" if has_failure else "Setup complete:\n") + "\n".join(f"- {a}" for a in actions)
    print(json.dumps({"message": summary}))
    sys.exit(exit_code)


if __name__ == "__main__":
    run_hook(main, HOOK_NAME, event_type="Setup")
