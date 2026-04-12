"""Tests for apps.orchestrate.task_manager — three-state lifecycle with deps."""

import json

import pytest

from apps.orchestrate.task_manager import (
    claim_task,
    clear_tasks,
    complete_task,
    create_task,
    get_task,
    list_tasks,
)


def test_create_task_creates_file(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "first task", task_path=log)
    assert log.exists()
    lines = log.read_text().strip().split("\n")
    assert len(lines) == 1


def test_create_task_fields(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "first", metadata={"agent": "builder"}, task_path=log)
    entry = json.loads(log.read_text().strip())
    for key in ("task_id", "title", "status", "agent", "dependencies", "metadata", "created_at", "updated_at"):
        assert key in entry


def test_created_task_is_pending(tmp_path):
    log = tmp_path / "tasks.jsonl"
    task = create_task("t1", "first", task_path=log)
    assert task["status"] == "pending"
    assert task["agent"] is None


def test_duplicate_task_id_raises(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "first", task_path=log)
    with pytest.raises(ValueError, match="already exists"):
        create_task("t1", "duplicate", task_path=log)


def test_claim_task_transitions_to_in_progress(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "first", task_path=log)
    task = claim_task("t1", "builder", task_path=log)
    assert task["status"] == "in_progress"
    assert task["agent"] == "builder"


def test_claim_nonexistent_task_raises(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "first", task_path=log)
    with pytest.raises(ValueError, match="not found"):
        claim_task("ghost", "builder", task_path=log)


def test_claim_already_in_progress_raises(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "first", task_path=log)
    claim_task("t1", "builder", task_path=log)
    with pytest.raises(ValueError, match="not pending"):
        claim_task("t1", "builder", task_path=log)


def test_claim_blocked_by_dependency(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "dep", task_path=log)
    create_task("t2", "blocked", dependencies=["t1"], task_path=log)
    with pytest.raises(ValueError, match="not completed"):
        claim_task("t2", "builder", task_path=log)


def test_claim_allowed_after_dep_completed(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "dep", task_path=log)
    create_task("t2", "blocked", dependencies=["t1"], task_path=log)
    claim_task("t1", "builder", task_path=log)
    complete_task("t1", task_path=log)
    task = claim_task("t2", "builder", task_path=log)
    assert task["status"] == "in_progress"


def test_complete_task(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "first", task_path=log)
    claim_task("t1", "builder", task_path=log)
    task = complete_task("t1", task_path=log)
    assert task["status"] == "completed"


def test_complete_non_in_progress_raises(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "first", task_path=log)
    with pytest.raises(ValueError, match="not in_progress"):
        complete_task("t1", task_path=log)


def test_get_task_returns_dict(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "first", task_path=log)
    task = get_task("t1", task_path=log)
    assert task is not None
    assert task["task_id"] == "t1"


def test_get_nonexistent_returns_none(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "first", task_path=log)
    assert get_task("missing", task_path=log) is None


def test_list_tasks_all(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "a", task_path=log)
    create_task("t2", "b", task_path=log)
    create_task("t3", "c", task_path=log)
    assert len(list_tasks(task_path=log)) == 3


def test_list_tasks_filter_by_status(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "a", task_path=log)
    create_task("t2", "b", task_path=log)
    claim_task("t2", "builder", task_path=log)
    assert len(list_tasks("pending", task_path=log)) == 1
    assert len(list_tasks("in_progress", task_path=log)) == 1


def test_list_tasks_invalid_status_raises(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "a", task_path=log)
    with pytest.raises(ValueError, match="invalid status"):
        list_tasks("done", task_path=log)


def test_clear_tasks(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "a", task_path=log)
    assert log.exists()
    clear_tasks(task_path=log)
    assert not log.exists()


def test_updated_at_changes_on_transition(tmp_path):
    log = tmp_path / "tasks.jsonl"
    task = create_task("t1", "first", task_path=log)
    created = task["updated_at"]
    claimed = claim_task("t1", "builder", task_path=log)
    assert claimed["updated_at"] >= created


def test_invalid_task_id_raises(tmp_path):
    log = tmp_path / "tasks.jsonl"
    with pytest.raises(ValueError, match="invalid task_id"):
        create_task("../../bad", "hack", task_path=log)


def test_invalid_agent_raises(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "first", task_path=log)
    with pytest.raises(ValueError, match="invalid agent"):
        claim_task("t1", "../../bad", task_path=log)


def test_metadata_persisted(tmp_path):
    log = tmp_path / "tasks.jsonl"
    create_task("t1", "first", metadata={"priority": "high"}, task_path=log)
    task = get_task("t1", task_path=log)
    assert task is not None
    assert task["metadata"] == {"priority": "high"}
