#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Prune events.jsonl — delete entries older than retention window.

Usage: uv run apps/observe/prune.py
       OBSERVE_RETENTION_DAYS=0 uv run apps/observe/prune.py  # clear all

Reads OBSERVE_RETENTION_DAYS from env (default 7).
"""

import fcntl
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


def parse_retention_days() -> int:
    raw = os.environ.get("OBSERVE_RETENTION_DAYS", "7")
    try:
        days = int(raw)
    except ValueError:
        print(f"ERROR: OBSERVE_RETENTION_DAYS={raw!r} is not an integer.", file=sys.stderr)
        sys.exit(1)
    if days < 0:
        print(f"ERROR: OBSERVE_RETENTION_DAYS={days} must be >= 0.", file=sys.stderr)
        sys.exit(1)
    return days


def prune_sqlite(cutoff: datetime, db_path: Path) -> None:
    """Prune SQLite events older than cutoff, then VACUUM."""
    if not db_path.exists():
        return
    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path), isolation_level=None)
        conn.execute("PRAGMA busy_timeout=500")
        cursor = conn.execute("DELETE FROM events WHERE timestamp < ?", (cutoff.isoformat(),))
        deleted = cursor.rowcount
        conn.execute("VACUUM")
        conn.close()
        print(f"SQLite: pruned {deleted} events, vacuumed")
    except Exception as e:
        print(f"SQLite prune error: {e}", file=sys.stderr)


def main():
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    events_file = Path(project_dir) / ".claude" / "logs" / "events.jsonl"
    db_path = Path(project_dir) / "apps" / "observe" / "events.db"

    retention_days = parse_retention_days()
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)

    # Prune SQLite first
    prune_sqlite(cutoff, db_path)

    # Hold LOCK_EX for the full read-truncate-write cycle so concurrent
    # hook appenders (which also flock in _base.emit_event) cannot interleave.
    # In-place truncate (not os.replace) preserves the inode so any stray
    # file handles opened without the lock still target the same file.
    try:
        f = open(events_file, "r+")
    except FileNotFoundError:
        print("No events.jsonl found. Nothing to prune.")
        return

    with f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            content = f.read()
            if not content.strip():
                print("events.jsonl is empty.")
                return

            total = 0
            kept: list[str] = []
            pruned = 0
            malformed = 0

            for line in content.split("\n"):
                if not line.strip():
                    continue
                total += 1
                try:
                    event = json.loads(line)
                    ts = datetime.fromisoformat(event.get("timestamp", ""))
                except (json.JSONDecodeError, ValueError, TypeError):
                    # Keep unparseable lines (don't lose data) but count them
                    # so the retention leak is observable.
                    malformed += 1
                    kept.append(line)
                    continue
                if ts >= cutoff:
                    kept.append(line)
                else:
                    pruned += 1

            f.seek(0)
            f.truncate()
            if kept:
                f.write("\n".join(kept) + "\n")
            f.flush()
            os.fsync(f.fileno())
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    print(f"Pruned {pruned}/{total} events (retention: {retention_days} days)")
    print(f"Remaining: {len(kept)} events ({malformed} malformed/unparseable)")


if __name__ == "__main__":
    main()
