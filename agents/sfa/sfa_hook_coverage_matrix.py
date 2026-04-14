#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "rich>=13.7.0",
#   "pyyaml>=6.0.0",
# ]
# ///

"""
sfa_hook_coverage_matrix.py — Phase 3 Check 2: subagent hook coverage

Walks `.claude/settings.json` + every `.claude/agents/*.md` subagent definition
and builds a matrix of which project-level hooks actually cover which subagent
spawn points. Flags coverage gaps — specifically the SP15 Exception 29 #3
pattern where a sandboxed fork subagent runs Bash outside damage-control.

This is a mechanical tool — no LLM calls.

Usage:
    uv run agents/sfa/sfa_hook_coverage_matrix.py \\
        --settings .claude/settings.json \\
        --agents-dir .claude/agents \\
        --output audits/phase3-hook-coverage-2026-04-14.md

Exit codes:
    0 = every subagent inherits the project-level security hooks, no gaps
    1 = coverage gap(s) detected
    2 = setup error
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set

import yaml
from rich.console import Console
from rich.table import Table

console = Console()

SECURITY_HOOK_EVENTS = {"PreToolUse", "PermissionRequest", "PostToolUseFailure"}


def load_settings(settings_path: Path) -> Dict:
    return json.loads(settings_path.read_text())


def build_hook_matrix(settings: Dict) -> Dict[str, List[Dict]]:
    """Return {event_name: [{matcher, command}, ...]} for every hook event."""
    matrix: Dict[str, List[Dict]] = {}
    for event, hook_blocks in settings.get("hooks", {}).items():
        rows: List[Dict] = []
        for block in hook_blocks:
            matcher = block.get("matcher", "*")
            for hook in block.get("hooks", []):
                rows.append(
                    {
                        "matcher": matcher,
                        "type": hook.get("type", "command"),
                        "command": hook.get("command", ""),
                    }
                )
        matrix[event] = rows
    return matrix


def parse_agent(path: Path) -> Dict:
    """Parse a subagent .md file — return frontmatter + system prompt excerpt."""
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not m:
        return {"name": path.stem, "error": "no frontmatter", "body": text}
    try:
        frontmatter = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        return {"name": path.stem, "error": f"yaml parse error: {exc}", "body": m.group(2)}
    body = m.group(2)
    return {
        "name": frontmatter.get("name", path.stem),
        "description": frontmatter.get("description", ""),
        "tools": frontmatter.get("tools") or [],
        "disallowed": frontmatter.get("disallowedTools") or [],
        "model": frontmatter.get("model", ""),
        "permission_mode": frontmatter.get("permissionMode", ""),
        "max_turns": frontmatter.get("maxTurns"),
        "body": body,
        "path": str(path),
    }


def collect_agents(agents_dir: Path) -> List[Dict]:
    agents: List[Dict] = []
    for md in sorted(agents_dir.rglob("*.md")):
        if md.name.upper() == "CLAUDE.MD":
            continue
        agents.append(parse_agent(md))
    return agents


def classify_agent(agent: Dict, hook_matrix: Dict) -> Dict:
    """Determine which hooks cover this agent's tool surface + flag gaps."""
    name = agent.get("name", "unknown")
    tools = set(agent.get("tools") or [])
    disallowed = set(agent.get("disallowed") or [])

    has_bash = "Bash" in tools and "Bash" not in disallowed
    has_write = any(t in tools for t in ("Write", "Edit", "NotebookEdit")) and not all(
        t in disallowed for t in ("Write", "Edit", "NotebookEdit")
    )
    has_read = "Read" in tools and "Read" not in disallowed

    pre_tool_hooks = hook_matrix.get("PreToolUse", [])
    covers_bash = any(
        ("bash" in h["matcher"].lower() if h.get("matcher") else False)
        or "bash_damage_control" in h.get("command", "")
        for h in pre_tool_hooks
    )
    covers_write = any(
        "write" in h["matcher"].lower() or "edit" in h["matcher"].lower()
        if h.get("matcher")
        else False
        for h in pre_tool_hooks
    ) or any("edit_damage_control" in h["command"] or "write_damage_control" in h["command"] for h in pre_tool_hooks)

    # A hook without a matcher (empty string) applies to all events of that type
    generic_pretooluse = any(
        (h.get("matcher", "") in ("", "*"))
        and "pre_tool_use" in h.get("command", "").lower()
        for h in pre_tool_hooks
    )

    notes: List[str] = []
    gap: Optional[str] = None

    if has_bash and not covers_bash and not generic_pretooluse:
        gap = "Bash outside damage-control"
        notes.append("Bash enabled, no PreToolUse matcher protecting it")
    elif has_bash and generic_pretooluse and not covers_bash:
        notes.append("Bash covered by generic PreToolUse only (no bash_damage_control)")

    if has_write and not covers_write and not generic_pretooluse:
        if gap is None:
            gap = "Write/Edit outside damage-control"
        notes.append("Write/Edit/NotebookEdit enabled, no matcher protecting it")

    if not tools and not disallowed:
        notes.append("no tools/disallowedTools frontmatter — inherits defaults")

    return {
        "name": name,
        "path": agent.get("path", ""),
        "tools": sorted(tools),
        "disallowed": sorted(disallowed),
        "model": agent.get("model", ""),
        "permission_mode": agent.get("permission_mode", ""),
        "max_turns": agent.get("max_turns"),
        "has_bash": has_bash,
        "has_write": has_write,
        "has_read": has_read,
        "covers_bash": covers_bash,
        "covers_write": covers_write,
        "generic_pretooluse": generic_pretooluse,
        "gap": gap,
        "notes": notes,
    }


