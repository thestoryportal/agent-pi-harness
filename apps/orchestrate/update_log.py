"""Chronological update log — append-only JSONL for job state tracking.

Each entry records a status change with timestamp, job ID, and metadata.
Thread-safe via fcntl.flock. Follows the _base.py emit_event pattern.
"""

import fcntl
import json
import os
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())) / "apps" / "orchestrate" / "logs"
UPDATE_LOG = LOG_DIR / "updates.jsonl"


def append_update(
    job_id: str,
    status: str,
    message: str,
    metadata: dict | None = None,
    *,
    log_path: Path | None = None,
) -> dict:
    """Append a chronological update entry to the JSONL log.

    Thread-safe via fcntl.flock. Never modifies existing entries.
    Returns the written entry dict.
    """
    target = log_path or UPDATE_LOG
    target.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "job_id": job_id,
        "status": status,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {},
    }

    with open(target, "a") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.write(json.dumps(entry) + "\n")
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    return entry


def read_updates(
    job_id: str | None = None,
    *,
    log_path: Path | None = None,
) -> list[dict]:
    """Read all update entries, optionally filtered by job_id.

    Returns list in append order (chronological).
    Skips malformed lines silently.
    """
    target = log_path or UPDATE_LOG
    if not target.exists():
        return []

    entries = []
    with open(target) as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
        try:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if job_id is None or entry.get("job_id") == job_id:
                    entries.append(entry)
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    return entries


def clear_log(*, log_path: Path | None = None) -> None:
    """Truncate the log. For testing only."""
    target = log_path or UPDATE_LOG
    if target.exists():
        target.unlink()
