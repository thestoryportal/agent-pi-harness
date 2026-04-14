#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "rich>=13.7.0",
#   "pyyaml>=6.0",
# ]
# ///

"""
sfa_coder_validator_loop.py — Phase 2 coder↔validator loop driver

Runs inside an E2B sandbox as part of the ArhuGula Comprehensive Audit
(see audits/comprehensive-audit-spec.md §5). Drives an Anthropic coder
agent through a tool-use loop that reviews one sub-project's scope and
proposes diffs, then submits the review to an independent validator
running on a DIFFERENT model (OpenAI o4-mini / Codex). Loops up
to --max-iter cycles until the validator emits verdict=pass, then
appends a single result line to the shared mailbox JSONL.

The SFA is invoked by scripts/phase2_sp_fanout.sh (CA-U07), which spins
up one sandbox per SP via SP15 `sbx-fork` and passes in a prepared
context bundle. Inside the sandbox, the mount of the main repo is
read-only — the coder writes diffs only to /tmp/coder_diffs/.

Usage:
    # Live run inside a sandbox (invoked by CA-U07 fanout)
    uv run agents/sfa/sfa_coder_validator_loop.py \\
        --sp SP15 \\
        --sp-manifest /tmp/sp15-bundle.yaml \\
        --mailbox audits/phase2-mailbox.jsonl \\
        --coder-model anthropic:claude-sonnet-4-6 \\
        --validator-model openai:o4-mini \\
        --max-iter 3

    # Dry-run smoke (no SDK calls, canned fixtures, mock validator)
    uv run agents/sfa/sfa_coder_validator_loop.py \\
        --sp SP16 \\
        --mailbox /tmp/phase2-smoke.jsonl \\
        --dry-run \\
        --max-iter 1

Dry-run mode never opens a network socket. It reads an embedded fixture
of coder findings, feeds them to a mock validator that returns
verdict=pass, and emits exactly one mailbox line. Use this to verify
the CLI/loop plumbing without burning sandbox budget or API credits.

Validator model constraint:
    --coder-model and --validator-model MUST differ. Matching strings
    exit immediately with
    "VALIDATOR_MODEL_VIOLATION: coder and validator must use different models".

Mailbox schema (one JSON object per line):
    {
      "sp": "SP15",
      "verdict": "pass" | "fail" | "escalate",
      "iterations": 2,
      "coder_model": "anthropic:claude-sonnet-4-6",
      "validator_model": "openai:o4-mini",
      "findings": [...],
      "final_verdict_json": {...},
      "timestamp": "2026-04-14T12:34:56Z",
      "dry_run": false
    }

Exit codes:
    0 = verdict=pass
    1 = verdict=fail or verdict=escalate
    2 = setup error (missing manifest, model constraint violation,
        live path invoked before CA-U10)
"""

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from rich.console import Console
from rich.panel import Panel

console = Console()


DEFAULT_MAILBOX = Path("audits/phase2-mailbox.jsonl")
DEFAULT_MAX_ITER = 3
TEMPERATURE = 0.1  # spec §5 — coder↔validator determinism

# Canned dry-run fixtures exercise the loop plumbing without any SDK calls.
# The shapes mirror the real coder-output / validator-verdict contracts so the
# wire format stays frozen when CA-U10 swaps in live dispatch.
DRY_RUN_CODER_FIXTURE: Dict[str, Any] = {
    "findings": [
        {
            "severity": "P1",
            "axis": "3-adversarial",
            "file": "apps/voice/voice_to_claude_code.py",
            "line": 1,
            "evidence": "dry-run canned evidence — no real scan performed",
            "why": "fixture finding exercising loop plumbing",
            "fix_suggestion": "not applicable (fixture)",
        }
    ],
    "proposed_diffs": "",
}

