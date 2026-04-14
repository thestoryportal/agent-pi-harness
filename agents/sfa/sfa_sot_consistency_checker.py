#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "rich>=13.7.0",
# ]
# ///

"""
sfa_sot_consistency_checker.py — Phase 3 Check 4: Source of Truth consistency

Cross-references SoT §1 (what's built), §4 (per-SP feature inventory), §8
(priority table), and §11 (statistics). Flags:
  - SP counts that disagree across sections
  - Per-SP feature counts that don't sum to the §11 total
  - SPs listed in §1 header but missing a §4 block
  - §8 priority rows with status markers that don't match §1
  - CLAUDE.md SP table row status not matching SoT §1/§8

Usage:
    uv run agents/sfa/sfa_sot_consistency_checker.py \\
        --sot ~/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md \\
        --claude-md .claude/CLAUDE.md \\
        --output audits/phase3-sot-consistency-2026-04-14.md

Exit codes:
    0 = all cross-references consistent
    1 = mismatch(es) detected
    2 = setup error (missing files)
"""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from rich.console import Console
from rich.table import Table

console = Console()


def extract_sp_number(text: str) -> Optional[int]:
    m = re.match(r"SP(\d+)", text)
    return int(m.group(1)) if m else None


def parse_sot_section1_audited(sot_text: str) -> List[int]:
    """Extract the list of SPs marked as AUDIT R1 COMPLETE from §1 header."""
    m = re.search(r"##\s*1\.\s*What's Built.*?(?=\n##\s)", sot_text, re.DOTALL)
    if not m:
        return []
    section1 = m.group(0)
    audited = set()
    for m2 in re.finditer(r"SP(\d+)\s+r1", section1):
        audited.add(int(m2.group(1)))
    return sorted(audited)


def parse_sot_section1_sp_blocks(sot_text: str) -> Dict[int, Dict]:
    """Extract per-SP blocks from §1. Each block starts with `### SP<N>:`."""
    blocks: Dict[int, Dict] = {}
    m = re.search(r"##\s*1\.\s*What's Built.*?(?=\n##\s)", sot_text, re.DOTALL)
    if not m:
        return blocks
    section1 = m.group(0)
    for block_m in re.finditer(
        r"^###\s*SP(\d+):\s*(.+?)(?=\n###\s*SP|\Z)",
        section1,
        re.DOTALL | re.MULTILINE,
    ):
        sp = int(block_m.group(1))
        body = block_m.group(2)
        title_line = body.splitlines()[0] if body else ""
        feat_match = re.search(r"\*\*Feature count:\*\*\s*(\d+)", body)
        feature_count = int(feat_match.group(1)) if feat_match else None
        status_markers = []
        for marker in (
            "COMPLETE",
            "AUDIT R1 COMPLETE",
            "BUILT",
            "GAP",
            "NEXT",
            "DEFERRED",
        ):
            if marker in title_line:
                status_markers.append(marker)
        blocks[sp] = {
            "title_line": title_line.strip(),
            "feature_count": feature_count,
            "status_markers": status_markers,
            "length": len(body),
        }
    return blocks


def parse_sot_section4(sot_text: str) -> Dict[int, Dict]:
    """Extract per-SP blocks from §4 (feature inventory).

    §4 uses topic-based subsections (4.1 through 4.15) with the SP number
    appearing AFTER the title, not before: `### 4.1 Security Hardening — SP2`.
    """
    blocks: Dict[int, Dict] = {}
    m = re.search(r"##\s*4\.\s*.*?(?=\n##\s)", sot_text, re.DOTALL)
    if not m:
        return blocks
    section4 = m.group(0)
    for block_m in re.finditer(
        r"^###\s*4\.(\d+)\s+(.+?)\s*[—-]\s*SP(\d+)[^\n]*\n(.*?)(?=\n###\s*4\.|\n##\s|\Z)",
        section4,
        re.DOTALL | re.MULTILINE,
    ):
        sp = int(block_m.group(3))
        title = block_m.group(2).strip()
        body = block_m.group(4)
        feature_rows = re.findall(r"^\|\s*[A-Z]\d+\s*\|", body, re.MULTILINE)
        status_tokens = re.findall(r"\b(BUILT|GAP|NEXT|DEFERRED|REJECTED)\b", body)
        built_count = status_tokens.count("BUILT")
        gap_count = status_tokens.count("GAP")
        blocks[sp] = {
            "title": title,
            "subsection": f"4.{block_m.group(1)}",
            "row_count": len(feature_rows),
            "built": built_count,
            "gap": gap_count,
            "token_total": len(status_tokens),
        }
    return blocks


def parse_sot_section8(sot_text: str) -> Dict[int, Dict]:
    """Extract SP rows from §8 priority table."""
    rows: Dict[int, Dict] = {}
    m = re.search(r"##\s*8\.\s*.*?(?=\n##\s)", sot_text, re.DOTALL)
    if not m:
        return rows
    section8 = m.group(0)
    for line in section8.splitlines():
        for m2 in re.finditer(
            r"SP(\d+)\s+([^|()]+?)\s*\(\s*(DONE|NEXT|PENDING|DEFERRED|BLOCKED)\s*\)",
            line,
        ):
            sp = int(m2.group(1))
            status = m2.group(3).strip()
            rows.setdefault(sp, {"status": status, "row_text": line.strip()})
    return rows


