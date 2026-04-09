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

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


def main():
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    events_file = Path(project_dir) / ".claude" / "logs" / "events.jsonl"

    if not events_file.exists():
        print("No events.jsonl found. Nothing to prune.")
        return

    retention_days = int(os.environ.get("OBSERVE_RETENTION_DAYS", "7"))
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)

    # Read all events
    lines = events_file.read_text().strip().split("\n")
    if not lines or lines == [""]:
        print("events.jsonl is empty.")
        return

    total = len(lines)
    kept = []
    pruned = 0

    for line in lines:
        if not line.strip():
            continue
        try:
            event = json.loads(line)
            ts = datetime.fromisoformat(event.get("timestamp", ""))
            if ts >= cutoff:
                kept.append(line)
            else:
                pruned += 1
        except (json.JSONDecodeError, ValueError):
            # Keep unparseable lines (don't lose data)
            kept.append(line)

    # Write back
    events_file.write_text("\n".join(kept) + "\n" if kept else "")

    print(f"Pruned {pruned}/{total} events (retention: {retention_days} days)")
    print(f"Remaining: {len(kept)} events")


if __name__ == "__main__":
    main()