DRY_RUN_VERDICT_TEMPLATE: Dict[str, Any] = {
    "verdict": "pass",
    "iteration": 1,
    "model": "dry-run:mock",
    "sp_id": None,
    "summary": "dry-run mock verdict (no real validation performed)",
    "findings": [],
    "coder_assessment": {
        "findings_confirmed": 1,
        "findings_refuted": 0,
        "findings_fabricated": 0,
        "findings_missed_by_coder": 0,
        "static_checks_pass": True,
        "exception_violations": 0,
    },
    "continue_loop": False,
    "escalate_reason": None,
}


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def enforce_validator_model_constraint(coder: str, validator: str) -> None:
    """Hard-fail when coder and validator resolve to the same model string.

    The check is a case-insensitive equality on the full `provider:model`
    spec (or bare model name, for test convenience). Matching providers with
    different model families are allowed (e.g. `anthropic:claude-opus-4-6`
    vs `anthropic:claude-sonnet-4-6`), but identical strings are not.
    """
    if coder.strip().lower() == validator.strip().lower():
        print(
            "VALIDATOR_MODEL_VIOLATION: coder and validator must use different models",
            file=sys.stderr,
        )
        sys.exit(2)


@dataclass
class LoopResult:
    sp_id: str
    verdict: str
    iterations: int
    coder_model: str
    validator_model: str
    findings: List[Dict[str, Any]]
    final_verdict_json: Dict[str, Any]
    dry_run: bool
    escalate_reason: Optional[str] = None


def load_sp_manifest(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"SP manifest not found: {path}")
    with path.open() as fh:
        return yaml.safe_load(fh) or {}


def run_coder_pass_dry_run(sp_id: str, iteration: int) -> Dict[str, Any]:
    fixture = json.loads(json.dumps(DRY_RUN_CODER_FIXTURE))
    for finding in fixture["findings"]:
        finding["sp_id"] = sp_id
        finding["iteration"] = iteration
    return fixture


def run_validator_pass_dry_run(sp_id: str, iteration: int) -> Dict[str, Any]:
    verdict = json.loads(json.dumps(DRY_RUN_VERDICT_TEMPLATE))
    verdict["sp_id"] = sp_id
    verdict["iteration"] = iteration
    return verdict


