import os
from unittest.mock import MagicMock

from rich.console import Console

from apps.dropzone.backends import BackendResult
from apps.dropzone.config import DropZoneConfig
from apps.dropzone.watcher import (
    DropZoneEventHandler,
    archive_file,
    is_within_zone,
    matches_pattern,
)


def _zone(**overrides) -> DropZoneConfig:
    return DropZoneConfig(
        name=overrides.get("name", "Test Zone"),
        file_patterns=overrides.get("file_patterns", ["*.txt"]),
        reusable_prompt=overrides.get("reusable_prompt", "prompt.md"),
        zone_dirs=overrides.get("zone_dirs", ["/tmp/zone"]),
        events=overrides.get("events", ["created"]),
        agent=overrides.get("agent", "claude_code"),
        model=overrides.get("model", "sonnet"),
        mcp_server_file=overrides.get("mcp_server_file"),
        create_zone_dir_if_not_exists=overrides.get("create_zone_dir_if_not_exists", True),
        skip_permissions=overrides.get("skip_permissions", False),
    )


def test_matches_pattern_txt():
    assert matches_pattern("report.txt", ["*.txt"]) is True


def test_matches_pattern_no_match():
    assert matches_pattern("report.csv", ["*.txt", "*.md"]) is False


def test_matches_pattern_multiple_patterns():
    assert matches_pattern("README.md", ["*.txt", "*.md"]) is True


def test_archive_file_moves_file(tmp_path):
    zone_dir = tmp_path / "zone"
    zone_dir.mkdir()
    f = zone_dir / "test.txt"
    f.write_text("hello")
    dest = archive_file(f)
    assert dest == zone_dir / "archive" / "test.txt"
    assert dest.exists()
    assert not f.exists()


def test_archive_file_creates_archive_dir(tmp_path):
    zone_dir = tmp_path / "zone"
    zone_dir.mkdir()
    f = zone_dir / "data.csv"
    f.write_text("a,b,c")
    archive_file(f)
    assert (zone_dir / "archive").is_dir()


def test_event_handler_ignores_directory_events(monkeypatch):
    zone = _zone()
    console = Console(quiet=True)
    handler = DropZoneEventHandler(zone, console)
    event = MagicMock()
    event.is_directory = True

    # Patch dispatch_backend to track calls
    calls = []
    monkeypatch.setattr(
        "apps.dropzone.watcher.dispatch_backend",
        lambda *a, **kw: calls.append(1),
    )
    handler.on_created(event)
    assert len(calls) == 0


def test_event_handler_ignores_pattern_mismatch(monkeypatch):
    zone = _zone(file_patterns=["*.txt"])
    console = Console(quiet=True)
    handler = DropZoneEventHandler(zone, console)
    event = MagicMock()
    event.is_directory = False
    event.src_path = "/tmp/zone/file.csv"

    calls = []
    monkeypatch.setattr(
        "apps.dropzone.watcher.dispatch_backend",
        lambda *a, **kw: calls.append(1),
    )
    handler.on_created(event)
    assert len(calls) == 0


def test_event_handler_ignores_wrong_event_type(monkeypatch):
    zone = _zone(events=["created"])
    console = Console(quiet=True)
    handler = DropZoneEventHandler(zone, console)
    event = MagicMock()
    event.is_directory = False
    event.src_path = "/tmp/zone/file.txt"

    calls = []
    monkeypatch.setattr(
        "apps.dropzone.watcher.dispatch_backend",
        lambda *a, **kw: calls.append(1),
    )
    handler.on_modified(event)
    assert len(calls) == 0


def test_event_handler_rejects_symlink(tmp_path, monkeypatch):
    zone_dir = tmp_path / "zone"
    zone_dir.mkdir()
    target = zone_dir / "real.txt"
    target.write_text("real content")
    link = zone_dir / "link.txt"
    os.symlink(str(target), str(link))

    zone = _zone(zone_dirs=[str(zone_dir)])
    console = Console(quiet=True)
    handler = DropZoneEventHandler(zone, console)
    event = MagicMock()
    event.is_directory = False
    event.src_path = str(link)

    calls: list[object] = []
    monkeypatch.setattr(
        "apps.dropzone.watcher.dispatch_backend",
        lambda *a, **kw: calls.append(1),
    )
    handler.on_created(event)
    assert len(calls) == 0


def test_is_within_zone(tmp_path):
    zone_dir = tmp_path / "zone"
    zone_dir.mkdir()
    inside = zone_dir / "file.txt"
    inside.write_text("x")
    assert is_within_zone(inside, [str(zone_dir)]) is True

    outside = tmp_path / "other.txt"
    outside.write_text("x")
    assert is_within_zone(outside, [str(zone_dir)]) is False


def test_event_handler_happy_path_dispatches(tmp_path, monkeypatch):
    zone_dir = tmp_path / "zone"
    zone_dir.mkdir()
    prompt_file = tmp_path / "prompt.md"
    prompt_file.write_text("Process {FILE_PATH}")
    f = zone_dir / "test.txt"
    f.write_text("content")

    zone = _zone(zone_dirs=[str(zone_dir)], reusable_prompt=str(prompt_file))
    console = Console(quiet=True)
    handler = DropZoneEventHandler(zone, console)

    event = MagicMock()
    event.is_directory = False
    event.src_path = str(f)

    mock_result = BackendResult(
        exit_code=0, stdout="ok", stderr="",
        agent="claude_code", zone_name="Test Zone", file_path=str(f),
    )
    dispatched: list[str] = []

    def mock_dispatch(prompt, z, fp):
        dispatched.append(prompt)
        return mock_result

    monkeypatch.setattr("apps.dropzone.watcher.dispatch_backend", mock_dispatch)
    handler.on_created(event)

    assert len(dispatched) == 1
    assert str(f.resolve()) in dispatched[0]
    # File should be archived
    assert not f.exists()
    assert (zone_dir / "archive" / "test.txt").exists()
