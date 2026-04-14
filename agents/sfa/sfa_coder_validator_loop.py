#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "anthropic>=0.47.1",
#   "openai>=1.30.0",
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
        --coder-model anthropic:claude-haiku-4-5 \\
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
    """Live coder pass — Anthropic tool-use loop (CA-U10).

    Drives claude-haiku-4-5 (or the --coder-model override) through up to
    MAX_TURNS tool-use cycles.  Tools available to the coder:
        read_file          — read any path in the sandbox read-only mount
        run_static_checks  — ruff + py_compile on a path
        run_smoke_tests    — pytest -x (no-credential tests)
        propose_diff       — write a unified diff to /tmp/coder_diffs/
        submit_findings    — terminate the loop and return structured findings

    The repo mount is read-only; propose_diff is the only path that writes, and
    it writes exclusively to /tmp/coder_diffs/<name>.patch.

    Returns a dict with shape identical to DRY_RUN_CODER_FIXTURE:
        {"findings": [...], "proposed_diffs": "<unified diff text>"}

    If the tool loop exhausts MAX_TURNS without submit_findings, a P0
    "tool-loop-exhausted" finding is injected so the validator can escalate.
    """
    import anthropic  # lazy import — only loaded on live path
    import random
    import subprocess
    import time

    MAX_TURNS = 12
    DEADLINE_TURN = MAX_TURNS - 2  # inject hard deadline warning at this turn index

    # ── Rate-limit retry helper (Bug D fix) ────────────────────────────────
    # CA-U28 Step G (16-SP fanout) had SP1/SP8/SP16 hit Anthropic 429 rate
    # limits. SP1's obox agent improvised a model switch (security incident,
    # leaked API key to fork log). SP8/SP16 wrote error JSONs and were
    # dropped. The root cause is the SFA has no retry logic — any 429 kills
    # the run immediately. Wrap messages.create in a bounded exponential
    # backoff loop that honors the server's Retry-After header when present.
    _MAX_RETRIES = 4
    _BACKOFF_BASE = 2.0  # seconds
    _BACKOFF_CAP = 60.0  # seconds

    def _create_with_retry(client_: "anthropic.Anthropic", **kwargs):
        """Call client_.messages.create with bounded 429 backoff."""
        attempt = 0
        while True:
            try:
                return client_.messages.create(**kwargs)
            except anthropic.RateLimitError as exc:
                attempt += 1
                if attempt > _MAX_RETRIES:
                    raise
                # Honor Retry-After header when present.
                retry_after = None
                try:
                    resp_headers = getattr(exc, "response", None)
                    if resp_headers is not None:
                        headers = getattr(resp_headers, "headers", {}) or {}
                        ra = headers.get("retry-after") or headers.get("Retry-After")
                        if ra:
                            retry_after = float(ra)
                except (AttributeError, ValueError, TypeError):
                    retry_after = None
                if retry_after is None:
                    # Exponential backoff with jitter
                    delay = min(_BACKOFF_CAP, _BACKOFF_BASE * (2 ** (attempt - 1)))
                    delay += random.uniform(0.0, delay * 0.25)
                else:
                    delay = min(_BACKOFF_CAP, retry_after + random.uniform(0.0, 1.5))
                console.print(
                    f"[yellow]Rate limited by Anthropic (attempt {attempt}/{_MAX_RETRIES}). "
                    f"Sleeping {delay:.1f}s before retry...[/yellow]"
                )
                time.sleep(delay)
            except anthropic.APIStatusError as exc:
                # 5xx retry with shorter backoff
                status = getattr(exc, "status_code", None)
                if status is not None and 500 <= status < 600:
                    attempt += 1
                    if attempt > _MAX_RETRIES:
                        raise
                    delay = min(_BACKOFF_CAP / 2, _BACKOFF_BASE * (2 ** (attempt - 1)))
                    console.print(
                        f"[yellow]Anthropic {status} (attempt {attempt}/{_MAX_RETRIES}). "
                        f"Sleeping {delay:.1f}s...[/yellow]"
                    )
                    time.sleep(delay)
                    continue
                raise

    # Strip provider prefix: "anthropic:claude-haiku-4-5" → "claude-haiku-4-5"
    model_id = coder_model.split(":", 1)[-1] if ":" in coder_model else coder_model

    sp_scope: List[str] = manifest.get("sp_scope", [])
    spec_refs: Dict[str, Any] = manifest.get("spec_refs", {})
    exceptions_subset: List[Any] = manifest.get("exceptions_subset", [])

    system_prompt = (
        f"<purpose>\n"
        f"You are an adversarial code reviewer performing Phase 2 of the ArhuGula "
        f"Comprehensive Audit.  Your job is to review sub-project {sp_id} "
        f"and submit structured findings.  You are operating inside a read-only E2B "
        f"sandbox.  You may only write to /tmp/coder_diffs/.\n"
        f"</purpose>\n\n"
        f"<turn_budget>\n"
        f"You have exactly {MAX_TURNS} tool-use turns.  Budget them strictly:\n"
        f"  Turns 1-{DEADLINE_TURN - 1}: read_file + run_static_checks exploration.\n"
        f"  Turn {DEADLINE_TURN}: a deadline warning will be injected — you MUST call\n"
        f"    submit_findings on your very next turn (turn {DEADLINE_TURN + 1}) or sooner.\n"
        f"  Turn {MAX_TURNS}: hard cap — the loop exits regardless.\n"
        f"CRITICAL: Exhausting all {MAX_TURNS} turns without calling submit_findings\n"
        f"produces a P0 meta-finding and wastes the entire iteration budget.\n"
        f"Submit partial findings early — the validator loop can request a second pass.\n"
        f"</turn_budget>\n\n"
        f"<instructions>\n"
        f"1. Use read_file to inspect files in the SP scope: {json.dumps(sp_scope)}\n"
        f"2. Focus on these axes:\n"
        f"   - Byte-parity drift vs upstream IndyDevDan source\n"
        f"   - Security vulnerabilities (command injection, path traversal, data exposure)\n"
        f"   - Hook bypass vectors and credential exposure patterns\n"
        f"   - Static analysis failures (ruff/mypy/py_compile issues)\n"
        f"   - SoT exception violations (audits/exceptions.md)\n"
        f"3. For each finding, collect file:line evidence before submitting\n"
        f"4. Use propose_diff for recommended fixes (writes to /tmp/coder_diffs/ only)\n"
        f"5. Call submit_findings to conclude — partial findings are acceptable\n"
        f"6. Severity: P0=security/critical, P1=correctness, P2=drift, P3=style\n"
        f"</instructions>\n\n"
        f"<spec_refs>\n"
        f"SoT section: {spec_refs.get('sot_section', 'N/A')}\n"
        f"Memory file: {spec_refs.get('memory_file', 'N/A')}\n"
        f"Active exceptions subset: {json.dumps(exceptions_subset)}\n"
        f"</spec_refs>"
    )
    if previous_verdict:
        unresolved = [
            f for f in previous_verdict.get("findings", [])
            if f.get("coder_status") not in ("confirmed", "fixed")
        ]
        system_prompt += (
            f"\n\n<previous_validator_verdict>\n"
            f"The validator returned findings in the prior iteration.  "
            f"Address each unresolved item below:\n"
            f"{json.dumps(unresolved, indent=2)}\n"
            f"Escalate reason: {previous_verdict.get('escalate_reason')}\n"
            f"</previous_validator_verdict>"
        )

    tools: List[Dict[str, Any]] = [
        {
            "name": "read_file",
            "description": "Read a file from the repository (sandbox read-only mount). Returns up to 8 000 characters.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to read"}
                },
                "required": ["path"],
            },
        },
        {
            "name": "run_static_checks",
            "description": "Run ruff check and python3 -m py_compile on a path. Returns combined stdout/stderr.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "sp_path": {"type": "string", "description": "Directory or .py file path to check"}
                },
                "required": ["sp_path"],
            },
        },
        {
            "name": "run_smoke_tests",
            "description": "Run pytest -x on no-credential tests for the SP scope. Returns up to 4 000 characters of output.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "sp_path": {"type": "string", "description": "Directory to discover tests in"}
                },
                "required": ["sp_path"],
            },
        },
        {
            "name": "propose_diff",
            "description": "Record a proposed fix as a unified diff. Writes to /tmp/coder_diffs/<name>.patch (sandbox scratch only).",
            "input_schema": {
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "File path being patched"},
                    "old": {"type": "string", "description": "Original content snippet"},
                    "new": {"type": "string", "description": "Replacement content snippet"},
                },
                "required": ["file", "old", "new"],
            },
        },
        {
            "name": "submit_findings",
            "description": "Submit final structured findings to end the review loop.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "findings": {
                        "type": "array",
                        "description": "List of finding objects",
                        "items": {
                            "type": "object",
                            "properties": {
                                "severity": {"type": "string", "enum": ["P0", "P1", "P2", "P3"]},
                                "axis": {"type": "string"},
                                "file": {"type": "string"},
                                "line": {"type": "integer"},
                                "evidence": {"type": "string"},
                                "why": {"type": "string"},
                                "fix_suggestion": {"type": "string"},
                            },
                            "required": ["severity", "axis", "file", "line", "evidence", "why"],
                        },
                    },
                    "summary": {"type": "string", "description": "One-line summary of the review"},
                },
                "required": ["findings", "summary"],
            },
        },
    ]

    # /tmp scratch dir for diffs (sandbox-safe — never touches repo mount)
    diffs_dir = Path("/tmp/coder_diffs")
    diffs_dir.mkdir(parents=True, exist_ok=True)
    accumulated_diffs: List[str] = []

    def _dispatch(tool_name: str, tool_input: Dict[str, Any]) -> str:
        if tool_name == "read_file":
            path = Path(tool_input["path"])
            try:
                return path.read_text(errors="replace")[:8000]
            except Exception as exc:
                return f"error reading {path}: {exc}"

        if tool_name == "run_static_checks":
            sp_path = tool_input["sp_path"]
            parts: List[str] = []
            for cmd in (
                ["ruff", "check", sp_path],
                ["python3", "-m", "py_compile", sp_path],
            ):
                try:
                    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                    label = cmd[0] if cmd[0] != "python3" else "py_compile"
                    out = (r.stdout + r.stderr).strip() or "(clean)"
                    parts.append(f"{label}: {out}")
                except Exception as exc:
                    parts.append(f"{cmd[0]}: unavailable ({exc})")
            return "\n".join(parts)

        if tool_name == "run_smoke_tests":
            sp_path = tool_input["sp_path"]
            try:
                r = subprocess.run(
                    [
                        "python3", "-m", "pytest", sp_path,
                        "-x", "--no-header", "-q",
                        "-k", "not credential and not api_key and not live",
                    ],
                    capture_output=True, text=True, timeout=120,
                )
                return (r.stdout + r.stderr)[:4000]
            except Exception as exc:
                return f"pytest unavailable: {exc}"

        if tool_name == "propose_diff":
            file_path = tool_input["file"]
            old_text = tool_input["old"]
            new_text = tool_input["new"]
            safe_name = file_path.replace("/", "_").replace(".", "_")
            diff_path = diffs_dir / f"{safe_name}.patch"
            diff_lines = [f"--- a/{file_path}\n", f"+++ b/{file_path}\n"]
            diff_lines += [f"-{line}\n" for line in old_text.splitlines()]
            diff_lines += [f"+{line}\n" for line in new_text.splitlines()]
            diff_text = "".join(diff_lines)
            diff_path.write_text(diff_text)
            accumulated_diffs.append(diff_text)
            return f"diff written to {diff_path}"

        if tool_name == "submit_findings":
            return "__SUBMIT_FINDINGS__"

        return f"unknown tool: {tool_name}"

    # ── tool-use loop ──────────────────────────────────────────────────────────
    client = anthropic.Anthropic()
    messages: List[Dict[str, Any]] = [
        {
            "role": "user",
            "content": (
                f"Review sub-project {sp_id}.  "
                f"SP scope globs: {json.dumps(sp_scope)}.  "
                f"Read the relevant files, run static checks, identify all findings, "
                f"then call submit_findings with your complete results."
            ),
        }
    ]

    submitted_findings: Optional[Dict[str, Any]] = None

    for _turn in range(MAX_TURNS):
        # Inject deadline warning at DEADLINE_TURN to force submit_findings on next turn
        if _turn == DEADLINE_TURN and submitted_findings is None:
            deadline_msg = (
                f"\u26a0 DEADLINE: {MAX_TURNS - _turn} turn(s) remaining. "
                f"You MUST call submit_findings on your next turn with whatever "
                f"findings you have found so far. Partial findings are acceptable — "
                f"the validator will review and the loop can iterate if needed."
            )
            messages.append({"role": "user", "content": deadline_msg})

        response = _create_with_retry(
            client,
            model=model_id,
            max_tokens=4096,
            temperature=TEMPERATURE,
            system=system_prompt,
            tools=tools,  # type: ignore[arg-type]
            messages=messages,  # type: ignore[arg-type]
        )

        # Record assistant turn
        messages.append({"role": "assistant", "content": response.content})

        tool_results: List[Dict[str, Any]] = []
        has_tool_use = False

        for block in response.content:
            if block.type != "tool_use":
                continue
            has_tool_use = True
            tool_output = _dispatch(block.name, block.input)

            if tool_output == "__SUBMIT_FINDINGS__":
                submitted_findings = {
                    "findings": block.input.get("findings", []),
                    "proposed_diffs": "\n\n".join(accumulated_diffs),
                }
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": "findings submitted"}
                )
            else:
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": tool_output}
                )

        if submitted_findings is not None:
            return submitted_findings

        if not has_tool_use or response.stop_reason == "end_turn":
            break

        if tool_results:
            messages.append({"role": "user", "content": tool_results})

    # Loop exhausted without submit_findings — inject P0 meta-finding
    return {
        "findings": [
            {
                "severity": "P0",
                "axis": "0-meta",
                "file": sp_id,
                "line": 0,
                "evidence": (
                    f"coder tool-use loop exhausted {MAX_TURNS} turns "
                    f"without calling submit_findings"
                ),
                "why": "loop budget exceeded — coder may be stuck in exploration",
                "fix_suggestion": (
                    "investigate coder system prompt; consider reducing sp_scope "
                    "or increasing --max-iter"
                ),
                "sp_id": sp_id,
            }
        ],
        "proposed_diffs": "\n\n".join(accumulated_diffs),
    }


