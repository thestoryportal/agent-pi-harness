#!/usr/bin/env python3
"""run-claude.py — Python wrapper for programmatic Claude Code invocation.

Called from an external orchestrator via subprocess. Handles subprocess management,
JSON parsing, error handling, timeout enforcement, and cost logging.

Usage:
    python3 scripts/run-claude.py \
        --prompt "Review the diff against SPEC-H02" \
        --tools Read Grep Glob \
        --system-prompt "project=arhugula task=code-review" \
        --timeout 120 \
        --max-turns 10

    # Or from Python:
    from run_claude import run_claude
    result = run_claude(
        prompt="Review the diff against SPEC-H02",
        tools=["Read", "Grep", "Glob"],
        permission_mode="dontAsk",
        timeout=120,
    )
"""

import json
import logging
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("run_claude")

CLAUDE_BINARY = "claude"
DEFAULT_TIMEOUT = 120
DEFAULT_MAX_TURNS = 10
PROJECT_DIR = Path(__file__).resolve().parent.parent


@dataclass
class ClaudeResult:
    success: bool
    result_text: str
    cost_usd: float
    duration_ms: int
    duration_api_ms: int
    num_turns: int
    session_id: str
    subtype: str
    raw_json: dict = field(default_factory=dict)
    error_message: Optional[str] = None


@dataclass
class InvocationConfig:
    prompt: str
    tools: list[str]
    auto_approved_tools: list[str] = field(default_factory=list)
    system_prompt: str = ""
    permission_mode: Optional[str] = None
    use_bare: bool = True
    timeout: int = DEFAULT_TIMEOUT
    max_turns: int = DEFAULT_MAX_TURNS
    model: Optional[str] = None
    working_directory: Optional[str] = None


SANDBOX_PRESETS = {
    "read_only": ["Read", "Grep", "Glob"],
    "content_write": ["Read", "Grep", "Glob", "Write", "Edit"],
    "migration": ["Read", "Grep", "Glob", "Write", "Edit", "Bash"],
    "full": ["Read", "Grep", "Glob", "Write", "Edit", "Bash"],
}


def run_claude(
    prompt: str,
    tools: list[str],
    auto_approved_tools: Optional[list[str]] = None,
    system_prompt: str = "",
    permission_mode: Optional[str] = None,
    use_bare: bool = True,
    timeout: int = DEFAULT_TIMEOUT,
    max_turns: int = DEFAULT_MAX_TURNS,
    model: Optional[str] = None,
    working_directory: Optional[str] = None,
) -> ClaudeResult:
    config = InvocationConfig(
        prompt=prompt,
        tools=tools,
        auto_approved_tools=auto_approved_tools or [],
        system_prompt=system_prompt,
        permission_mode=permission_mode,
        use_bare=use_bare,
        timeout=timeout,
        max_turns=max_turns,
        model=model,
        working_directory=working_directory,
    )

    cmd = _build_command(config)
    cwd = config.working_directory or str(PROJECT_DIR)

    logger.info(
        "Invoking: tools=%s, mode=%s, bare=%s, timeout=%ds, max_turns=%d",
        config.tools, config.permission_mode, config.use_bare,
        config.timeout, config.max_turns,
    )

    start_time = time.monotonic()

    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=config.timeout, cwd=cwd,
        )
    except subprocess.TimeoutExpired as e:
        elapsed = time.monotonic() - start_time
        logger.error("Timed out after %.1fs", elapsed)
        return ClaudeResult(
            success=False, result_text="", cost_usd=0.0,
            duration_ms=int(elapsed * 1000), duration_api_ms=0,
            num_turns=0, session_id="", subtype="error_timeout",
            error_message=f"Timed out after {config.timeout}s. stderr: {(e.stderr or '')[:500]}",
        )
    except FileNotFoundError:
        logger.error("Claude binary not found: %s", CLAUDE_BINARY)
        return ClaudeResult(
            success=False, result_text="", cost_usd=0.0,
            duration_ms=0, duration_api_ms=0,
            num_turns=0, session_id="", subtype="error_binary_not_found",
            error_message=f"Claude binary '{CLAUDE_BINARY}' not found on PATH",
        )

    elapsed_ms = int((time.monotonic() - start_time) * 1000)

    if proc.returncode != 0:
        logger.error("Exit code %d. stderr: %s", proc.returncode, proc.stderr[:500])
        return ClaudeResult(
            success=False, result_text=proc.stdout[:2000], cost_usd=0.0,
            duration_ms=elapsed_ms, duration_api_ms=0,
            num_turns=0, session_id="", subtype=f"error_exit_{proc.returncode}",
            error_message=f"Exit code {proc.returncode}: {proc.stderr[:500]}",
        )

    return _parse_output(proc.stdout, elapsed_ms)


