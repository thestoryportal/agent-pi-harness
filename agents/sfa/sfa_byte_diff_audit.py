#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "rich>=13.7.0",
# ]
# ///

"""
sfa_byte_diff_audit.py — Phase 1 byte-parity sweep (Comprehensive Audit)

Walks the upstream full-clone tree, diffs every file against its ArhuGula
counterpart, cross-references drift against audits/exceptions.md, and emits a
structured Markdown report. Exit 0 on clean parity, exit 1 on unexplained drift.

This is a mechanical tool — no LLM calls. The /// script block keeps the
dependency surface minimal (rich only, for console output).

Usage:
    # Full sweep over every clone in the full-clones directory
    uv run agents/sfa/sfa_byte_diff_audit.py \\
        --clones ~/Projects/indydevdan-harness-research/research/full-clones \\
        --repo /Users/robertrhu/Projects/arhugula \\
        --exceptions audits/exceptions.md \\
        --output audits/phase1-byte-parity-2026-04-14.md

    # Filter to a single upstream clone
    uv run agents/sfa/sfa_byte_diff_audit.py \\
        --clone agent-sandboxes \\
        --clones ~/Projects/indydevdan-harness-research/research/full-clones \\
        --output /tmp/sp15-parity.md

    # Strict mode: treat MISSING upstream files as failure too
    uv run agents/sfa/sfa_byte_diff_audit.py \\
        --clones ~/Projects/indydevdan-harness-research/research/full-clones \\
        --output /tmp/strict.md \\
        --strict

Exit codes:
    0 = clean (all drift exception-covered; MISSING tolerated unless --strict)
    1 = unexplained drift present (or MISSING present in --strict mode)
    2 = setup error (missing clones dir, missing repo, etc.)
"""

import argparse
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.table import Table

console = Console()

SKIP_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    "venv",
    ".venv",
    "target",
    "dist",
    "build",
    ".next",
    ".swc",
    ".cache",
}
SKIP_EXTS = {".pyc", ".pyo", ".swp", ".swo", ".DS_Store"}
ALWAYS_CONSIDER_DOTFILES = {
    ".gitignore",
    ".env.example",
    ".env.sample",
    ".tool-versions",
    ".mcp.json",
    ".mcp.json.sandbox",
    ".mcp.json.sandbox.firecrawl",
}


def parse_exceptions(exceptions_md: Path) -> Dict[str, str]:
    """Parse audits/exceptions.md and return {path: exception_label}.

    The parser is line-oriented:
      - Enters "paths block" state when it sees `**Path(s):**`
      - Exits when it hits another `**Field:**` marker
      - Extracts each backtick-wrapped path token inside the block

    Annotations like `(Tier 1 byte-identical — upstream ...)` are ignored; only
    the first backtick token per line becomes a key.
    """
    text = exceptions_md.read_text()
    mapping: Dict[str, str] = {}
    current_ex: str | None = None
    in_paths_block = False

    for raw in text.splitlines():
        line = raw.rstrip()

        m = re.match(r"^## Exception (\d+)", line)
        if m:
            current_ex = m.group(1)
            in_paths_block = False
            continue

        if line.strip() == "**Path(s):**":
            in_paths_block = True
            continue

        if in_paths_block and re.match(r"^\*\*[A-Za-z]", line.strip()):
            in_paths_block = False
            continue

        if in_paths_block and current_ex and line.strip().startswith("- "):
            path_match = re.search(r"`([^`]+)`", line)
            if path_match:
                path = path_match.group(1)
                mapping[path] = f"Exception {current_ex}"

    return mapping


def should_skip(path: Path) -> bool:
    """Skip non-source files (caches, build artifacts, IDE cruft)."""
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    if path.suffix in SKIP_EXTS:
        return True
    name = path.name
    if name.startswith(".") and name not in ALWAYS_CONSIDER_DOTFILES:
        return True
    return False


def compare_bytes(local: Path, upstream: Path) -> str:
    """Return MATCH | DRIFT | MISSING. Reads both files in full."""
    if not local.exists():
        return "MISSING"
    if not upstream.exists():
        return "UPSTREAM_ABSENT"
    try:
        return "MATCH" if local.read_bytes() == upstream.read_bytes() else "DRIFT"
    except OSError as exc:
        console.print(f"[yellow]warn[/yellow] io error on {local}: {exc}")
        return "DRIFT"


