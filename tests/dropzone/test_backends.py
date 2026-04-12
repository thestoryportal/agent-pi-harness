import subprocess

import pytest

from apps.dropzone.backends import (
    BackendResult,
    dispatch_backend,
    run_claude_code,
    run_gemini_cli,
)
from apps.dropzone.config import DropZoneConfig


def _zone(**overrides) -> DropZoneConfig:
    return DropZoneConfig(
        name=overrides.get("name", "Test Zone"),
        file_patterns=overrides.get("file_patterns", ["*.txt"]),
        reusable_prompt=overrides.get("reusable_prompt", "x"),
        zone_dirs=overrides.get("zone_dirs", ["/tmp"]),
        events=overrides.get("events", ["created"]),
        agent=overrides.get("agent", "claude_code"),
        model=overrides.get("model", "sonnet"),
        mcp_server_file=overrides.get("mcp_server_file"),
        create_zone_dir_if_not_exists=overrides.get("create_zone_dir_if_not_exists", True),
        skip_permissions=overrides.get("skip_permissions", False),
    )


def test_dispatch_codex_stub():
    zone = _zone(agent="codex_cli")
    r = dispatch_backend("prompt", zone, "/tmp/file.txt")
    assert r.exit_code == 1
    assert "not implemented" in r.stderr
    assert r.agent == "codex_cli"


def test_dispatch_unknown_agent_raises():
    zone = _zone(agent="bogus")
    with pytest.raises(ValueError, match="bogus"):
        dispatch_backend("prompt", zone, "/tmp/x")


def test_backend_result_fields():
    r = BackendResult(
        exit_code=0, stdout="ok", stderr="",
        agent="claude_code", zone_name="Z", file_path="/x",
    )
    assert r.exit_code == 0
    assert r.stdout == "ok"
    assert r.agent == "claude_code"


def test_run_claude_code_subprocess(monkeypatch):
    zone = _zone()
    mock_result = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="done", stderr="",
    )
    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: mock_result)
    r = run_claude_code("prompt", zone, "/tmp/x.txt")
    assert r.exit_code == 0
    assert r.stdout == "done"


def test_run_gemini_cli_subprocess(monkeypatch):
    zone = _zone(agent="gemini_cli")
    mock_result = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="gemini ok", stderr="",
    )
    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: mock_result)
    r = run_gemini_cli("prompt", zone, "/tmp/x.txt")
    assert r.exit_code == 0
    assert r.stdout == "gemini ok"


def test_run_claude_code_timeout(monkeypatch):
    zone = _zone()

    def raise_timeout(*a, **kw):
        raise subprocess.TimeoutExpired(cmd=[], timeout=1)

    monkeypatch.setattr(subprocess, "run", raise_timeout)
    r = run_claude_code("prompt", zone, "/tmp/x.txt")
    assert r.exit_code == -1
    assert "timeout" in r.stderr


def test_run_gemini_cli_timeout(monkeypatch):
    zone = _zone(agent="gemini_cli")

    def raise_timeout(*a, **kw):
        raise subprocess.TimeoutExpired(cmd=[], timeout=1)

    monkeypatch.setattr(subprocess, "run", raise_timeout)
    r = run_gemini_cli("prompt", zone, "/tmp/x.txt")
    assert r.exit_code == -1
    assert "timeout" in r.stderr


def test_skip_permissions_adds_flag(monkeypatch):
    zone = _zone(skip_permissions=True)
    captured_cmds: list[list[str]] = []

    def capture_run(cmd, **kw):
        captured_cmds.append(cmd)
        return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")

    monkeypatch.setattr(subprocess, "run", capture_run)
    run_claude_code("prompt", zone, "/tmp/x.txt")
    assert "--dangerously-skip-permissions" in captured_cmds[0]


def test_no_skip_permissions_by_default(monkeypatch):
    zone = _zone()
    captured_cmds: list[list[str]] = []

    def capture_run(cmd, **kw):
        captured_cmds.append(cmd)
        return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")

    monkeypatch.setattr(subprocess, "run", capture_run)
    run_claude_code("prompt", zone, "/tmp/x.txt")
    assert "--dangerously-skip-permissions" not in captured_cmds[0]
