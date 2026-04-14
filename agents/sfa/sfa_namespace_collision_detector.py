#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "rich>=13.7.0",
# ]
# ///

"""
sfa_namespace_collision_detector.py — Phase 3 Check 3: cross-SP namespace collisions

Scans `.claude/commands/`, `.claude/skills/`, and `.claude/agents/` for name
collisions — cases where the same slash command / skill name / agent name
exists at multiple paths (e.g., the Exception 23 4-way `prime.md` collision
across SP1/SP8/SP12/SP15).

This is a mechanical tool — no LLM calls.

Usage:
    uv run agents/sfa/sfa_namespace_collision_detector.py \\
        --claude-dir .claude \\
        --output audits/phase3-namespace-collisions-2026-04-14.md

Exit codes:
    0 = no namespace collisions
    1 = collision(s) detected (review against exceptions ledger)
    2 = setup error
"""

import argparse
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.table import Table

console = Console()


def collect_commands(claude_dir: Path) -> Dict[str, List[Path]]:
    """Enumerate every .md command file under .claude/commands/, keyed by base name."""
    commands_dir = claude_dir / "commands"
    if not commands_dir.exists():
        return {}
    by_name: Dict[str, List[Path]] = defaultdict(list)
    for md in commands_dir.rglob("*.md"):
        if md.name.upper() == "CLAUDE.MD":
            continue
        name = md.stem
        by_name[name].append(md.relative_to(claude_dir.parent) if claude_dir.parent else md)
    return by_name


def collect_skills(claude_dir: Path) -> Dict[str, List[Path]]:
    """Enumerate every SKILL.md under .claude/skills/, keyed by parent dir name."""
    skills_dir = claude_dir / "skills"
    if not skills_dir.exists():
        return {}
    by_name: Dict[str, List[Path]] = defaultdict(list)
    for skill_md in skills_dir.rglob("SKILL.md"):
        name = skill_md.parent.name
        by_name[name].append(skill_md.relative_to(claude_dir.parent) if claude_dir.parent else skill_md)
    return by_name


def collect_agents(claude_dir: Path) -> Dict[str, List[Path]]:
    """Enumerate every .md agent file under .claude/agents/, keyed by stem."""
    agents_dir = claude_dir / "agents"
    if not agents_dir.exists():
        return {}
    by_name: Dict[str, List[Path]] = defaultdict(list)
    for md in agents_dir.rglob("*.md"):
        if md.name.upper() == "CLAUDE.MD":
            continue
        name = md.stem
        by_name[name].append(md.relative_to(claude_dir.parent) if claude_dir.parent else md)
    return by_name


def collect_cross_namespace(
    commands: Dict[str, List[Path]],
    skills: Dict[str, List[Path]],
    agents: Dict[str, List[Path]],
) -> Dict[str, Dict[str, List[Path]]]:
    """Detect names that exist in more than one of (commands, skills, agents)."""
    all_names = set(commands) | set(skills) | set(agents)
    cross: Dict[str, Dict[str, List[Path]]] = {}
    for name in all_names:
        registries = {}
        if name in commands:
            registries["commands"] = commands[name]
        if name in skills:
            registries["skills"] = skills[name]
        if name in agents:
            registries["agents"] = agents[name]
        if len(registries) > 1:
            cross[name] = registries
    return cross