def _build_command(config: InvocationConfig) -> list[str]:
    cmd = [CLAUDE_BINARY]

    if config.use_bare:
        cmd.append("--bare")

    cmd.extend([
        "-p", config.prompt,
        "--output-format", "json",
        "--max-turns", str(config.max_turns),
    ])

    if config.tools:
        cmd.extend(["--tools", ",".join(config.tools)])

    if config.auto_approved_tools:
        cmd.append("--allowedTools")
        cmd.extend(config.auto_approved_tools)

    if config.permission_mode:
        cmd.extend(["--permission-mode", config.permission_mode])

    if config.system_prompt:
        cmd.extend(["--append-system-prompt", config.system_prompt])

    if config.model:
        cmd.extend(["--model", config.model])

    return cmd


def _parse_output(stdout: str, elapsed_ms: int) -> ClaudeResult:
    stdout = stdout.strip()

    if not stdout:
        return ClaudeResult(
            success=False, result_text="", cost_usd=0.0,
            duration_ms=elapsed_ms, duration_api_ms=0,
            num_turns=0, session_id="", subtype="error_empty_output",
            error_message="Claude Code returned empty output",
        )

    try:
        data = json.loads(stdout)
    except json.JSONDecodeError as e:
        return ClaudeResult(
            success=False, result_text=stdout[:2000], cost_usd=0.0,
            duration_ms=elapsed_ms, duration_api_ms=0,
            num_turns=0, session_id="", subtype="error_json_parse",
            error_message=f"JSON parse error: {e}",
        )

    is_error = data.get("is_error", False)

    return ClaudeResult(
        success=not is_error,
        result_text=data.get("result", ""),
        cost_usd=data.get("cost_usd", 0.0),
        duration_ms=data.get("duration_ms", elapsed_ms),
        duration_api_ms=data.get("duration_api_ms", 0),
        num_turns=data.get("num_turns", 0),
        session_id=data.get("session_id", ""),
        subtype=data.get("subtype", "unknown"),
        raw_json=data,
        error_message=data.get("result", "") if is_error else None,
    )


def log_cost(result: ClaudeResult, workflow_id: str, invocation_type: str) -> None:
    """Log invocation cost to JSONL file for observability."""
    log_dir = PROJECT_DIR / ".claude" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "invocations.jsonl"

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "workflow_id": workflow_id,
        "invocation_type": invocation_type,
        "cost_usd": result.cost_usd,
        "duration_ms": result.duration_ms,
        "duration_api_ms": result.duration_api_ms,
        "num_turns": result.num_turns,
        "session_id": result.session_id,
        "success": result.success,
        "error_message": result.error_message,
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")

    logger.info(
        "Cost logged: $%.6f for %s/%s (session=%s)",
        result.cost_usd, workflow_id, invocation_type, result.session_id,
    )


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Invoke Claude Code programmatically")
    parser.add_argument("--prompt", required=True, help="Task prompt")
    parser.add_argument("--tools", nargs="+", required=True, help="Allowed tools")
    parser.add_argument("--approved-tools", nargs="*", default=None, help="Auto-approved tools")
    parser.add_argument("--system-prompt", default="", help="Per-job context")
    parser.add_argument("--permission-mode", default=None, help="Permission mode (dontAsk, acceptEdits, etc.)")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Timeout in seconds")
    parser.add_argument("--max-turns", type=int, default=DEFAULT_MAX_TURNS, help="Max agentic turns")
    parser.add_argument("--model", default=None, help="Model override")
    parser.add_argument("--working-directory", default=None, help="Working directory")
    parser.add_argument("--workflow-id", default="manual", help="Workflow ID for cost tracking")
    parser.add_argument("--invocation-type", default="manual", help="Invocation type for cost tracking")
    parser.add_argument("--preset", choices=list(SANDBOX_PRESETS.keys()), help="Tool preset")

    args = parser.parse_args()

    tools = SANDBOX_PRESETS[args.preset] if args.preset else args.tools

    result = run_claude(
        prompt=args.prompt,
        tools=tools,
        auto_approved_tools=args.approved_tools,
        system_prompt=args.system_prompt,
        permission_mode=args.permission_mode,
        timeout=args.timeout,
        max_turns=args.max_turns,
        model=args.model,
        working_directory=args.working_directory,
    )

    log_cost(result, args.workflow_id, args.invocation_type)

    print(json.dumps(asdict(result), indent=2))
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