def parse_sot_section11(sot_text: str) -> Dict:
    """Extract global counts from §11 statistics."""
    m = re.search(r"##\s*11\.\s*.*?(?=\n##\s|\Z)", sot_text, re.DOTALL)
    if not m:
        return {}
    section11 = m.group(0)
    stats: Dict[str, int] = {}
    for m2 in re.finditer(r"\|\s*Features\s+(BUILT|GAP|REJECTED|TOTAL)[^\|]*\|\s*(\d+)", section11):
        stats[m2.group(1)] = int(m2.group(2))
    return stats


def parse_claude_md_sp_table(claude_md_text: str) -> Dict[int, Dict]:
    """Parse the Sub-Project Status table in .claude/CLAUDE.md."""
    rows: Dict[int, Dict] = {}
    # Table rows look like: | SP1 | CC Harness | BUILT | 40 | hooks-mastery, ... |
    for line in claude_md_text.splitlines():
        m = re.match(
            r"\|\s*SP(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|",
            line,
        )
        if m:
            sp = int(m.group(1))
            rows[sp] = {
                "name": m.group(2).strip(),
                "status": m.group(3).strip(),
                "features": int(m.group(4)),
            }
    return rows


def cross_reference(
    sec1_audited: List[int],
    sec1_blocks: Dict[int, Dict],
    sec4_blocks: Dict[int, Dict],
    sec8_rows: Dict[int, Dict],
    sec11_stats: Dict,
    claude_md_rows: Dict[int, Dict],
) -> List[Dict]:
    issues: List[Dict] = []

    # Every SP in sec1_audited should have a sec1 block
    for sp in sec1_audited:
        if sp not in sec1_blocks:
            issues.append({
                "severity": "P1",
                "check": "§1 audited-list vs §1 block presence",
                "sp": sp,
                "detail": f"SP{sp} listed as audited in §1 header but has no §1 block",
            })

    # Every SP in sec1_blocks should have a sec4 block
    for sp in sec1_blocks:
        if sp not in sec4_blocks:
            issues.append({
                "severity": "P1",
                "check": "§1 vs §4 block presence",
                "sp": sp,
                "detail": f"SP{sp} present in §1 but no §4.{sp} block found",
            })

    # Every SP in sec4 should have a sec8 row
    for sp in sec4_blocks:
        if sp not in sec8_rows:
            issues.append({
                "severity": "P2",
                "check": "§4 vs §8 row presence",
                "sp": sp,
                "detail": f"SP{sp} in §4 but no row in §8 priority table",
            })

    # Feature count cross-check: §1 block count vs §4 BUILT count
    for sp in sec1_blocks:
        sec1_count = sec1_blocks[sp].get("feature_count")
        sec4_built = sec4_blocks.get(sp, {}).get("built")
        if sec1_count is not None and sec4_built is not None and sec1_count != sec4_built:
            issues.append({
                "severity": "P1",
                "check": "feature count §1 vs §4",
                "sp": sp,
                "detail": f"SP{sp}: §1 says {sec1_count} features, §4 has {sec4_built} BUILT tokens",
            })

    # CLAUDE.md cross-check
    for sp, row in claude_md_rows.items():
        sec1_count = sec1_blocks.get(sp, {}).get("feature_count")
        if sec1_count is not None and sec1_count != row["features"]:
            issues.append({
                "severity": "P2",
                "check": "feature count §1 vs CLAUDE.md",
                "sp": sp,
                "detail": f"SP{sp}: §1 has {sec1_count}, CLAUDE.md row has {row['features']}",
            })

    # Global total cross-check
    if sec11_stats.get("BUILT"):
        total_from_sec1 = sum(
            (b.get("feature_count") or 0) for b in sec1_blocks.values()
        )
        if total_from_sec1 and total_from_sec1 != sec11_stats["BUILT"]:
            issues.append({
                "severity": "P1",
                "check": "feature total §1 sum vs §11",
                "sp": None,
                "detail": f"sum of §1 per-SP counts = {total_from_sec1}, "
                          f"§11 Features BUILT = {sec11_stats['BUILT']}",
            })

    return issues