def render_report(
    agents: List[Dict],
    assessments: List[Dict],
    hook_matrix: Dict,
    output: Path,
    settings_path: Path,
    agents_dir: Path,
) -> Dict[str, int]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    gaps = [a for a in assessments if a.get("gap")]
    clean = [a for a in assessments if not a.get("gap")]

    lines: List[str] = [
        "# Phase 3 Check 2 — Subagent Hook Coverage Matrix",
        "",
        f"**Date:** {now}",
        f"**Settings:** `{settings_path}`",
        f"**Agents dir:** `{agents_dir}`",
        f"**Subagents audited:** {len(assessments)}",
        f"**Coverage gaps:** {len(gaps)}",
        "",
        "## Project-level hook matrix",
        "",
        "| Event | Matcher | Command |",
        "|---|---|---|",
    ]
    for event in sorted(hook_matrix.keys()):
        for hook in hook_matrix[event]:
            matcher = hook["matcher"] or "(any)"
            command = hook["command"]
            if len(command) > 100:
                command = command[:97] + "..."
            lines.append(f"| {event} | `{matcher}` | `{command}` |")
    lines.append("")

    if gaps:
        lines.append("## ❌ Coverage gaps")
        lines.append("")
        lines.append("| Subagent | Gap | Tools | Model | PermissionMode |")
        lines.append("|---|---|---|---|---|")
        for a in gaps:
            tools = ", ".join(a["tools"]) if a["tools"] else "(inherited)"
            lines.append(
                f"| `{a['name']}` | {a['gap']} | {tools} | "
                f"{a['model'] or '(default)'} | {a['permission_mode'] or '(default)'} |"
            )
        lines.append("")
        for a in gaps:
            lines.append(f"### `{a['name']}` — {a['gap']}")
            lines.append(f"*Path:* `{a['path']}`")
            lines.append("")
            lines.append("Notes:")
            for note in a["notes"]:
                lines.append(f"- {note}")
            lines.append("")
    else:
        lines.append("## ✓ No coverage gaps detected")
        lines.append("")

    lines.append("## All subagents (coverage details)")
    lines.append("")
    lines.append("| Subagent | Tools | Disallowed | Bash | Write | Bash hook | Write hook | Gap |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for a in sorted(assessments, key=lambda a: a["name"]):
        tools = ", ".join(a["tools"]) if a["tools"] else "-"
        disallowed = ", ".join(a["disallowed"]) if a["disallowed"] else "-"
        bash = "✓" if a["has_bash"] else "-"
        write = "✓" if a["has_write"] else "-"
        bash_hook = "✓" if a["covers_bash"] or a["generic_pretooluse"] else "✗"
        write_hook = "✓" if a["covers_write"] or a["generic_pretooluse"] else "✗"
        gap = a.get("gap") or "-"
        lines.append(
            f"| `{a['name']}` | {tools} | {disallowed} | {bash} | {write} | {bash_hook} | {write_hook} | {gap} |"
        )
    lines.append("")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n")
    return {"gaps": len(gaps), "clean": len(clean), "total": len(assessments)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 3 Check 2: subagent hook coverage matrix")
    parser.add_argument(
        "--settings",
        type=Path,
        default=Path(".claude/settings.json"),
        help="Project settings.json",
    )
    parser.add_argument(
        "--agents-dir",
        type=Path,
        default=Path(".claude/agents"),
        help="Subagents directory",
    )
    parser.add_argument("--output", type=Path, required=True, help="Output markdown report path")
    args = parser.parse_args()

    if not args.settings.exists():
        console.print(f"[red]error:[/red] settings not found: {args.settings}")
        sys.exit(2)
    if not args.agents_dir.exists():
        console.print(f"[red]error:[/red] agents dir not found: {args.agents_dir}")
        sys.exit(2)

    settings = load_settings(args.settings)
    hook_matrix = build_hook_matrix(settings)
    console.print(
        f"[cyan]hook matrix:[/cyan] {sum(len(v) for v in hook_matrix.values())} "
        f"hook(s) across {len(hook_matrix)} event(s)"
    )

    agents = collect_agents(args.agents_dir)
    console.print(f"[cyan]subagents:[/cyan] {len(agents)} found in {args.agents_dir}")

    assessments = [classify_agent(a, hook_matrix) for a in agents]
    summary = render_report(agents, assessments, hook_matrix, args.output, args.settings, args.agents_dir)

    table = Table(title="Hook Coverage Summary")
    table.add_column("Metric")
    table.add_column("Count", justify="right")
    table.add_row("Subagents total", str(summary["total"]))
    table.add_row("Clean (no gap)", str(summary["clean"]))
    table.add_row("Gaps", str(summary["gaps"]), style="red" if summary["gaps"] else None)
    console.print(table)
    console.print(f"[green]✓[/green] report written: {args.output}")

    if summary["gaps"]:
        console.print(f"[red]FAIL[/red] {summary['gaps']} coverage gap(s)")
        sys.exit(1)
    console.print("[green]PASS[/green] all subagents covered")
    sys.exit(0)


if __name__ == "__main__":
    main()
