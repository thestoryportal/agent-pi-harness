#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "rich>=13.7.0",
# ]
# ///

"""
sfa_exception_ledger_auditor.py — Phase 3 Check 1: exception ledger drift

Parses audits/exceptions.md and verifies that every path referenced in each
exception's `Path(s)` block still exists in the git-tracked working tree.
Flags stale exceptions (path absent), upstream-only paths (intentionally
skipped), and ambiguous entries.

This is a mechanical tool — no LLM calls.

Usage:
    uv run agents/sfa/sfa_exception_ledger_auditor.py \\
        --exceptions audits/exceptions.md \\
        --repo /Users/robertrhu/Projects/arhugula \\
        --output audits/phase3-exception-ledger-2026-04-14.md

Exit codes:
    0 = all active exception paths exist in git
    1 = one or more stale paths present
    2 = setup error (missing files, git not a repo)
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set

from rich.console import Console
from rich.table import Table

console = Console()

UPSTREAM_PREFIXES = ("~/", "upstream/", "disler/", "http://", "https://")
UPSTREAM_MARKERS = (
    "full-clone",
    "full clone",
    "upstream ",
    "not ArhuGula",
    "repo root",
    "repo-root",
)
# Phrases that mark an exception path as documenting an intentional absence
# (deletions, preserved non-imports, security regressions). Paths under these
# markers should not be flagged as stale.
ABSENCE_MARKERS = (
    "invention, classify DELETE",
    "intentionally absent",
    "will remain absent",
    "permanent — `",
    "security regression flag",
    "documented loss",
    "deliberate non-import",
    "deliberately non-imported",
)


def git_ls_files(repo: Path) -> Set[str]:
    """Return the set of all git-tracked paths in the repo."""
    result = subprocess.run(
        ["git", "-C", str(repo), "ls-files"],
        capture_output=True,
        text=True,
        check=True,
    )
    return set(result.stdout.splitlines())


def parse_exceptions(exceptions_md: Path) -> List[Dict]:
    """Parse each exception entry into {id, title, status, paths: [...], line_refs}."""
    text = exceptions_md.read_text()
    lines = text.splitlines()
    entries: List[Dict] = []
    current: Dict | None = None
    in_paths_block = False

    def finalize(entry: Dict | None) -> None:
        if entry is not None:
            entries.append(entry)

    for idx, raw in enumerate(lines):
        line = raw.rstrip()

        m = re.match(r"^## Exception (\d+)\s*[—-]\s*(.+)$", line)
        if m:
            finalize(current)
            current = {
                "id": int(m.group(1)),
                "title": m.group(2).strip(),
                "status": "unknown",
                "paths": [],
                "path_lines": [],
                "line_start": idx + 1,
            }
            in_paths_block = False
            continue

        if current is None:
            continue

        stripped = line.strip()

        if stripped == "**Path(s):**":
            in_paths_block = True
            continue

        status_match = re.match(r"^\*\*Status:\*\*\s*(.+)$", stripped)
        if status_match:
            current["status"] = status_match.group(1).strip()
            continue

        if in_paths_block and re.match(r"^\*\*[A-Za-z]", stripped):
            in_paths_block = False
            continue

        if in_paths_block and stripped.startswith("- "):
            # Extract the first backtick-wrapped token on the line
            path_m = re.search(r"`([^`]+)`", line)
            if path_m:
                path_val = path_m.group(1)
                low_line = line.lower()
                low_path = path_val.lower()
                # Context classification (case-insensitive)
                is_upstream = (
                    path_val.startswith(UPSTREAM_PREFIXES)
                    or any(marker in low_line for marker in UPSTREAM_MARKERS)
                    or any(marker in low_path for marker in UPSTREAM_MARKERS)
                    or "upstream candidate" in low_line
                )
                is_absence = any(marker.lower() in low_line for marker in ABSENCE_MARKERS)
                # Brace-expansion pattern `dir/{a, b, c}` — documented bundles
                # that we should not try to resolve as a single path
                is_brace = "{" in path_val and "}" in path_val

                if is_upstream:
                    classification = "upstream"
                elif is_absence:
                    classification = "intentional_absence"
                elif is_brace:
                    classification = "brace_bundle"
                else:
                    classification = "local"

                current["paths"].append(
                    {
                        "path": path_val,
                        "raw_line": line.strip(),
                        "line_no": idx + 1,
                        "classification": classification,
                    }
                )
                current["path_lines"].append(idx + 1)

    finalize(current)
    return entries


def audit(entries: List[Dict], tracked: Set[str], repo: Path) -> Dict:
    """Check every local path against the git manifest. Return summary dict."""
    stale: List[Dict] = []
    active: List[Dict] = []
    upstream: List[Dict] = []
    absences: List[Dict] = []
    brace_bundles: List[Dict] = []
    resolved_status = {"active": 0, "resolved": 0, "unknown": 0}

    for entry in entries:
        status = entry["status"].lower()
        if "resolved" in status:
            resolved_status["resolved"] += 1
        elif "active" in status:
            resolved_status["active"] += 1
        else:
            resolved_status["unknown"] += 1

        for path_entry in entry["paths"]:
            path_val = path_entry["path"]
            record = {
                "exception_id": entry["id"],
                "exception_title": entry["title"],
                "exception_status": entry["status"],
                "path": path_val,
                "raw_line": path_entry["raw_line"],
                "line_no": path_entry["line_no"],
                "classification": path_entry["classification"],
            }
            cls = path_entry["classification"]
            if cls == "upstream":
                upstream.append(record)
                continue
            if cls == "intentional_absence":
                absences.append(record)
                continue
            if cls == "brace_bundle":
                brace_bundles.append(record)
                continue

            # Local path — check git tracking
            # IMPORTANT: use removeprefix, not lstrip — lstrip("./") would
            # also strip the leading "." from dotfile paths like .claude/...
            normalized = path_val.removeprefix("./")
            check_path = normalized.split("*")[0].rstrip("/")
            if check_path in tracked:
                record["verdict"] = "tracked"
                active.append(record)
            elif (repo / check_path).exists():
                record["verdict"] = "present_untracked"
                active.append(record)
            else:
                # Try prefix match (directories listed without trailing /)
                prefix_hit = any(t.startswith(check_path + "/") for t in tracked)
                if prefix_hit:
                    record["verdict"] = "tracked_prefix"
                    active.append(record)
                else:
                    record["verdict"] = "STALE"
                    stale.append(record)

    return {
        "resolved_status": resolved_status,
        "total_exceptions": len(entries),
        "total_local_paths": len(active) + len(stale),
        "total_upstream_paths": len(upstream),
        "total_absences": len(absences),
        "total_brace_bundles": len(brace_bundles),
        "active_paths": active,
        "upstream_paths": upstream,
        "absence_paths": absences,
        "brace_bundle_paths": brace_bundles,
        "stale_paths": stale,
    }


def render_report(summary: Dict, output: Path, exceptions_md: Path) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: List[str] = [
        "# Phase 3 Check 1 — Exception Ledger Drift",
        "",
        f"**Date:** {now}",
        f"**Source:** `{exceptions_md}`",
        f"**Total exceptions parsed:** {summary['total_exceptions']}",
        f"**Status breakdown:** "
        f"active={summary['resolved_status']['active']} "
        f"resolved={summary['resolved_status']['resolved']} "
        f"unknown={summary['resolved_status']['unknown']}",
        f"**Local paths checked:** {summary['total_local_paths']}",
        f"**Upstream paths skipped:** {summary['total_upstream_paths']}",
        f"**Intentional absences skipped:** {summary['total_absences']}",
        f"**Brace-bundle paths skipped:** {summary['total_brace_bundles']}",
        "",
    ]

    if summary["stale_paths"]:
        lines.append("## ❌ STALE paths (no longer present in git)")
        lines.append("")
        lines.append("| Exception | Path | Exception Status | Raw line |")
        lines.append("|---|---|---|---|")
        for r in sorted(summary["stale_paths"], key=lambda r: (r["exception_id"], r["path"])):
            lines.append(
                f"| Exception {r['exception_id']} | `{r['path']}` | "
                f"{r['exception_status']} | {r['raw_line']} |"
            )
        lines.append("")
    else:
        lines.append("## ✓ No stale local paths detected")
        lines.append("")

    lines.append("## Active local paths (resolved to tracked files)")
    lines.append("")
    by_ex: Dict[int, List[Dict]] = {}
    for r in summary["active_paths"]:
        by_ex.setdefault(r["exception_id"], []).append(r)
    for ex_id in sorted(by_ex.keys()):
        rows = by_ex[ex_id]
        title = rows[0]["exception_title"]
        status = rows[0]["exception_status"]
        lines.append(f"### Exception {ex_id} — {title}")
        lines.append(f"*Status:* {status}")
        lines.append("")
        lines.append("| Path | Verdict |")
        lines.append("|---|---|")
        for r in rows:
            lines.append(f"| `{r['path']}` | {r['verdict']} |")
        lines.append("")

    if summary["upstream_paths"]:
        lines.append("## Skipped: upstream-only references")
        lines.append("")
        lines.append(f"_{len(summary['upstream_paths'])} path(s) reference upstream clones "
                     f"or are annotated as not ArhuGula artifacts — not audited by this check._")
        lines.append("")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 3 Check 1: exception ledger drift")
    parser.add_argument(
        "--exceptions",
        type=Path,
        default=Path("audits/exceptions.md"),
        help="Exceptions ledger to audit",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="ArhuGula repo root",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output markdown report path",
    )
    args = parser.parse_args()

    if not args.exceptions.exists():
        console.print(f"[red]error:[/red] exceptions file not found: {args.exceptions}")
        sys.exit(2)
    if not (args.repo / ".git").exists():
        console.print(f"[red]error:[/red] not a git repo: {args.repo}")
        sys.exit(2)

    console.print(f"[cyan]parsing exceptions:[/cyan] {args.exceptions}")
    entries = parse_exceptions(args.exceptions)
    console.print(f"  loaded [bold]{len(entries)}[/bold] exception entries")

    console.print(f"[cyan]loading git manifest:[/cyan] {args.repo}")
    try:
        tracked = git_ls_files(args.repo)
    except subprocess.CalledProcessError as exc:
        console.print(f"[red]error:[/red] git ls-files failed: {exc}")
        sys.exit(2)
    console.print(f"  [bold]{len(tracked)}[/bold] tracked files")

    summary = audit(entries, tracked, args.repo)
    render_report(summary, args.output, args.exceptions)

    table = Table(title="Exception Ledger Audit")
    table.add_column("Metric")
    table.add_column("Count", justify="right")
    table.add_row("Exceptions total", str(summary["total_exceptions"]))
    table.add_row("  active", str(summary["resolved_status"]["active"]))
    table.add_row("  resolved", str(summary["resolved_status"]["resolved"]))
    table.add_row("  unknown", str(summary["resolved_status"]["unknown"]))
    table.add_row("Local paths checked", str(summary["total_local_paths"]))
    table.add_row(
        "  STALE",
        str(len(summary["stale_paths"])),
        style="red" if summary["stale_paths"] else None,
    )
    table.add_row("Upstream paths skipped", str(summary["total_upstream_paths"]))
    console.print(table)
    console.print(f"[green]✓[/green] report written: {args.output}")

    if summary["stale_paths"]:
        console.print(f"[red]FAIL[/red] {len(summary['stale_paths'])} stale path(s)")
        sys.exit(1)
    console.print("[green]PASS[/green] zero stale paths")
    sys.exit(0)


if __name__ == "__main__":
    main()