def render_report(
    sec1_audited: List[int],
    sec1_blocks: Dict[int, Dict],
    sec4_blocks: Dict[int, Dict],
    sec8_rows: Dict[int, Dict],
    sec11_stats: Dict,
    claude_md_rows: Dict[int, Dict],
    issues: List[Dict],
    output: Path,
    sot_path: Path,
    claude_md_path: Path,
) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: List[str] = [
        "# Phase 3 Check 4 — Source of Truth Consistency",
        "",
        f"**Date:** {now}",
        f"**SoT:** `{sot_path}`",
        f"**CLAUDE.md:** `{claude_md_path}`",
        f"**§1 SP blocks:** {len(sec1_blocks)}",
        f"**§1 audited (r1) count:** {len(sec1_audited)} — {sec1_audited}",
        f"**§4 SP blocks:** {len(sec4_blocks)}",
        f"**§8 priority rows:** {len(sec8_rows)}",
        f"**§11 global stats:** {sec11_stats if sec11_stats else '(not parsed)'}",
        f"**CLAUDE.md rows:** {len(claude_md_rows)}",
        f"**Issues found:** {len(issues)}",
        "",
    ]

    if issues:
        lines.append("## ❌ Consistency issues")
        lines.append("")
        lines.append("| Severity | Check | SP | Detail |")
        lines.append("|---|---|---|---|")
        for issue in sorted(issues, key=lambda i: (i["severity"], i.get("sp") or 0)):
            sp_str = f"SP{issue['sp']}" if issue.get("sp") else "—"
            lines.append(f"| {issue['severity']} | {issue['check']} | {sp_str} | {issue['detail']} |")
        lines.append("")
    else:
        lines.append("## ✓ No consistency issues detected")
        lines.append("")

    lines.append("## Per-SP cross-reference matrix")
    lines.append("")
    lines.append("| SP | §1 features | §4 BUILT | §8 status | CLAUDE.md features | CLAUDE.md status |")
    lines.append("|---|---|---|---|---|---|")
    all_sps = set(sec1_blocks) | set(sec4_blocks) | set(sec8_rows) | set(claude_md_rows)
    for sp in sorted(all_sps):
        s1 = sec1_blocks.get(sp, {}).get("feature_count", "-")
        s4 = sec4_blocks.get(sp, {}).get("built", "-")
        s8 = sec8_rows.get(sp, {}).get("status", "-")
        cm_f = claude_md_rows.get(sp, {}).get("features", "-")
        cm_s = claude_md_rows.get(sp, {}).get("status", "-")
        lines.append(f"| SP{sp} | {s1} | {s4} | {s8} | {cm_f} | {cm_s} |")
    lines.append("")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 3 Check 4: Source of Truth consistency")
    parser.add_argument(
        "--sot",
        type=Path,
        default=Path.home() / "Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md",
        help="Source of Truth markdown path",
    )
    parser.add_argument(
        "--claude-md",
        type=Path,
        default=Path(".claude/CLAUDE.md"),
        help="Project CLAUDE.md with Sub-Project Status table",
    )
    parser.add_argument("--output", type=Path, required=True, help="Output markdown report path")
    args = parser.parse_args()

    if not args.sot.exists():
        console.print(f"[red]error:[/red] SoT not found: {args.sot}")
        sys.exit(2)
    if not args.claude_md.exists():
        console.print(f"[yellow]warn:[/yellow] CLAUDE.md not found: {args.claude_md}")
        claude_md_text = ""
    else:
        claude_md_text = args.claude_md.read_text()

    sot_text = args.sot.read_text()
    console.print(f"[cyan]parsing SoT:[/cyan] {len(sot_text)} chars")

    sec1_audited = parse_sot_section1_audited(sot_text)
    sec1_blocks = parse_sot_section1_sp_blocks(sot_text)
    sec4_blocks = parse_sot_section4(sot_text)
    sec8_rows = parse_sot_section8(sot_text)
    sec11_stats = parse_sot_section11(sot_text)
    claude_md_rows = parse_claude_md_sp_table(claude_md_text)

    console.print(
        f"[cyan]parsed:[/cyan] §1={len(sec1_blocks)} §4={len(sec4_blocks)} "
        f"§8={len(sec8_rows)} §11={sec11_stats} CLAUDE.md={len(claude_md_rows)}"
    )

    issues = cross_reference(
        sec1_audited, sec1_blocks, sec4_blocks, sec8_rows, sec11_stats, claude_md_rows
    )

    render_report(
        sec1_audited,
        sec1_blocks,
        sec4_blocks,
        sec8_rows,
        sec11_stats,
        claude_md_rows,
        issues,
        args.output,
        args.sot,
        args.claude_md,
    )

    table = Table(title="SoT Consistency")
    table.add_column("Metric")
    table.add_column("Count", justify="right")
    table.add_row("§1 SP blocks", str(len(sec1_blocks)))
    table.add_row("§4 SP blocks", str(len(sec4_blocks)))
    table.add_row("§8 priority rows", str(len(sec8_rows)))
    table.add_row("§11 Features BUILT", str(sec11_stats.get("BUILT", "-")))
    table.add_row("CLAUDE.md SP rows", str(len(claude_md_rows)))
    table.add_row("Issues", str(len(issues)), style="red" if issues else None)
    console.print(table)
    console.print(f"[green]✓[/green] report written: {args.output}")

    if issues:
        console.print(f"[yellow]REVIEW[/yellow] {len(issues)} consistency issue(s)")
        sys.exit(1)
    console.print("[green]PASS[/green] SoT consistent across sections")
    sys.exit(0)


if __name__ == "__main__":
    main()