def walk_clone(clone_root: Path, repo_root: Path) -> List[Dict[str, str]]:
    """Walk one full-clone tree and diff every file against the ArhuGula repo."""
    rows: List[Dict[str, str]] = []
    for file in clone_root.rglob("*"):
        if not file.is_file():
            continue
        if should_skip(file):
            continue
        rel = file.relative_to(clone_root)
        local_path = repo_root / rel
        status = compare_bytes(local_path, file)
        rows.append(
            {
                "clone": clone_root.name,
                "rel_path": str(rel),
                "local_path": str(local_path),
                "status": status,
            }
        )
    return rows


def classify(rows: List[Dict[str, str]], exception_map: Dict[str, str], repo_root: Path) -> List[Dict[str, str]]:
    """Annotate each row with final_status + exception_id lookup."""
    for row in rows:
        status = row["status"]
        exception_id = None
        if status == "DRIFT":
            rel = row["rel_path"]
            local_abs = row["local_path"]
            local_rel_to_repo = local_abs.replace(str(repo_root).rstrip("/") + "/", "")
            if rel in exception_map:
                exception_id = exception_map[rel]
                status = "DRIFT_EXPLAINED"
            elif local_rel_to_repo in exception_map:
                exception_id = exception_map[local_rel_to_repo]
                status = "DRIFT_EXPLAINED"
            else:
                status = "DRIFT_UNEXPLAINED"
        row["final_status"] = status
        row["exception_id"] = exception_id or ""
    return rows