def _load_validator_system_prompt() -> str:
    """Load sandbox-validator-agent.md body (everything after the closing ---)."""
    agent_path = Path(__file__).parents[2] / ".claude" / "agents" / "sandbox-validator-agent.md"
    if not agent_path.exists():
        # Fallback: walk up from cwd (handles invocation from repo root)
        agent_path = Path(".claude/agents/sandbox-validator-agent.md")
    text = agent_path.read_text()
    # Strip YAML frontmatter: content after the second "---\n" delimiter
    parts = text.split("---\n", 2)
    return parts[2].strip() if len(parts) >= 3 else text.strip()


def _parse_verdict_json(text: str) -> Optional[Dict[str, Any]]:
    """Extract and parse the first ```json ... ``` block from a response string."""
    import re
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None


def _hard_fail_verdict(
    sp_id: str,
    validator_model: str,
    iteration: int,
    reason: str,
) -> Dict[str, Any]:
    return {
        "verdict": "escalate",
        "iteration": iteration,
        "model": validator_model,
        "sp_id": sp_id,
        "summary": reason,
        "findings": [],
        "coder_assessment": {
            "findings_confirmed": 0,
            "findings_refuted": 0,
            "findings_fabricated": 0,
            "findings_missed_by_coder": 0,
            "static_checks_pass": False,
            "exception_violations": 0,
        },
        "continue_loop": False,
        "escalate_reason": reason,
    }


