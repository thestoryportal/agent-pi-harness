"""Task management system — three-state lifecycle with dependency tracking.

States: pending → in_progress → completed.
Blocked tasks (unmet dependencies) cannot be claimed.
Thread-safe via fcntl.flock — single exclusive lock for read-modify-write.
"""

from __future__ import annotations

import fcntl
import json
import os
import re
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path

TASK_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())) / "apps" / "orchestrate" / "logs"
TASK_FILE = TASK_DIR / "tasks.jsonl"
VALID_STATUSES = ("pending", "in_progress", "completed")
_SAFE_ID = re.compile(r"[a-zA-Z0-9_.-]+")


def _validate_id(value: str, label: str) -> None:
    """Reject IDs that contain unsafe characters."""
    if not _SAFE_ID.fullmatch(value):
        raise ValueError(f"invalid {label} {value!r}: must match [a-zA-Z0-9_.-]+")


def _parse_jsonl(text: str) -> list[dict]:
    """Parse JSONL text into list of dicts. Skips malformed lines."""
    tasks: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            tasks.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return tasks


def _serialize_jsonl(tasks: list[dict]) -> str:
    """Serialize list of dicts to JSONL text."""
    return "".join(json.dumps(t) + "\n" for t in tasks)


def _read_all(path: Path) -> list[dict]:
    """Read all task records from JSONL under shared lock."""
    if not path.exists():
        return []
    with open(path) as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
        try:
            return _parse_jsonl(f.read())
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def _mutate(path: Path, fn: Callable[[list[dict]], None]) -> list[dict]:
    """Read-modify-write under a single exclusive lock.

    Opens file in r+ mode (or creates it), acquires LOCK_EX, reads all
    tasks, calls fn(tasks), writes back, and returns the task list.
    The callable fn should mutate the list in place.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()
    with open(path, "r+") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            tasks = _parse_jsonl(f.read())
            fn(tasks)
            f.seek(0)
            f.truncate()
            f.write(_serialize_jsonl(tasks))
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    return tasks


def create_task(
    task_id: str,
    title: str,
    dependencies: list[str] | None = None,
    metadata: dict | None = None,
    *,
    task_path: Path | None = None,
) -> dict:
    """Create a new task in pending state.

    Raises ValueError if task_id already exists or task_id is invalid.
    """
    _validate_id(task_id, "task_id")
    target = task_path or TASK_FILE
    now = datetime.now(timezone.utc).isoformat()
    task: dict = {
        "task_id": task_id,
        "title": title,
        "status": "pending",
        "agent": None,
        "dependencies": dependencies or [],
        "metadata": metadata or {},
        "created_at": now,
        "updated_at": now,
    }

    def _do(tasks: list[dict]) -> None:
        for t in tasks:
            if t["task_id"] == task_id:
                raise ValueError(f"task {task_id!r} already exists")
        tasks.append(task)

    _mutate(target, _do)
    return task


def claim_task(
    task_id: str,
    agent: str,
    *,
    task_path: Path | None = None,
) -> dict:
    """Transition pending → in_progress.

    Raises ValueError if task not found, not pending, dependencies unmet, or IDs invalid.
    """
    _validate_id(task_id, "task_id")
    _validate_id(agent, "agent")
    target = task_path or TASK_FILE
    result: list[dict] = []

    def _do(tasks: list[dict]) -> None:
        status_lookup = {t["task_id"]: t["status"] for t in tasks}
        task = None
        for t in tasks:
            if t["task_id"] == task_id:
                task = t
                break

        if task is None:
            raise ValueError(f"task {task_id!r} not found")
        if task["status"] != "pending":
            raise ValueError(f"task {task_id!r} is {task['status']!r}, not pending")

        for dep_id in task["dependencies"]:
            dep_status = status_lookup.get(dep_id)
            if dep_status != "completed":
                raise ValueError(f"dependency {dep_id!r} is not completed")

        task["status"] = "in_progress"
        task["agent"] = agent
        task["updated_at"] = datetime.now(timezone.utc).isoformat()
        result.append(task)

    _mutate(target, _do)
    return result[0]


def complete_task(
    task_id: str,
    *,
    task_path: Path | None = None,
) -> dict:
    """Transition in_progress → completed.

    Raises ValueError if task not found or not in_progress.
    """
    target = task_path or TASK_FILE
    result: list[dict] = []

    def _do(tasks: list[dict]) -> None:
        task = None
        for t in tasks:
            if t["task_id"] == task_id:
                task = t
                break

        if task is None:
            raise ValueError(f"task {task_id!r} not found")
        if task["status"] != "in_progress":
            raise ValueError(f"task {task_id!r} is {task['status']!r}, not in_progress")

        task["status"] = "completed"
        task["updated_at"] = datetime.now(timezone.utc).isoformat()
        result.append(task)

    _mutate(target, _do)
    return result[0]


def get_task(
    task_id: str,
    *,
    task_path: Path | None = None,
) -> dict | None:
    """Return task dict or None if not found."""
    target = task_path or TASK_FILE
    for t in _read_all(target):
        if t["task_id"] == task_id:
            return t
    return None


def list_tasks(
    status: str | None = None,
    *,
    task_path: Path | None = None,
) -> list[dict]:
    """Return all tasks, optionally filtered by status.

    Raises ValueError if status is not a valid status string.
    """
    if status is not None and status not in VALID_STATUSES:
        raise ValueError(f"invalid status {status!r}, must be one of {VALID_STATUSES}")
    target = task_path or TASK_FILE
    tasks = _read_all(target)
    if status is not None:
        tasks = [t for t in tasks if t["status"] == status]
    return tasks


def clear_tasks(*, task_path: Path | None = None) -> None:
    """Delete the task file. For testing only."""
    target = task_path or TASK_FILE
    if target.exists():
        target.unlink()
