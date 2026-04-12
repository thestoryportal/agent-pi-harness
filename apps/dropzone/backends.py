"""Multi-agent backend abstraction — Claude Code, Gemini CLI, Codex CLI stub."""

import subprocess
from dataclasses import dataclass
from pathlib import Path

from apps.dropzone.config import DropZoneConfig


@dataclass
class BackendResult:
    exit_code: int
    stdout: str
    stderr: str
    agent: str
    zone_name: str
    file_path: str


def run_claude_code(
    prompt: str,
    zone: DropZoneConfig,
    file_path: str,
) -> BackendResult:
    """Dispatch to Claude Code via CLI --print (fire-and-forget, no tmux)."""
    cmd = ["claude", "--print", "--model", zone.model]
    if zone.skip_permissions:
        cmd.insert(1, "--dangerously-skip-permissions")
    if zone.mcp_server_file and Path(zone.mcp_server_file).exists():
        cmd.extend(["--mcp-config", zone.mcp_server_file])
    cmd.append(prompt)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        return BackendResult(
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            agent="claude_code",
            zone_name=zone.name,
            file_path=file_path,
        )
    except subprocess.TimeoutExpired:
        return BackendResult(
            exit_code=-1, stdout="", stderr="timeout",
            agent="claude_code", zone_name=zone.name, file_path=file_path,
        )


def run_gemini_cli(
    prompt: str,
    zone: DropZoneConfig,
    file_path: str,
) -> BackendResult:
    """Dispatch to Gemini CLI via subprocess."""
    cmd = ["gemini", "--model", zone.model]
    if zone.skip_permissions:
        cmd.extend(["--yolo", "--sandbox"])
    cmd.append(prompt)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        return BackendResult(
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            agent="gemini_cli",
            zone_name=zone.name,
            file_path=file_path,
        )
    except subprocess.TimeoutExpired:
        return BackendResult(
            exit_code=-1, stdout="", stderr="timeout",
            agent="gemini_cli", zone_name=zone.name, file_path=file_path,
        )


def run_codex_cli(
    prompt: str,
    zone: DropZoneConfig,
    file_path: str,
) -> BackendResult:
    """Codex CLI stub — not yet implemented in source repo."""
    return BackendResult(
        exit_code=1, stdout="", stderr="codex_cli not implemented",
        agent="codex_cli", zone_name=zone.name, file_path=file_path,
    )


_BACKENDS = {
    "claude_code": run_claude_code,
    "gemini_cli": run_gemini_cli,
    "codex_cli": run_codex_cli,
}


def dispatch_backend(
    prompt: str,
    zone: DropZoneConfig,
    file_path: str,
) -> BackendResult:
    """Route to the correct agent backend based on zone config."""
    backend_fn = _BACKENDS.get(zone.agent)
    if backend_fn is None:
        raise ValueError(f"Unknown agent: {zone.agent}")

    return backend_fn(prompt, zone, file_path)