def run_validator_pass_live(
    sp_id: str,
    coder_output: Dict[str, Any],
    validator_model: str,
    iteration: int,
    previous_verdict: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Live validator pass — OpenAI o4-mini adversarial review (CA-U10).

    Loads the validator system prompt from
    .claude/agents/sandbox-validator-agent.md (body after frontmatter),
    builds the structured user payload, and calls o4-mini at temperature 0.1.
    Parses the fenced ```json block from the response.  On parse failure,
    retries once; on second failure returns a hard-fail escalate verdict so
    the loop can surface it cleanly.

    The validator_model arg should be "openai:o4-mini" — the "openai:" prefix
    is stripped before passing to the OpenAI client.
    """
    import openai  # lazy import — only loaded on live path

    # Strip provider prefix: "openai:o4-mini" → "o4-mini"
    model_id = validator_model.split(":", 1)[-1] if ":" in validator_model else validator_model

    system_prompt = _load_validator_system_prompt()

    # Build structured user payload matching the input schema in sandbox-validator-agent.md
    sp_scope: List[str] = []  # not passed to validator; it reads from coder findings
    spec_refs: Dict[str, Any] = {}
    user_payload: Dict[str, Any] = {
        "sp_id": sp_id,
        "sp_scope": sp_scope,
        "spec_refs": spec_refs,
        "coder_findings": coder_output.get("findings", []),
        "coder_proposed_diffs": coder_output.get("proposed_diffs", ""),
        "iteration": iteration,
        "max_iterations": DEFAULT_MAX_ITER,
        "previous_verdict": previous_verdict,
    }
    user_message = (
        "Validate the following coder review output and return your verdict as a "
        "```json ... ``` block matching the output schema.\n\n"
        f"```json\n{json.dumps(user_payload, indent=2)}\n```"
    )

    client = openai.OpenAI()

    def _call_once() -> Optional[Dict[str, Any]]:
        # o4-mini (and some other reasoning models) reject the temperature
        # parameter entirely — omit it for those models.
        _o_series = model_id.startswith("o") and model_id[1:2].isdigit()
        create_kwargs: Dict[str, Any] = dict(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        if not _o_series:
            create_kwargs["temperature"] = TEMPERATURE
        response = client.chat.completions.create(**create_kwargs)
        content = response.choices[0].message.content or ""
        return _parse_verdict_json(content)

    # First attempt
    verdict = _call_once()
    if verdict is None:
        # Retry once
        verdict = _call_once()

    if verdict is None:
        return _hard_fail_verdict(
            sp_id, validator_model, iteration,
            "validator output unparseable after 2 attempts",
        )

    # Ensure required fields are present; fill safe defaults where missing
    verdict.setdefault("sp_id", sp_id)
    verdict.setdefault("iteration", iteration)
    verdict.setdefault("model", validator_model)
    verdict.setdefault("continue_loop", verdict.get("verdict") == "fail")
    verdict.setdefault("escalate_reason", None)
    verdict.setdefault("findings", [])
    verdict.setdefault("coder_assessment", {
        "findings_confirmed": 0,
        "findings_refuted": 0,
        "findings_fabricated": 0,
        "findings_missed_by_coder": 0,
        "static_checks_pass": True,
        "exception_violations": 0,
    })

    return verdict


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
        default="anthropic:claude-haiku-4-5",
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