def render_report(
    rows: List[Dict[str, str]],
    clone_roots: List[Path],
    exception_map_size: int,
    output: Path,
    strict: bool,
) -> Dict[str, int]:
    """Write the markdown report and return the status-count dict."""
    stats = {
        "MATCH": 0,
        "DRIFT_EXPLAINED": 0,
        "DRIFT_UNEXPLAINED": 0,
        "MISSING": 0,
        "UPSTREAM_ABSENT": 0,
    }
    for row in rows:
        stats[row["final_status"]] += 1

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: List[str] = [
        "# Phase 1 — Byte-Parity Sweep Report",
        "",
        f"**Date:** {now}",
        f"**Strict mode:** {'yes' if strict else 'no'}",
        f"**Clones scanned:** {len(clone_roots)}",
        f"**Total files examined:** {len(rows)}",
        f"**Exception paths loaded:** {exception_map_size}",
        "",
        "## Summary",
        "",
        "| Status | Count |",
        "|---|---|",
        f"| MATCH | {stats['MATCH']} |",
        f"| DRIFT (explained) | {stats['DRIFT_EXPLAINED']} |",
        f"| DRIFT (UNEXPLAINED) | {stats['DRIFT_UNEXPLAINED']} |",
        f"| MISSING in ArhuGula | {stats['MISSING']} |",
        f"| Upstream absent | {stats['UPSTREAM_ABSENT']} |",
        "",
    ]

    unexplained = sorted(
        [r for r in rows if r["final_status"] == "DRIFT_UNEXPLAINED"],
        key=lambda r: (r["clone"], r["rel_path"]),
    )
    if unexplained:
        lines.append("## Unexplained drift (Phase 2 priority targets)")
        lines.append("")
        lines.append("| Clone | Rel Path | Local Path |")
        lines.append("|---|---|---|")
        for row in unexplained:
            lines.append(f"| {row['clone']} | `{row['rel_path']}` | `{row['local_path']}` |")
        lines.append("")

    explained = sorted(
        [r for r in rows if r["final_status"] == "DRIFT_EXPLAINED"],
        key=lambda r: (r["clone"], r["rel_path"]),
    )
    if explained:
        lines.append("## Explained drift (exception-covered)")
        lines.append("")
        lines.append("| Clone | Rel Path | Exception |")
        lines.append("|---|---|---|")
        for row in explained:
            lines.append(f"| {row['clone']} | `{row['rel_path']}` | {row['exception_id']} |")
        lines.append("")

    missing = sorted(
        [r for r in rows if r["final_status"] == "MISSING"],
        key=lambda r: (r["clone"], r["rel_path"]),
    )
    if missing:
        lines.append("## Missing in ArhuGula (upstream files not imported)")
        lines.append("")
        lines.append("| Clone | Rel Path |")
        lines.append("|---|---|")
        for row in missing:
            lines.append(f"| {row['clone']} | `{row['rel_path']}` |")
        lines.append("")

    lines.append("## Per-clone breakdown")
    lines.append("")
    lines.append("| Clone | MATCH | DRIFT-E | DRIFT-U | MISSING |")
    lines.append("|---|---|---|---|---|")
    by_clone: Dict[str, Dict[str, int]] = {}
    for row in rows:
        bucket = by_clone.setdefault(
            row["clone"],
            {"MATCH": 0, "DRIFT_EXPLAINED": 0, "DRIFT_UNEXPLAINED": 0, "MISSING": 0, "UPSTREAM_ABSENT": 0},
        )
        bucket[row["final_status"]] += 1
    for clone in sorted(by_clone.keys()):
        s = by_clone[clone]
        lines.append(
            f"| {clone} | {s['MATCH']} | {s['DRIFT_EXPLAINED']} | {s['DRIFT_UNEXPLAINED']} | {s['MISSING']} |"
        )
    lines.append("")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n")
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 1 byte-parity sweep for Comprehensive Audit")
    parser.add_argument("--clones", type=Path, required=True, help="Full-clone root directory")
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="ArhuGula repo root (default: cwd)")
    parser.add_argument(
        "--exceptions",
        type=Path,
        default=Path("audits/exceptions.md"),
        help="Exceptions ledger for drift lookup",
    )
    parser.add_argument("--output", type=Path, required=True, help="Output markdown report path")
    parser.add_argument("--clone", type=str, default=None, help="Filter to a single clone name")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat MISSING upstream files as failure (default: tolerate MISSING)",
    )
    args = parser.parse_args()

    if not args.clones.exists():
        console.print(f"[red]error:[/red] clones dir not found: {args.clones}")
        sys.exit(2)
    if not args.repo.exists():
        console.print(f"[red]error:[/red] repo dir not found: {args.repo}")
        sys.exit(2)

    if args.exceptions.exists():
        exception_map = parse_exceptions(args.exceptions)
    else:
        console.print(f"[yellow]warn[/yellow] exceptions file not found: {args.exceptions}")
        exception_map = {}

    if args.clone:
        candidate = args.clones / args.clone
        if not candidate.exists():
            console.print(f"[red]error:[/red] clone not found: {candidate}")
            sys.exit(2)
        clone_roots = [candidate]
    else:
        clone_roots = sorted(
            c for c in args.clones.iterdir() if c.is_dir() and not c.name.startswith(".")
        )

    console.print(f"[cyan]Phase 1:[/cyan] walking {len(clone_roots)} clone(s)")
    console.print(f"[cyan]Exceptions:[/cyan] loaded {len(exception_map)} path(s)")

    all_rows: List[Dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(walk_clone, clone, args.repo): clone for clone in clone_roots}
        for future in as_completed(futures):
            clone = futures[future]
            try:
                rows = future.result()
                all_rows.extend(rows)
                console.print(f"  [green]✓[/green] {clone.name}: {len(rows)} files")
            except Exception as exc:
                console.print(f"  [red]✗[/red] {clone.name}: {exc}")

    all_rows = classify(all_rows, exception_map, args.repo)
    stats = render_report(all_rows, clone_roots, len(exception_map), args.output, args.strict)

    table = Table(title="Phase 1 summary")
    table.add_column("Status")
    table.add_column("Count", justify="right")
    table.add_row("MATCH", str(stats["MATCH"]))
    table.add_row("DRIFT (explained)", str(stats["DRIFT_EXPLAINED"]))
    table.add_row(
        "DRIFT (UNEXPLAINED)",
        str(stats["DRIFT_UNEXPLAINED"]),
        style="red" if stats["DRIFT_UNEXPLAINED"] else None,
    )
    table.add_row("MISSING", str(stats["MISSING"]))
    console.print(table)
    console.print(f"[green]✓[/green] report written: {args.output}")

    fail = stats["DRIFT_UNEXPLAINED"] > 0 or (args.strict and stats["MISSING"] > 0)
    if fail:
        console.print(
            f"[red]FAIL[/red] unexplained={stats['DRIFT_UNEXPLAINED']} missing={stats['MISSING']}"
        )
        sys.exit(1)
    console.print(f"[green]PASS[/green] zero unexplained drift")
    sys.exit(0)


if __name__ == "__main__":
    main()
