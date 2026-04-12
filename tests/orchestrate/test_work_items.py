"""Tests for apps.orchestrate.work_items — YAML work item discovery."""

import yaml

from apps.orchestrate.work_items import discover_work_items


def _write_yaml(path, data):
    path.write_text(yaml.dump(data))


def test_discovers_items_from_yaml(tmp_path):
    _write_yaml(tmp_path / "tasks.yaml", {"items": [{"name": "x"}]})
    result = discover_work_items(tmp_path)
    assert len(result) == 1
    assert result[0]["name"] == "x"


def test_flat_list_across_files(tmp_path):
    _write_yaml(tmp_path / "a.yaml", {"items": [{"n": 1}, {"n": 2}]})
    _write_yaml(tmp_path / "b.yaml", {"items": [{"n": 3}, {"n": 4}]})
    result = discover_work_items(tmp_path)
    assert len(result) == 4


def test_source_file_injected(tmp_path):
    _write_yaml(tmp_path / "tasks.yaml", {"items": [{"name": "x"}]})
    result = discover_work_items(tmp_path)
    assert "source_file" in result[0]
    assert "tasks.yaml" in result[0]["source_file"]


def test_filename_filter(tmp_path):
    _write_yaml(tmp_path / "deploy.yaml", {"items": [{"n": 1}]})
    _write_yaml(tmp_path / "config.yaml", {"items": [{"n": 2}]})
    result = discover_work_items(tmp_path, filename_filter="deploy")
    assert len(result) == 1
    assert result[0]["n"] == 1


def test_skips_unparseable_file(tmp_path, capsys):
    (tmp_path / "bad.yaml").write_text(": : : invalid")
    _write_yaml(tmp_path / "good.yaml", {"items": [{"n": 1}]})
    result = discover_work_items(tmp_path)
    assert len(result) == 1
    captured = capsys.readouterr()
    assert "WARNING" in captured.err


def test_no_items_key_skipped(tmp_path):
    _write_yaml(tmp_path / "config.yaml", {"foo": "bar"})
    result = discover_work_items(tmp_path)
    assert result == []


def test_empty_dir_returns_empty(tmp_path):
    result = discover_work_items(tmp_path)
    assert result == []


def test_filter_no_match_returns_empty(tmp_path):
    _write_yaml(tmp_path / "a.yaml", {"items": [{"n": 1}]})
    result = discover_work_items(tmp_path, filename_filter="z")
    assert result == []


def test_nonexistent_dir_returns_empty(tmp_path):
    result = discover_work_items(tmp_path / "nonexistent")
    assert result == []


def test_non_dict_items_skipped(tmp_path):
    _write_yaml(tmp_path / "mixed.yaml", {"items": [{"n": 1}, "bare_string", 42]})
    result = discover_work_items(tmp_path)
    assert len(result) == 1
    assert result[0]["n"] == 1
