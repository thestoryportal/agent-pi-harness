#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Claude Code Setup Hook: Maintenance Mode

Triggered by: claude --maintenance
Purpose: Update app dependencies, prune logs, validate patterns.yaml, verify hook health
"""

import sys

# Early exit for health-check probe (session_start.py health scan)
if "--health-check" in sys.argv:
    print("OK:setup_maintenance.py")
    sys.exit(0)

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

import yaml

LOG_FILE = Path(__file__).parent / "setup.maintenance.log"
PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

# Keep in sync with session_start.py REQUIRED_HOOKS
REQUIRED_HOOKS = [
    "session_start.py", "setup_init.py", "setup_maintenance.py",
    "pre_tool_use.py", "post_tool_use.py",
    "notification.py", "stop.py", "user_prompt_submit.py", "pre_compact.py",
    "subagent_start.py", "subagent_stop.py", "session_end.py",
    "permission_request.py", "post_tool_use_failure.py",
    str(Path(PROJECT_DIR) / ".claude/skills/damage-control/hooks/damage-control-python/bash_damage_control.py"),
    str(Path(PROJECT_DIR) / ".claude/skills/damage-control/hooks/damage-control-python/edit_damage_control.py"),
    str(Path(PROJECT_DIR) / ".claude/skills/damage-control/hooks/damage-control-python/write_damage_control.py"),
]


def log(msg: str) -> None:
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")


def run(cmd: list[str], cwd: str | None = None) -> bool:
    log(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        for line in result.stdout.strip().split("\n")[:5]:
            log(f"    {line}")
    if result.returncode != 0:
        log(f"  ERROR: exit code {result.returncode}")
        if result.stderr:
            log(f"  {result.stderr[:200]}")
    return result.returncode == 0


def main() -> None:
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        hook_input = {}

    log(f"\n{'='*60}")
    log(f"=== Maintenance Hook: {datetime.now().isoformat()} ===")
    log(f"{'='*60}")
    log(f"INPUT: {json.dumps(hook_input, indent=2)}")
    log(f"Project: {PROJECT_DIR}")

    actions: list[str] = []
    errors: list[str] = []

    # 1. Update per-app Python dependencies
    log("\n>>> Updating app dependencies...")
    apps_dir = Path(PROJECT_DIR) / "apps"
    app_dirs = sorted(p.parent for p in apps_dir.glob("*/pyproject.toml") if p.parent.is_dir())
    for app_dir in app_dirs:
        log(f"\n  App: {app_dir.name}")
        if run(["uv", "sync", "--upgrade"], cwd=str(app_dir)):
            actions.append(f"Updated {app_dir.name} dependencies")
        else:
            errors.append(f"{app_dir.name}: uv sync failed")

    # 2. Prune observe logs
    log("\n>>> Pruning observe logs...")
    prune_script = Path(PROJECT_DIR) / "apps" / "observe" / "prune.py"
    if prune_script.exists():
        if run(["uv", "run", str(prune_script)], cwd=PROJECT_DIR):
            actions.append("Pruned observe events.jsonl")
        else:
            errors.append("observe prune failed")
    else:
        log("  apps/observe/prune.py not found — skipping")

    # 3. Validate damage-control patterns.yaml
    log("\n>>> Validating patterns.yaml...")
    patterns_path = Path(PROJECT_DIR) / ".claude/skills/damage-control/patterns.yaml"
    if patterns_path.exists():
        try:
            yaml.safe_load(patterns_path.read_text())
            log("  patterns.yaml: valid")
            actions.append("Validated patterns.yaml (syntactically valid YAML)")
        except yaml.YAMLError as exc:
            log(f"  patterns.yaml INVALID: {exc}")
            errors.append(f"patterns.yaml syntax error: {exc}")
    else:
        log("  patterns.yaml not found")
        errors.append("patterns.yaml missing")

    # 4. Hook health check
    log("\n>>> Verifying hook health...")
    hooks_dir = Path(PROJECT_DIR) / ".claude" / "hooks"
    hook_failures: list[str] = []
    for hook_name in REQUIRED_HOOKS:
        hook_file = hooks_dir / hook_name
        if not hook_file.exists():
            hook_failures.append(f"MISSING: {hook_name}")
            log(f"  MISSING: {hook_name}")
            continue
        if not os.access(hook_file, os.X_OK):
            hook_failures.append(f"NOT_EXECUTABLE: {hook_file.name}")
            log(f"  NOT EXECUTABLE: {hook_file.name}")
            continue
        try:
            result = subprocess.run(
                ["uv", "run", str(hook_file), "--health-check"],
                capture_output=True, text=True, timeout=10,
                env={**os.environ, "CLAUDE_PROJECT_DIR": PROJECT_DIR},
            )
            if result.returncode != 0:
                hook_failures.append(f"FAIL: {hook_file.name}")
                log(f"  FAIL: {hook_file.name} (exit {result.returncode})")
            else:
                log(f"  OK: {hook_file.name}")
        except subprocess.TimeoutExpired:
            hook_failures.append(f"TIMEOUT: {hook_file.name}")
            log(f"  TIMEOUT: {hook_file.name}")

    if hook_failures:
        errors.extend(hook_failures)
    else:
        actions.append(f"All {len(REQUIRED_HOOKS)} hooks passed health check")

    # Build output
    summary = "Maintenance completed!\n\nActions:\n"
    for action in actions:
        summary += f"  - {action}\n"
    if errors:
        summary += "\nErrors:\n"
        for error in errors:
            summary += f"  - {error}\n"

    output = {
        "hookSpecificOutput": {
            "hookEventName": "Setup",
            "additionalContext": summary,
        }
    }

    log(f"\nOUTPUT: {json.dumps(output, indent=2)}")
    log(f"=== Completed: {datetime.now().isoformat()} ===")

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except BaseException as exc:
        with open(LOG_FILE, "a") as f:
            f.write(f"CRASH (fail-open): {type(exc).__name__}: {exc}\n")
        sys.exit(1)