def run_coder_pass_live(
    sp_id: str,
    manifest: Dict[str, Any],
    coder_model: str,
    previous_verdict: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Live coder pass — stubbed until CA-U10 wires the Anthropic tool-use loop.

    The tool-use loop (read_file / run_static_checks / run_smoke_tests /
    propose_diff / submit_findings) lives behind this seam so the dry-run
    smoke can land independently. CA-U10 (Phase 2 execution) is the first
    caller that exercises the live path; until then, invocation raises
    NotImplementedError so accidental live runs surface loudly.
    """
    raise NotImplementedError(
        "live coder pass stubbed until CA-U10 — rerun with --dry-run "
        f"(would have invoked {coder_model} on {sp_id})"
    )


def run_validator_pass_live(
    sp_id: str,
    coder_output: Dict[str, Any],
    validator_model: str,
    iteration: int,
    previous_verdict: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Live validator pass — stubbed until CA-U10 wires provider dispatch.

    CA-U10 will either (a) lazy-import anthropic + openai and dispatch
    directly, or (b) shell out to `just-prompt` once that package grows a
    non-MCP invocation path. Either way, the validator system
    prompt is loaded from .claude/agents/sandbox-validator-agent.md and
    the output JSON block is parsed into this function's return shape.
    """
    raise NotImplementedError(
        "live validator pass stubbed until CA-U10 — rerun with --dry-run "
        f"(would have invoked {validator_model} on {sp_id} @iter {iteration})"
    )


def append_to_mailbox(mailbox: Path, result: LoopResult) -> None:
    mailbox.parent.mkdir(parents=True, exist_ok=True)
    record: Dict[str, Any] = {
        "sp": result.sp_id,
        "verdict": result.verdict,
        "iterations": result.iterations,
        "coder_model": result.coder_model,
        "validator_model": result.validator_model,
        "findings": result.findings,
        "final_verdict_json": result.final_verdict_json,
        "timestamp": _utcnow(),
        "dry_run": result.dry_run,
    }
    if result.escalate_reason:
        record["escalate_reason"] = result.escalate_reason
    with mailbox.open("a") as fh:
        fh.write(json.dumps(record, separators=(",", ":")) + "\n")


def run_loop(args: argparse.Namespace) -> int:
    enforce_validator_model_constraint(args.coder_model, args.validator_model)

    mailbox = Path(args.mailbox)
    console.rule(f"[yellow]Coder↔Validator loop — {args.sp}[/yellow]")
    console.print(
        f"[dim]coder={args.coder_model} validator={args.validator_model} "
        f"max-iter={args.max_iter} dry_run={args.dry_run}[/dim]"
    )

    manifest: Optional[Dict[str, Any]] = None
    if not args.dry_run:
        if not args.sp_manifest:
            print("setup error: --sp-manifest required unless --dry-run", file=sys.stderr)
            return 2
        manifest = load_sp_manifest(Path(args.sp_manifest))

    previous_verdict: Optional[Dict[str, Any]] = None
    iteration = 0
    verdict_json: Dict[str, Any] = {}
    findings: List[Dict[str, Any]] = []

    while iteration < args.max_iter:
        iteration += 1
        console.print(f"[cyan]iter {iteration}/{args.max_iter}[/cyan]")

        if args.dry_run:
            coder_output = run_coder_pass_dry_run(args.sp, iteration)
        else:
            coder_output = run_coder_pass_live(
                args.sp, manifest or {}, args.coder_model, previous_verdict
            )

        if args.dry_run:
            verdict_json = run_validator_pass_dry_run(args.sp, iteration)
        else:
            verdict_json = run_validator_pass_live(
                args.sp,
                coder_output,
                args.validator_model,
                iteration,
                previous_verdict,
            )

        findings = verdict_json.get("findings", [])
        verdict = verdict_json.get("verdict", "escalate")
        border = "green" if verdict == "pass" else "yellow"
        console.print(
            Panel.fit(
                f"verdict={verdict} iteration={iteration} findings={len(findings)}",
                border_style=border,
            )
        )

        if verdict == "pass":
            break
        if verdict == "escalate":
            break
        # verdict == "fail" — either loop back or escalate on cap
        if iteration >= args.max_iter:
            verdict_json = {
                **verdict_json,
                "verdict": "escalate",
                "escalate_reason": verdict_json.get(
                    "escalate_reason",
                    f"iteration cap hit ({iteration}/{args.max_iter}) with unresolved findings",
                ),
            }
            break
        if not verdict_json.get("continue_loop", True):
            verdict_json = {
                **verdict_json,
                "verdict": "escalate",
                "escalate_reason": verdict_json.get(
                    "escalate_reason",
                    "validator rejected findings with continue_loop=False",
                ),
            }
            break
        previous_verdict = verdict_json

    terminal_verdict = verdict_json.get("verdict", "escalate")
    result = LoopResult(
        sp_id=args.sp,
        verdict=terminal_verdict,
        iterations=iteration,
        coder_model=args.coder_model,
        validator_model=args.validator_model,
        findings=findings,
        final_verdict_json=verdict_json,
        dry_run=args.dry_run,
        escalate_reason=verdict_json.get("escalate_reason"),
    )
    append_to_mailbox(mailbox, result)
    console.print(
        f"[green]mailbox line appended to {mailbox}[/green] "
        f"[dim](verdict={terminal_verdict}, iterations={iteration})[/dim]"
    )

    return 0 if terminal_verdict == "pass" else 1


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="sfa_coder_validator_loop.py",
        description="Phase 2 coder↔validator loop driver (runs inside an E2B sandbox).",
    )
    parser.add_argument("--sp", required=True, help="Sub-project id (SP1..SP16)")
    parser.add_argument(
        "--sp-manifest",
        default=None,
        help="Path to per-SP context bundle YAML (required unless --dry-run)",
    )
    parser.add_argument(
        "--max-iter",
        type=int,
        default=DEFAULT_MAX_ITER,
        help=f"Maximum coder↔validator cycles (default {DEFAULT_MAX_ITER})",
    )
    parser.add_argument(
        "--mailbox",
        default=str(DEFAULT_MAILBOX),
        help=f"JSONL mailbox path (default {DEFAULT_MAILBOX})",
    )
    parser.add_argument(
        "--coder-model",
        default="anthropic:claude-sonnet-4-6",
        help="Provider:model for the coder agent",
    )
    parser.add_argument(
        "--validator-model",
        default="openai:o4-mini",
        help="Provider:model for the validator (must differ from --coder-model)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the loop against canned fixtures (no SDK calls, no sandbox)",
    )
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    try:
        return run_loop(args)
    except NotImplementedError as e:
        print(f"not implemented: {e}", file=sys.stderr)
        return 2
    except FileNotFoundError as e:
        print(f"setup error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
