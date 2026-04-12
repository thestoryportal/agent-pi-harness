"""Tests for apps.orchestrate.update_log — chronological JSONL update log."""

import json

from apps.orchestrate.update_log import append_update, clear_log, read_updates


def test_append_creates_file(tmp_path):
    log = tmp_path / "updates.jsonl"
    append_update("j1", "pending", "start", log_path=log)
    assert log.exists()
    lines = log.read_text().strip().split("\n")
    assert len(lines) == 1


def test_append_is_valid_json(tmp_path):
    log = tmp_path / "updates.jsonl"
    append_update("j1", "pending", "start", log_path=log)
    entry = json.loads(log.read_text().strip())
    for key in ("job_id", "status", "message", "timestamp", "metadata"):
        assert key in entry


def test_append_is_chronological(tmp_path):
    log = tmp_path / "updates.jsonl"
    append_update("j1", "pending", "created", log_path=log)
    append_update("j1", "in_progress", "claimed", log_path=log)
    append_update("j1", "completed", "done", log_path=log)
    entries = read_updates("j1", log_path=log)
    assert len(entries) == 3
    assert entries[0]["status"] == "pending"
    assert entries[1]["status"] == "in_progress"
    assert entries[2]["status"] == "completed"


def test_filter_by_job_id(tmp_path):
    log = tmp_path / "updates.jsonl"
    append_update("j1", "pending", "a", log_path=log)
    append_update("j2", "pending", "b", log_path=log)
    entries = read_updates("j1", log_path=log)
    assert len(entries) == 1
    assert entries[0]["job_id"] == "j1"


def test_read_all_no_filter(tmp_path):
    log = tmp_path / "updates.jsonl"
    append_update("j1", "pending", "a", log_path=log)
    append_update("j2", "pending", "b", log_path=log)
    entries = read_updates(log_path=log)
    assert len(entries) == 2


def test_malformed_line_skipped(tmp_path):
    log = tmp_path / "updates.jsonl"
    log.write_text("not valid json\n")
    append_update("j1", "pending", "ok", log_path=log)
    entries = read_updates(log_path=log)
    assert len(entries) == 1
    assert entries[0]["job_id"] == "j1"


def test_read_nonexistent_file(tmp_path):
    log = tmp_path / "nonexistent.jsonl"
    entries = read_updates(log_path=log)
    assert entries == []


def test_metadata_persisted(tmp_path):
    log = tmp_path / "updates.jsonl"
    append_update("j1", "pending", "start", {"agent": "builder"}, log_path=log)
    entries = read_updates(log_path=log)
    assert entries[0]["metadata"] == {"agent": "builder"}


def test_clear_log(tmp_path):
    log = tmp_path / "updates.jsonl"
    append_update("j1", "pending", "start", log_path=log)
    assert log.exists()
    clear_log(log_path=log)
    assert not log.exists()