def render_report(
    commands: Dict[str, List[Path]],
    skills: Dict[str, List[Path]],
    agents: Dict[str, List[Path]],
    cross_collisions: Dict[str, Dict[str, List[Path]]],
    output: Path,
    claude_dir: Path,
) -> Dict[str, int]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    intra_commands = {name: paths for name, paths in commands.items() if len(paths) > 1}
    intra_skills = {name: paths for name, paths in skills.items() if len(paths) > 1}
    intra_agents = {name: paths for name, paths in agents.items() if len(paths) > 1}

    total_collisions = len(intra_commands) + len(intra_skills) + len(intra_agents) + len(cross_collisions)

    lines: List[str] = [
        "# Phase 3 Check 3 — Cross-SP Namespace Collisions",
        "",
        f"**Date:** {now}",
        f"**Root:** `{claude_dir}`",
        f"**Commands:** {sum(len(p) for p in commands.values())} file(s) across {len(commands)} names",
        f"**Skills:** {sum(len(p) for p in skills.values())} file(s) across {len(skills)} names",
        f"**Agents:** {sum(len(p) for p in agents.values())} file(s) across {len(agents)} names",
        f"**Total collisions:** {total_collisions}",
        "",
    ]

    def emit_intra(title: str, registry: Dict[str, List[Path]]) -> None:
        if not registry:
            lines.append(f"## ✓ No intra-{title} collisions")
            lines.append("")
            return
        lines.append(f"## ❌ Intra-{title} collisions")
        lines.append("")
        lines.append(f"| Name | Count | Paths |")
        lines.append(f"|---|---|---|")
        for name in sorted(registry.keys()):
            paths = registry[name]
            paths_str = " <br> ".join(f"`{p}`" for p in paths)
            lines.append(f"| `{name}` | {len(paths)} | {paths_str} |")
        lines.append("")

    emit_intra("commands", intra_commands)
    emit_intra("skills", intra_skills)
    emit_intra("agents", intra_agents)

    if cross_collisions:
        lines.append("## ❌ Cross-registry collisions (same name in multiple registries)")
        lines.append("")
        lines.append("These are names that exist in more than one of `.claude/commands/`, "
                     "`.claude/skills/`, `.claude/agents/`. The slash-command router's resolution "
                     "order is undefined; cross-collisions must either be renamed or documented "
                     "in `audits/exceptions.md` (see Exception 23 for the `prime.md` precedent).")
        lines.append("")
        lines.append("| Name | Registries | Paths |")
        lines.append("|---|---|---|")
        for name in sorted(cross_collisions.keys()):
            registries = cross_collisions[name]
            regs_str = " + ".join(sorted(registries.keys()))
            all_paths = []
            for reg_paths in registries.values():
                all_paths.extend(reg_paths)
            paths_str = " <br> ".join(f"`{p}`" for p in all_paths)
            lines.append(f"| `{name}` | {regs_str} | {paths_str} |")
        lines.append("")
    else:
        lines.append("## ✓ No cross-registry collisions")
        lines.append("")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n")

    return {
        "intra_commands": len(intra_commands),
        "intra_skills": len(intra_skills),
        "intra_agents": len(intra_agents),
        "cross": len(cross_collisions),
        "total": total_collisions,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 3 Check 3: cross-SP namespace collisions")
    parser.add_argument(
        "--claude-dir",
        type=Path,
        default=Path(".claude"),
        help=".claude root directory (contains commands/, skills/, agents/)",
    )
    parser.add_argument("--output", type=Path, required=True, help="Output markdown report path")
    args = parser.parse_args()

    if not args.claude_dir.exists():
        console.print(f"[red]error:[/red] claude dir not found: {args.claude_dir}")
        sys.exit(2)

    commands = collect_commands(args.claude_dir)
    skills = collect_skills(args.claude_dir)
    agents = collect_agents(args.claude_dir)
    cross = collect_cross_namespace(commands, skills, agents)

    console.print(
        f"[cyan]inventory:[/cyan] "
        f"commands={sum(len(p) for p in commands.values())} "
        f"skills={sum(len(p) for p in skills.values())} "
        f"agents={sum(len(p) for p in agents.values())}"
    )

    summary = render_report(commands, skills, agents, cross, args.output, args.claude_dir)

    table = Table(title="Namespace Collisions")
    table.add_column("Type")
    table.add_column("Count", justify="right")
    table.add_row("Intra-commands", str(summary["intra_commands"]))
    table.add_row("Intra-skills", str(summary["intra_skills"]))
    table.add_row("Intra-agents", str(summary["intra_agents"]))
    table.add_row("Cross-registry", str(summary["cross"]))
    table.add_row("Total", str(summary["total"]), style="red" if summary["total"] else None)
    console.print(table)
    console.print(f"[green]✓[/green] report written: {args.output}")

    if summary["total"] > 0:
        console.print(f"[yellow]REVIEW[/yellow] {summary['total']} collision(s) — cross-check against exceptions.md Exception 23 pattern")
        sys.exit(1)
    console.print("[green]PASS[/green] no namespace collisions")
    sys.exit(0)


if __name__ == "__main__":
    main()
