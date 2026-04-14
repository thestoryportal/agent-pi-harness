# Comprehensive Audit — Implementation Plan

## Metadata
- Source scout: `/Users/robertrhu/Projects/arhugula/audits/comprehensive-audit-scout.md`
- Spec: `/Users/robertrhu/Projects/arhugula/audits/comprehensive-audit-spec.md`
- Total units: 22
- Critical path: 10 units (CA-U01 → CA-U02 → CA-U04 → CA-U06/07 → CA-U10 → CA-U17 → CA-U18 → CA-U19 → CA-U20)
- Estimated total effort: ~4.5 hr build + ~2.5 hr execution (Phase 2 dominates at ~1.5 hr wall-clock)
- Orchestration: Option B default (Claude Code native); Option A (Pi) annotated for CA-U21/CA-U22

---

## Agent assignment map

| Unit | Subagent | Tool requirements |
|------|----------|-------------------|
| CA-U01 | @builder (or main session) | Read, Grep, Glob |
| CA-U02 | @builder | Write |
| CA-U03 | @builder | Read, Edit (justfile) |
| CA-U04 | main session | Bash (uv run) |
| CA-U05 | @builder | Write |
| CA-U06 | @builder | Write |
| CA-U07 | @builder | Write |
| CA-U08 | main session | Bash (just-prompt smoke) |
| CA-U09 | main session | Bash (sbx --help) |
| CA-U10 | main session | Bash (phase2_sp_fanout.sh) |
| CA-U11 | @builder | Write |
| CA-U12 | @builder | Write |
| CA-U13 | @builder | Write |
| CA-U14 | @builder | Write |
| CA-U15 | main session | Bash (uv run × 4 SFAs) |
| CA-U16 | @builder | Write |
| CA-U17 | @cross-model-consensus-agent | Bash (just-prompt) |
| CA-U18 | @builder | Read, Write |
| CA-U19 | @builder | Write |
| CA-U20 | @builder | Write |
| CA-U21 | main session (Option A only) | Bash |
| CA-U22 | @builder (Option A only) | Edit (justfile) |

---

## Execution schedule

**Wave 0 — Precheck (sequential, ~10 min)**
- CA-U01

**Wave 1 — Infra build (parallelizable within wave, ~90 min total)**
Group A (Phase 1 infra): CA-U02, CA-U03
Group B (Phase 2 infra): CA-U05, CA-U06, CA-U07, CA-U08, CA-U09
Group C (Phase 3 infra): CA-U11, CA-U12, CA-U13, CA-U14
Group D (Phase 4 infra): CA-U16
Group F (Option A only): CA-U21, CA-U22

CA-U02 must precede CA-U03. CA-U05 + CA-U08 must precede CA-U06. CA-U06 + CA-U09 must precede CA-U07.

**Wave 2 — Phase 1 execution (~10 min)**
- CA-U04

**Wave 3 — Phase 2 + Phase 3 parallel execution (~1.5 hr wall-clock)**
- CA-U10 (heavy, dominated by slowest sandbox)
- CA-U15 (can run concurrently with CA-U10 in a second terminal)

**Decision gate (user must acknowledge Exception 29 activation before CA-U10)**

**Wave 4 — Phase 4 consensus (~15 min)**
- CA-U17

**Wave 5 — Phase 5 tail (~30 min)**
- CA-U18, CA-U19, CA-U20 (sequential)

---

## Per-unit plans

---

### CA-U01 — Run /find-skills precheck + document matches

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/audits/phase0-skill-matches-2026-04-14.md`

**Pattern reference:**
No code artifact — this is a session invocation. Follow the Phase 0 spec section (spec §3) which calls `/find-skills` against the global library catalog. The global catalog lives at `~/.claude/skills/library/library.yaml`.

**Implementation sketch:**
```
1. Open Claude Code session
2. Run /find-skills with keyword list from spec §3:
   diff-analyzer, dead-code, drift-detector, ledger-auditor, hook-graph,
   namespace-collision, sot-consistency, byte-diff, exception-auditor,
   cross-model-consensus
3. For each keyword, record: skill name if matched / "no match"
4. Evaluate: can any match replace one of the 6 planned SFAs or 3 subagents?
5. Write verdict table to audits/phase0-skill-matches-2026-04-14.md
   Columns: Keyword | Match | Artifact it could replace | Decision (use / skip)
6. Result informs whether the full artifact list (P1-A1 through P4-A1) stands or shrinks
```

**Test spec:**
- File exists at the above path after the session
- File contains a verdict row for each of the 10 keywords
- Each row has an explicit "Decision" column value

**Validation:**
```bash
ls /Users/robertrhu/Projects/arhugula/audits/phase0-skill-matches-2026-04-14.md
grep -c "| Decision" /Users/robertrhu/Projects/arhugula/audits/phase0-skill-matches-2026-04-14.md
# Expect ≥ 1 (header)
```

**Wave:** 0
**Commit:** Single commit: `audit(CA): Phase 0 skill-match precheck report`
**Risk:** Low. Read-only session.

---

### CA-U02 — Build `sfa_byte_diff_audit.py` (P1-A1)

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_byte_diff_audit.py`

**Pattern reference:**
`/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_bash_editor_agent_anthropic_v3.py` lines 1-9 — uv-run shebang + inline `/// script` dependency block (the file does not yet exist in the SFA dir; this is a new create).

`/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_codebase_context_agent_v3.py` lines 67-134 — `git_list_files` tool pattern using `subprocess.run("git ls-files", ...)` + `concurrent.futures.ThreadPoolExecutor` for parallelism.

`/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_duckdb_anthropic_v2.py` lines 1-60 — structured `AGENT_PROMPT` with `<purpose>/<instructions>` XML envelope + Anthropic tool-use loop.

**Implementation sketch:**
```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["anthropic>=0.47.1", "rich>=13.7.0"]
# ///

# Inline CLI: --sp (optional, default=all), --exceptions audits/exceptions.md,
#             --clones ~/Projects/indydevdan-harness-research/research/full-clones/,
#             --output audits/phase1-byte-parity-<date>.md

# Tools exposed to the Anthropic tool-use loop:
#   read_sot_sp_mapping(sp_id) → dict of {arhugula_path: upstream_path}
#   diff_files(local_path, upstream_path) → {status: MATCH|DRIFT|MISSING}
#   lookup_exception(path, exceptions_md) → exception_id or None
#   emit_row(sp_id, path, status, exception_id_or_None)
#   write_report(rows, output_path)

# Main agent loop:
#   1. For SP in [1..16] (or --sp filter):
#      a. read_sot_sp_mapping → list of (local, upstream) pairs
#      b. For each pair: diff_files → status
#      c. If DRIFT: lookup_exception → covered/unexplained
#   2. write_report → structured markdown table per SP
#      Columns: SP | File | Status | Exception | Notes
#   3. Exit 0 if zero DRIFT-unexplained; exit 1 otherwise

# Parallelism: xargs-style via concurrent.futures.ThreadPoolExecutor for diff_files
# No Anthropic calls needed for the diff itself — only for the optional
# "explain drift" summarization at the end (use sparingly to avoid cost)
```

**Test spec:**
- `uv run /Users/robertrhu/Projects/arhugula/agents/sfa/sfa_byte_diff_audit.py --help` exits 0
- `uv run ... --sp SP9 --dry-run` (mode that lists files without calling Anthropic) returns at least one row in the output
- With a known-matching SP (any SP with all files MATCH), exit code 0
- With an artificially introduced 1-char difference in a temp copy, exit code 1

**Validation:**
```bash
uv run /Users/robertrhu/Projects/arhugula/agents/sfa/sfa_byte_diff_audit.py --help
# output must contain: --sp, --exceptions, --clones, --output
```

**Wave:** 1 (Group A)
**Commit:** Batched with CA-U03: `build(CA-U02-U03): Phase 1 infra — byte-diff SFA + justfile recipe`
**Risk:** Low. New file, no existing code modified.

---

### CA-U03 — Add `just phase1-byte-diff` recipe

**Artifacts:**
- Modify: `/Users/robertrhu/Projects/arhugula/justfile`

**Pattern reference:**
`/Users/robertrhu/Projects/arhugula/justfile` lines 348-390 (SP15 `sbx-*` block) — comment block format with Exception citation, recipe name, and `uv run` invocation. The recipe sits in its own SP-labeled block with an ArhuGula-specific Exception note.

**Implementation sketch:**
```
New block in justfile after the existing SP15/SP16 blocks:

# === Comprehensive Audit Infrastructure ===
# ArhuGula-specific: audit tooling is Tier 3 (Exception 1).
# No upstream justfile counterpart.

# Phase 1: Byte-parity sweep across all 16 SPs
phase1-byte-diff *args:
    uv run agents/sfa/sfa_byte_diff_audit.py {{args}}

# Phase 3 cross-cutting checks
phase3-cross-cutting *args:
    uv run agents/sfa/sfa_exception_ledger_auditor.py {{args}}
    uv run agents/sfa/sfa_hook_coverage_matrix.py {{args}}
    uv run agents/sfa/sfa_namespace_collision_detector.py {{args}}
    uv run agents/sfa/sfa_sot_consistency_checker.py {{args}}

# Phase 2 fan-out (16-parallel SP sandboxes)
phase2-fanout *args:
    bash scripts/phase2_sp_fanout.sh {{args}}
```
(Additional recipes phase4-consensus, phase5-aggregate can be stubs referencing the relevant subagents.)

**Test spec:**
- `just --list | grep phase1-byte-diff` returns the recipe
- `just phase1-byte-diff --help` delegates to the SFA and exits 0

**Validation:**
```bash
cd /Users/robertrhu/Projects/arhugula && just --list | grep phase1
# Expected: phase1-byte-diff
```

**Wave:** 1 (Group A, after CA-U02)
**Commit:** Batched with CA-U02
**Risk:** Low. Additive justfile edit.

---

### CA-U04 — Execute Phase 1 — byte-parity sweep

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/audits/phase1-byte-parity-2026-04-14.md`

**Pattern reference:**
Execution unit — no new code. Invokes CA-U02 artifact via CA-U03 recipe.

**Implementation sketch:**
```
1. Run: just phase1-byte-diff \
     --exceptions /Users/robertrhu/Projects/arhugula/audits/exceptions.md \
     --clones ~/Projects/indydevdan-harness-research/research/full-clones/ \
     --output /Users/robertrhu/Projects/arhugula/audits/phase1-byte-parity-2026-04-14.md
2. Review exit code:
   - Exit 0 → all Tier 1 drift is exception-covered; note in report
   - Exit 1 → unexplained drift list in report; becomes Phase 2 priority targets
3. Do NOT commit yet — Phase 1 report is a runtime artifact, commit after review
```

**Test spec:**
- Report file exists and contains a table with columns: SP | File | Status | Exception
- Every DRIFT row has either an exception ID or the text "UNEXPLAINED"
- Exit code matches presence/absence of unexplained drift

**Validation:**
```bash
ls /Users/robertrhu/Projects/arhugula/audits/phase1-byte-parity-2026-04-14.md
grep "UNEXPLAINED" /Users/robertrhu/Projects/arhugula/audits/phase1-byte-parity-2026-04-14.md
# If zero lines: all drift is exception-covered (pass)
# If nonzero: review each before proceeding to Phase 2
```

**Wave:** 2
**Commit:** Deferred — commit Phase 1 report together with Phase 2 report once both are confirmed clean: `audit(CA): Phase 1 byte-parity sweep report`
**Risk:** Low. Read-only execution.

---

### CA-U05 — Build `@sandbox-validator-agent` subagent (P2-A1)

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/.claude/agents/sandbox-validator-agent.md`

**Pattern reference:**
`/Users/robertrhu/Projects/arhugula/.claude/agents/team/validator.md` lines 1-7 — frontmatter schema (`name`, `description`, `model`, `disallowedTools`, `color`).

`/Users/robertrhu/Projects/arhugula/.claude/agents/security.md` lines 1-20 — adversarial posture: `tools: Read, Grep, Glob`, `disallowedTools: Write, Edit, Bash`, `permissionMode: plan`, the attack-vector breakdown structure, and the Threat Level / finding format.

**Implementation sketch:**
```markdown
---
name: sandbox-validator-agent
description: >
  Adversarial validator for the Phase 2 coder↔validator loop. Use ONLY inside
  an E2B sandbox. MUST run under a different model than the coder agent
  (enforced: GPT-5 or Gemini via just-prompt; never Claude). Validates coder
  findings + diffs, runs an independent adversarial pass, and emits a structured
  JSON verdict.
tools: Read, Grep, Glob
disallowedTools: Write, Edit, Bash
model: sonnet            # placeholder — actual routing via just-prompt
permissionMode: plan
maxTurns: 20
---

# Purpose
You are an adversarial validator operating inside an E2B sandbox.
IMPORTANT: You MUST be invoked via just-prompt routing with a non-Anthropic
model (GPT-5 or Gemini). This is a hard requirement for coder/validator
independence. If invoked directly as a Claude subagent, reject the task and
report "VALIDATOR_MODEL_VIOLATION".

## Mandate
Given: coder findings + proposed diffs (passed as context)
Produce: structured JSON verdict at temperature=0.1

## Workflow
1. Read the coder's findings list (passed as <coder-findings> context block)
2. Independently verify each finding by reading the cited file:line
3. Run an adversarial pass: look for findings the coder MISSED
4. Assess each proposed diff for correctness + regression risk
5. Emit verdict JSON:
   {"verdict": "pass|fail|escalate",
    "findings": [{"severity":"P0..P3","file":"...","line":N,"evidence":"...","fix":"..."}],
    "iterations": N,
    "final_diff": "..."}

## Adversarial checks (from @security model)
- Command injection vectors the coder's diffs may introduce
- Path traversal not caught by static analysis
- Hook bypass patterns (fail-open vs fail-closed)
- Data exposure through logs / error messages

## Verdict rules
- pass: zero P0 findings, coder's diffs look correct
- fail: ≥1 P0 finding, or coder diffs contain regressions → return to coder
- escalate: iteration cap reached (iter≥3) OR 3-way model disagreement
```

**Test spec:**
- `grep "VALIDATOR_MODEL_VIOLATION"` present in agent body
- Frontmatter parses correctly (yaml-lint passes)
- Agent is listable via `claude agents list`

**Validation:**
```bash
head -10 /Users/robertrhu/Projects/arhugula/.claude/agents/sandbox-validator-agent.md
# Must show valid yaml frontmatter with name: sandbox-validator-agent
python3 -c "import yaml; yaml.safe_load(open('/Users/robertrhu/Projects/arhugula/.claude/agents/sandbox-validator-agent.md').read().split('---')[1])"
```

**Wave:** 1 (Group B)
**Commit:** Batched with CA-U06/CA-U07: `build(CA-U05-U07): Phase 2 infra — validator subagent + loop SFA + fanout script`
**Risk:** Medium. New subagent definition; the different-model constraint is enforced via instructions, not technical enforcement. Documented limitation.

---

### CA-U06 — Build `sfa_coder_validator_loop.py` (P2-A2)

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_coder_validator_loop.py`

**Pattern reference:**
`/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_bash_editor_agent_anthropic_v3.py` lines 1-9 — shebang + inline dependency block.

`/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_codebase_context_agent_v3.py` lines 719-936 — main agent loop pattern: `while True` with `compute_iterations` guard, `messages.append(...)` conversation state, tool dispatch, `break_loop` flag.

`/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_duckdb_anthropic_v2.py` lines 36-60 — `AGENT_PROMPT` with `<purpose>/<instructions>` envelope and structured output.

The loop architecture (coder→validator→coder) is described in spec §5.

**Implementation sketch:**
```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["anthropic>=0.47.1", "rich>=13.7.0", "e2b>=0.4.0"]
# ///

# CLI: --sp SP1..SP16 --sp-manifest path --max-iter 3
#      --mailbox audits/phase2-mailbox.jsonl
#      --coder-model claude-opus-4-6
#      --validator-model gpt-5  (enforced != coder-model)

# Tool set for the inner Anthropic coder agent:
#   read_file(path) → content
#   run_static_checks(sp_path) → ruff/ty/mypy output
#   run_smoke_tests(sp_path) → pytest -x no-credential tests
#   propose_diff(file, old, new) → stores diff in /tmp/coder_diffs/
#   submit_to_validator(findings_list, diff_list) → invokes validator via just-prompt

# Main loop (runs inside E2B sandbox):
#   iter_count = 0
#   while iter_count < max_iter:
#     coder_findings = run_coder_pass(sp_manifest)
#     validator_verdict = run_validator_pass(coder_findings)  # different model
#     if validator_verdict["verdict"] == "pass" or iter_count == max_iter-1:
#       emit_to_mailbox(sp_id, verdict, iter_count)
#       break
#     iter_count += 1
#   if iter_count == max_iter and verdict != "pass":
#     emit_to_mailbox(sp_id, "escalate", iter_count)

# Mailbox emit: append JSON line to audits/phase2-mailbox.jsonl
# Schema: {"sp": N, "verdict": "...", "findings": [...], "iterations": N, ...}
```

**Test spec:**
- `uv run sfa_coder_validator_loop.py --help` exits 0
- With `--max-iter 1 --dry-run --sp SP16` (no sandbox, mock validator): emits one mailbox line
- Validator model validation: `--validator-model claude-opus-4-6` with `--coder-model claude-opus-4-6` must error: "VALIDATOR_MODEL_VIOLATION: coder and validator must use different models"

**Validation:**
```bash
uv run /Users/robertrhu/Projects/arhugula/agents/sfa/sfa_coder_validator_loop.py --help
# Must show --sp, --max-iter, --mailbox, --coder-model, --validator-model
```

**Wave:** 1 (Group B, after CA-U05 + CA-U08)
**Commit:** Batched with CA-U05/CA-U07
**Risk:** Medium. Depends on E2B SDK + just-prompt API keys. Blocker: different-model constraint requires at least 1 non-Anthropic key (see Blocker 3).

---

### CA-U07 — Build `scripts/phase2_sp_fanout.sh` (P2-A3)

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/scripts/phase2_sp_fanout.sh`

**Pattern reference:**
No direct upstream analogue. Pattern is a bash driver that calls `just sbx-fork` (already built in SP15, justfile line 362-363) in a parallel loop. The `sbx-fork` recipe at `/Users/robertrhu/Projects/arhugula/justfile` line 362 provides the invocation shape: `just sbx-fork <repo> <prompt> <forks>`.

**Implementation sketch:**
```bash
#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/phase2_sp_fanout.sh [--sp SP1..SP16] [--dry-run]
# Kicks off 1 sbx-fork per SP (or the filtered subset), collects mailbox output.

MAILBOX="audits/phase2-mailbox.jsonl"
DATE=$(date +%Y-%m-%d)
SUMMARY_OUT="audits/phase2-summary-${DATE}.md"

SPS=(SP1 SP2 SP3 SP4 SP5 SP6 SP7 SP8 SP9 SP10 SP11 SP12 SP13 SP14 SP15 SP16)
# Parse --sp filter if provided

for SP in "${SPS[@]}"; do
  SP_REPORT="audits/phase2-${SP,,}-review-${DATE}.md"
  SP_PROMPT="Run sfa_coder_validator_loop.py for ${SP}. Output findings to ${SP_REPORT}. Append verdict to ${MAILBOX}."
  # Fire sbx-fork in background, capture pid
  just sbx-fork "$(pwd)" "${SP_PROMPT}" 1 &
  echo "Launched ${SP} (pid=$!)"
done

wait   # Block until all 16 complete (or timeout)

# Aggregate mailbox into summary
python3 -c "
import json, sys
rows = [json.loads(l) for l in open('${MAILBOX}')]
print(f'Phase 2 results: {len(rows)} SPs processed')
for r in rows:
  print(f'  {r[\"sp\"]}: {r[\"verdict\"]} ({r[\"iterations\"]} iters)')
" > "${SUMMARY_OUT}"
```

**Test spec:**
- `bash scripts/phase2_sp_fanout.sh --dry-run --sp SP16` runs without launching a sandbox, prints expected invocation commands
- Mailbox file path is configurable (no hardcoded paths)
- Script exits nonzero if more than 0 SPs emit "escalate" verdict

**Validation:**
```bash
chmod +x /Users/robertrhu/Projects/arhugula/scripts/phase2_sp_fanout.sh
bash /Users/robertrhu/Projects/arhugula/scripts/phase2_sp_fanout.sh --help
```

**Wave:** 1 (Group B, after CA-U06 + CA-U09)
**Commit:** Batched with CA-U05/CA-U06
**Risk:** Medium. No upstream pattern for the shell driver. Sandbox launches are expensive; `--dry-run` mode is load-bearing for testing without cost.

---

### CA-U08 — Verify SP4 just-prompt multi-model routing

**Artifacts:**
- None (verification unit)

**Pattern reference:**
SP4 MCP server lives at `mcp/just-prompt/`. The recipe `just sfa-duckdb` (justfile line 92) shows the `uv run` invocation pattern. The just-prompt multi-model invocation is documented in SoT §4.4.

**Implementation sketch:**
```
1. Verify just-prompt MCP server is accessible:
   just --list | grep prompt
2. Check API keys present (but NOT stored to disk):
   echo $OPENAI_API_KEY | head -c4   # expect "sk-p" or similar
   echo $GOOGLE_API_KEY | head -c2   # expect "AI"
3. Fire a minimal 3-model probe:
   uv run just-prompt --models "anthropic:claude-sonnet-4-6 openai:gpt-4o google:gemini-2.0-flash" \
     --prompt "Say the word PONG only"
4. Confirm all 3 models return a response (not an API error)
5. Document result: which models available, which failed
```

**Test spec:**
- At least 2 non-Anthropic models respond successfully (Phase 4 minimum for diversity)
- If only 1 non-Anthropic model available: flag Blocker 3 as "degraded mode" and note in pre-run checklist
- Anthropic model must always succeed (it is the coder model in Phase 2)

**Validation:**
```bash
# Run from /Users/robertrhu/Projects/arhugula
just --list | grep -E "prompt|multi"
echo "OpenAI key present: $([ -n "$OPENAI_API_KEY" ] && echo YES || echo NO)"
echo "Google key present: $([ -n "$GOOGLE_API_KEY" ] && echo YES || echo NO)"
```

**Wave:** 1 (Group B, independent)
**Commit:** Not committed (verification only)
**Risk:** Low. Read-only environment check.

---

### CA-U09 — Verify SP15 `sbx-fork` + E2B runtime

**Artifacts:**
- None (verification unit)

**Pattern reference:**
SP15 justfile block at `/Users/robertrhu/Projects/arhugula/justfile` lines 348-368, specifically `sbx *args` and `sbx-fork repo prompt forks` recipes.

**Implementation sketch:**
```
1. Verify sbx CLI is accessible (does NOT require E2B_API_KEY):
   just sbx --help
   → must print usage without error
2. Verify sbx-fork recipe is wired:
   just --list | grep sbx-fork
3. Check E2B_API_KEY status WITHOUT activating dormant findings:
   [ -n "$E2B_API_KEY" ] && echo "KEY PRESENT — Exception 29 dormant findings
   would become active at Phase 2 kickoff" || echo "KEY ABSENT — must set
   before CA-U10; acknowledge Exception 29 before proceeding"
4. Do NOT run sbx-fork yet. This is a dry-check only.
5. Document status: sbx CLI OK / E2B key absent (expected before acknowledgment)
```

**Test spec:**
- `just sbx --help` exits 0
- `just sbx-fork --help` or equivalent dry invocation exits 0
- Script correctly identifies KEY ABSENT state without error

**Validation:**
```bash
cd /Users/robertrhu/Projects/arhugula && just sbx --help 2>&1 | head -5
just --list | grep sbx-fork
```

**Wave:** 1 (Group B, independent)
**Commit:** Not committed
**Risk:** Medium. If `E2B_API_KEY` is already in `.env`, the check will print the activation warning. The builder must not proceed to CA-U10 without user acknowledgment.

---

### CA-U10 — Execute Phase 2 — 16-parallel SP fan-out with coder↔validator loops

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/audits/phase2-sp<N>-review-2026-04-14.md` (16 files, one per SP)
- Create: `/Users/robertrhu/Projects/arhugula/audits/phase2-summary-2026-04-14.md`
- Create: `/Users/robertrhu/Projects/arhugula/audits/phase2-mailbox.jsonl`

**Pattern reference:**
Execution unit. CA-U07 artifact is the driver. CA-U04 output (unexplained drift list) is the priority-target feed for the coder agent context.

**Implementation sketch:**
```
PRE-CONDITION GATE (user must confirm ALL of the following before proceeding):
  [ ] Exception 29 activation acknowledged (E2B_API_KEY in env = dormant findings active)
  [ ] Phase 2 cost budget ~$12 confirmed
  [ ] Exception 14 / 24 / 28 runtime activation notes reviewed
  [ ] At least 2 non-Anthropic models available (CA-U08 confirmed)
  [ ] E2B_API_KEY is set in .env

EXECUTION:
1. Export E2B_API_KEY to environment
2. Run: bash scripts/phase2_sp_fanout.sh \
       --mailbox audits/phase2-mailbox.jsonl \
       --date 2026-04-14
3. Monitor: 16 sbx-fork processes in background
4. On completion: verify all 16 per-SP reports exist
5. On any sandbox crash: note which SP, continue with remaining 15
6. Run summary aggregation: generates phase2-summary-2026-04-14.md
```

**Test spec:**
- All 16 `audits/phase2-sp<N>-review-2026-04-14.md` files exist (or fewer if sandboxes crashed, documented)
- Each report contains a `verdict: pass|fail|escalate` line
- `audits/phase2-mailbox.jsonl` has 16 JSON lines (one per SP)
- Zero coder↔validator loops left open (all have `"iterations": N` where N ≤ 3)
- Any "escalate" verdicts are listed explicitly in the summary as "requires human review"

**Validation:**
```bash
ls /Users/robertrhu/Projects/arhugula/audits/phase2-sp*-review-2026-04-14.md | wc -l
# Expected: 16 (or documented count if sandboxes crashed)
grep -c '"verdict"' /Users/robertrhu/Projects/arhugula/audits/phase2-mailbox.jsonl
# Expected: 16
grep "escalate" /Users/robertrhu/Projects/arhugula/audits/phase2-mailbox.jsonl | wc -l
# Zero = clean pass; nonzero = items for Phase 4
```

**Wave:** 3
**Commit:** Deferred — commit all Phase 2 reports together after review: `audit(CA): Phase 2 SP fan-out reports (16 SPs)`
**Risk:** HIGH. This is the most expensive and complex unit. Mitigation:
- `--dry-run` mode in CA-U07 lets you test the orchestration without sandbox launches
- Any sandbox crash drops that SP rather than aborting the run
- Cost is ~$12/run; confirm budget before executing
- Damage-control hook block during coder write inside sandbox = STOP and ask user (per `feedback_damage_control_self_unlock.md`)

---

### CA-U11 — Build `sfa_exception_ledger_auditor.py` (P3-A1)

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_exception_ledger_auditor.py`

**Pattern reference:**
`/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_bash_editor_agent_anthropic_v3.py` lines 1-9 — shebang + inline dep block.

`/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_codebase_context_agent_v3.py` lines 67-134 — `git_list_files` subprocess + file-existence checking pattern (the `check_file_paths_line_length` function at lines 137-177 shows the per-file iteration structure to reuse for per-exception path checking).

**Implementation sketch:**
```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["anthropic>=0.47.1", "rich>=13.7.0"]
# ///

# CLI: --exceptions audits/exceptions.md --repo-root /Users/robertrhu/Projects/arhugula
#      --output audits/phase3-exception-ledger-<date>.md

# Logic (no Anthropic calls needed for this SFA — pure mechanical check):
# 1. Parse exceptions.md:
#    - Split on "## Exception N" headers
#    - For each exception, extract Path(s): lines
#    - For each path: check if it exists in git (git ls-files --error-unmatch <path>)
# 2. Emit table: Exception | Path | Status (PRESENT|STALE|SKIP-wildcard)
# 3. STALE entries = flagged for human review (not auto-deleted)
# 4. Also check: every "## Exception N" has Status field
#    and cross-references a valid SP audit round
# 5. Write output to --output path
# 6. Exit 0 if zero STALE; exit 1 otherwise

# No Anthropic calls — use subprocess + file I/O only
# Dependencies: only rich (for output formatting)
```

**Test spec:**
- `uv run sfa_exception_ledger_auditor.py --help` exits 0
- Against the live `audits/exceptions.md`, produces a table with 29 exceptions
- A deliberately stale path (pointing to a file deleted from git) produces exit 1
- Wildcard paths (e.g., `audits/sp2_verify.py`) handled gracefully (SKIP-wildcard or glob-check)

**Validation:**
```bash
uv run /Users/robertrhu/Projects/arhugula/agents/sfa/sfa_exception_ledger_auditor.py --help
# Must show --exceptions, --repo-root, --output
```

**Wave:** 1 (Group C)
**Commit:** Batched with CA-U12/CA-U13/CA-U14: `build(CA-U11-U14): Phase 3 infra — 4 cross-cutting SFAs`
**Risk:** Low. Read-only file check. New file, no modifications.

---

### CA-U12 — Build `sfa_hook_coverage_matrix.py` (P3-A2)

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_hook_coverage_matrix.py`

**Pattern reference:**
`/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_codebase_context_agent_v3.py` lines 67-134 — `git_list_files` + file parsing loops.

The check is described in spec §6 check #2 (Exception 29 S-03 pattern: `fork subagent Bash outside damage-control`).

**Implementation sketch:**
```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["anthropic>=0.47.1", "rich>=13.7.0"]
# ///

# CLI: --agents .claude/agents/ --settings .claude/settings.json
#      --output audits/phase3-hook-matrix-<date>.md

# Logic:
# 1. Read .claude/settings.json → extract PreToolUse/PostToolUse hooks
#    and their matcher patterns
# 2. Walk .claude/agents/*.md + .claude/agents/team/*.md
#    For each agent: extract tools: list from frontmatter
# 3. Build matrix: Agent | Tools listed | Hooks that cover each tool
# 4. Flag any agent that has Bash in tools: but no Bash damage-control PreToolUse
#    coverage → "UNCOVERED BASH: [agent-name]"
# 5. Flag any agent that can Write/Edit without the write/edit damage-control hooks
# 6. Emit matrix as markdown table + findings list
# 7. Exit 0 if zero UNCOVERED findings; exit 1 otherwise

# Uses yaml.safe_load for frontmatter parsing (add pyyaml to deps if needed)
```

**Test spec:**
- For the existing `sandbox-validator-agent.md` (which has `disallowedTools: Bash`), no UNCOVERED BASH flag
- For a hypothetical agent with `tools: Bash` and no matching PreToolUse hook registered in `settings.json`, emits UNCOVERED
- Known gap: `@sandbox-validator-agent` inside E2B (SP15 Exception 29 S-03) should appear as a flagged pattern

**Validation:**
```bash
uv run /Users/robertrhu/Projects/arhugula/agents/sfa/sfa_hook_coverage_matrix.py --help
```

**Wave:** 1 (Group C)
**Commit:** Batched with CA-U11/CA-U13/CA-U14
**Risk:** Low. Read-only. New file.

---

### CA-U13 — Build `sfa_namespace_collision_detector.py` (P3-A3)

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_namespace_collision_detector.py`

**Pattern reference:**
`/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_codebase_context_agent_v3.py` lines 67-134 — file walking pattern.

The check is described in spec §6 check #3 (Exception 23 prime.md 4-way collision pattern).

**Implementation sketch:**
```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["rich>=13.7.0"]
# ///

# CLI: --claude-dir .claude/ --output audits/phase3-namespace-<date>.md

# Logic (no Anthropic calls — pure filename/frontmatter scan):
# 1. Walk .claude/commands/*.md → collect name (basename without .md)
#    Also extract "name:" frontmatter if present
# 2. Walk .claude/agents/*.md + .claude/agents/team/*.md → collect "name:" from frontmatter
# 3. Walk .claude/skills/*/ → collect skill dir names
# 4. Walk ~/.claude/skills/library/ (global) → collect skill names from library.yaml
# 5. Build cross-namespace collision map:
#    commands × agents, commands × skills, agents × skills, local × global
# 6. For each collision: emit: Namespace1 | Namespace2 | Name | Files
# 7. Known exception: prime.md collision (Exception 23) — pre-annotate it as KNOWN
# 8. Exit 1 if any UNKNOWN collisions found; exit 0 otherwise
```

**Test spec:**
- The known `prime.md` collision (Exception 23) appears in output but marked KNOWN
- Any new collision (if one was introduced) appears as UNKNOWN and triggers exit 1
- `--help` exits 0

**Validation:**
```bash
uv run /Users/robertrhu/Projects/arhugula/agents/sfa/sfa_namespace_collision_detector.py --help
# After Phase 3 execution:
grep "UNKNOWN" /Users/robertrhu/Projects/arhugula/audits/phase3-namespace-2026-04-14.md
# Expected: 0 lines (all collisions are known/excepted)
```

**Wave:** 1 (Group C)
**Commit:** Batched with CA-U11/CA-U12/CA-U14
**Risk:** Low. New file, read-only logic.

---

### CA-U14 — Build `sfa_sot_consistency_checker.py` (P3-A4)

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_sot_consistency_checker.py`

**Pattern reference:**
`/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_codebase_context_agent_v3.py` lines 180-307 — structured Anthropic API call with JSON output schema; this is the one SFA in Group C that benefits from an LLM call because it needs to parse free-text SoT sections and cross-reference counts.

**Implementation sketch:**
```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["anthropic>=0.47.1", "rich>=13.7.0"]
# ///

# CLI: --sot ~/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md
#      --memory ~/.claude/projects/.../memory/MEMORY.md
#      --output audits/phase3-sot-check-<date>.md

# Logic:
# 1. Read SoT §1 (current build status) → extract SP count + status markers
# 2. Read SoT §4 (per-SP feature inventory) → extract feature count per SP
# 3. Read SoT §8 (priority order) → verify SP ordering matches §1
# 4. Read SoT §11 (if present) → cross-check any numeric assertions
# 5. Read MEMORY.md → extract SP round markers (BUILT + AUDIT R1 COMPLETE)
# 6. Cross-reference: §1 SP status vs MEMORY.md SP entries
# 7. Flag mismatches: e.g., §1 says BUILT but no MEMORY.md entry; or §4 feature
#    count doesn't match §1 feature count for same SP
# 8. Use Anthropic API only for the parsing step (structured JSON extraction)
#    from the free-text SoT sections — minimizes cost
# 9. Emit: table of SP | SoT §1 status | MEMORY.md entry | §4 count | Match?
```

**Test spec:**
- All 16 SPs appear in the output table
- Any count mismatch (e.g., SoT §1 says SP12 has 14 features but §4 lists 15) appears as MISMATCH
- Known state: all 16 SPs should show BUILT + AUDIT R1 COMPLETE (based on current MEMORY.md)

**Validation:**
```bash
uv run /Users/robertrhu/Projects/arhugula/agents/sfa/sfa_sot_consistency_checker.py --help
# After Phase 3 execution:
grep "MISMATCH" /Users/robertrhu/Projects/arhugula/audits/phase3-sot-check-2026-04-14.md
# Expected: 0 lines
```

**Wave:** 1 (Group C)
**Commit:** Batched with CA-U11/CA-U12/CA-U13
**Risk:** Low. New file. Makes Anthropic API calls but at low volume (parsing only, not generative).

---

### CA-U15 — Execute Phase 3 — cross-cutting checks

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/audits/phase3-cross-cutting-2026-04-14.md`
- Create: `/Users/robertrhu/Projects/arhugula/audits/phase3-exception-ledger-2026-04-14.md` (from CA-U11)
- Create: `/Users/robertrhu/Projects/arhugula/audits/phase3-hook-matrix-2026-04-14.md` (from CA-U12)
- Create: `/Users/robertrhu/Projects/arhugula/audits/phase3-namespace-2026-04-14.md` (from CA-U13)
- Create: `/Users/robertrhu/Projects/arhugula/audits/phase3-sot-check-2026-04-14.md` (from CA-U14)

**Pattern reference:**
Execution unit. Can run in parallel with CA-U10 (in a second terminal). Spec §6 defines the 6 checks; checks 5 and 6 are grep-based sub-steps.

**Implementation sketch:**
```
1. Run the 4 SFAs sequentially (or in parallel with xargs):
   just phase3-cross-cutting
   which internally runs:
     uv run agents/sfa/sfa_exception_ledger_auditor.py \
       --exceptions audits/exceptions.md --repo-root . \
       --output audits/phase3-exception-ledger-2026-04-14.md
     uv run agents/sfa/sfa_hook_coverage_matrix.py \
       --agents .claude/agents/ --settings .claude/settings.json \
       --output audits/phase3-hook-matrix-2026-04-14.md
     uv run agents/sfa/sfa_namespace_collision_detector.py \
       --claude-dir .claude/ --output audits/phase3-namespace-2026-04-14.md
     uv run agents/sfa/sfa_sot_consistency_checker.py \
       --sot ~/Projects/indydevdan-harness-research/.../arhugula-source-of-truth.md \
       --output audits/phase3-sot-check-2026-04-14.md

2. Grep-based sub-steps (spec §6 checks 5 + 6):
   # Check 5: MEMORY.md ↔ memory files ↔ code
   grep -rn "project_" ~/.claude/projects/.../memory/MEMORY.md | \
     while read line; do
       f=$(echo $line | grep -oP 'project_\S+\.md')
       ls ~/.claude/projects/.../memory/$f || echo "STALE: $f"
     done

   # Check 6: runtime-blocker ledger ↔ exceptions.md [S]-tags
   grep "\[S\]" ~/.claude/projects/.../memory/project_runtime_blockers_ledger.md | \
     while read entry; do
       # verify a corresponding exception covers it
     done

3. Aggregate all outputs into phase3-cross-cutting-2026-04-14.md (consolidated report)
```

**Test spec:**
- All 5 per-check output files exist
- Consolidated report references all 6 checks by number
- Zero STALE exceptions (or any STALE listed as findings)
- Zero UNCOVERED agents (or any UNCOVERED listed as findings)
- KNOWN namespace collisions annotated (Exception 23 prime.md)

**Validation:**
```bash
ls /Users/robertrhu/Projects/arhugula/audits/phase3-*-2026-04-14.md
# Expected: 5 files (1 per SFA + 1 consolidated)
grep -c "STALE\|UNCOVERED\|MISMATCH\|UNKNOWN" /Users/robertrhu/Projects/arhugula/audits/phase3-cross-cutting-2026-04-14.md
# Green: 0 (all checks pass)
```

**Wave:** 3 (parallel with CA-U10)
**Commit:** Deferred — commit together with Phase 2 reports: `audit(CA): Phase 3 cross-cutting check reports`
**Risk:** Low. Read-only execution.

---

### CA-U16 — Build `@cross-model-consensus-agent` subagent (P4-A1)

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/.claude/agents/cross-model-consensus-agent.md`

**Pattern reference:**
`/Users/robertrhu/Projects/arhugula/.claude/agents/meta-agent.md` lines 1-7 — frontmatter (`name`, `description`, `tools`, `model`, `color`).

`/Users/robertrhu/Projects/arhugula/.claude/agents/meta-agent.md` lines 10-59 — multi-tool orchestration structure with numbered steps and output format.

SP4 just-prompt MCP server invocation is described in SoT §4.4. The Phase 4 workflow is in spec §7.

**Implementation sketch:**
```markdown
---
name: cross-model-consensus-agent
description: >
  Multi-model consensus reviewer for borderline Phase 2 audit findings.
  Use ONLY during Phase 4 of the comprehensive audit. Fan-outs a structured
  prompt to anthropic:claude-opus-4-6, openai:gpt-5, and google:gemini-2.5-pro
  via just-prompt. Applies reconciliation rules (unanimous/majority/3-way).
tools: Bash, Read
model: sonnet
color: cyan
---

# Purpose
Fan-out borderline audit findings to 3 models and reconcile verdicts.

## Workflow
1. Read the borderline finding bundle from context (passed as <borderline-findings>)
2. For each finding: invoke just-prompt with model fan-out:
   uv run just-prompt \
     --models "anthropic:claude-opus-4-6 openai:gpt-5 google:gemini-2.5-pro" \
     --prompt "<finding-prompt>"
3. Parse each model's verdict: {"severity": "P0..P3", "action": "lock|revisit|escalate"}
4. Apply reconciliation rules:
   - Unanimous agree → lock verdict + severity
   - 2-of-3 agree → adopt majority, note dissent in report
   - 3-way disagree on P0 → escalate to human immediately
5. Emit: audits/phase4-consensus-<date>.md with each finding's locked verdict

## Output format
For each reconciled finding:
| Finding ID | Coder verdict | Validator verdict | Model A | Model B | Model C | Final | Action |
```

**Test spec:**
- `grep "name: cross-model-consensus-agent"` present in frontmatter
- Yaml parses without error
- Reconciliation rules all 3 branches are documented in system prompt

**Validation:**
```bash
python3 -c "import yaml; yaml.safe_load(open('/Users/robertrhu/Projects/arhugula/.claude/agents/cross-model-consensus-agent.md').read().split('---')[1])"
grep "3-way disagree" /Users/robertrhu/Projects/arhugula/.claude/agents/cross-model-consensus-agent.md
```

**Wave:** 1 (Group D, independent)
**Commit:** Batched with Phase 2 infra: `build(CA-U16): Phase 4 infra — cross-model consensus agent`
**Risk:** Low. New file. Model routing uses existing just-prompt from SP4.

---

### CA-U17 — Execute Phase 4 — multi-model consensus on borderline findings

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/audits/phase4-consensus-2026-04-14.md`

**Pattern reference:**
Execution unit. CA-U16 is the subagent. Phase 2 mailbox `audits/phase2-mailbox.jsonl` provides the input (entries with `"verdict": "escalate"`).

**Implementation sketch:**
```
1. Check phase2-mailbox.jsonl for "escalate" entries:
   grep '"verdict": "escalate"' audits/phase2-mailbox.jsonl
   If zero: Phase 4 is a no-op (record "Phase 4: no borderline findings" in report)
   If nonzero: proceed with multi-model consensus for each

2. For each escalated finding:
   - Extract finding bundle (SP, evidence, coder verdict, validator verdict)
   - Invoke @cross-model-consensus-agent with the bundle as context
   - Agent fans out to 3 models via just-prompt
   - Reconcile per the rules

3. Write phase4-consensus-2026-04-14.md:
   - Per-finding verdict table
   - Any remaining 3-way disagreements listed as "requires user decision"
   - Total: N findings locked, M escalated to human

4. If 3-way disagreement on a P0 finding: STOP, surface to user before continuing
```

**Test spec:**
- Phase 4 report exists
- Every "escalate" entry from Phase 2 mailbox has a corresponding row in Phase 4 report
- No 3-way P0 disagreements left open (if any exist, user must decide before Phase 5)

**Validation:**
```bash
ls /Users/robertrhu/Projects/arhugula/audits/phase4-consensus-2026-04-14.md
grep "requires user decision" /Users/robertrhu/Projects/arhugula/audits/phase4-consensus-2026-04-14.md
# If nonzero: pause for user decision before proceeding to CA-U18
```

**Wave:** 4
**Commit:** Deferred — commit with Phase 5 tail: `audit(CA): Phases 4-5 reports + exception drafts`
**Risk:** Medium. Depends on 3 API keys (Blocker 3). If APIs fail: degrade to single-model mode, document in report.

---

### CA-U18 — Execute Phase 5 — `@builder` aggregates all phase outputs

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/audits/comprehensive-review-2026-04-14.md`

**Pattern reference:**
The `@builder` subagent (already exists). The Phase 5 workflow is described in spec §8. The output format mirrors the existing audit report format visible in `audits/exceptions.md` — structured headings, verdict tables, action items.

**Implementation sketch:**
```
@builder reads all prior phase outputs and produces the consolidated report.
Context to pass:
  - audits/phase0-skill-matches-2026-04-14.md
  - audits/phase1-byte-parity-2026-04-14.md
  - audits/phase2-sp*-review-2026-04-14.md (16 files)
  - audits/phase2-summary-2026-04-14.md
  - audits/phase3-cross-cutting-2026-04-14.md
  - audits/phase4-consensus-2026-04-14.md (if exists)

Output structure for comprehensive-review-2026-04-14.md:
## Executive Summary
- Identicality axis: PASS/FAIL
- Code review axis: PASS/FAIL + P0 count
- QA axis: PASS/FAIL

## Per-SP Verdict Table
| SP | Identicality | Code Review | QA | Verdict |

## Aggregated Findings by Priority
### P0 Findings (blocking)
### P1 Findings (documented exceptions)
### P2/P3 Findings (advisory)

## Proposed New Exceptions (numbered 30+)

## Recommended Action Items
```

**Test spec:**
- File exists and is non-empty
- Contains "Executive Summary" section
- Per-SP table has 16 rows
- Each proposed exception is numbered sequentially from 30

**Validation:**
```bash
ls /Users/robertrhu/Projects/arhugula/audits/comprehensive-review-2026-04-14.md
grep "## Per-SP Verdict" /Users/robertrhu/Projects/arhugula/audits/comprehensive-review-2026-04-14.md
wc -l /Users/robertrhu/Projects/arhugula/audits/comprehensive-review-2026-04-14.md
# Expected: > 100 lines
```

**Wave:** 5
**Commit:** Batched with CA-U19/CA-U20: `audit(CA): Phase 5 comprehensive review + exception drafts + memory update`
**Risk:** Medium. Depends on all prior phases completing. If a phase was skipped or degraded, the report must note it.

---

### CA-U19 — Draft proposed Exception 30+ entries (staged, NOT auto-committed)

**Artifacts:**
- Create: `/Users/robertrhu/Projects/arhugula/audits/phase5-proposed-exceptions-2026-04-14.md`

**Pattern reference:**
`/Users/robertrhu/Projects/arhugula/audits/exceptions.md` Exception 29 (lines 1593-1678) — the full exception format. Required fields: Path(s), SP audit round, Decision date, Status, Rationale, Findings, Runtime activation checklist (if security-posture), Sibling exceptions, Review cadence, Related findings, Follow-up actions.

**Implementation sketch:**
```
For each new finding in the comprehensive review that is NOT covered by existing
exceptions 1-29:

1. Assign sequential number (30, 31, ...) based on finding priority (P0 first)
2. Draft using Exception 29 as the template:
   ## Exception N — [Short title]
   **Path(s):** [files affected]
   **SP audit round:** Comprehensive audit round 1 (2026-04-14)
   **Decision date:** [PENDING USER APPROVAL — staged draft]
   **Status:** DRAFT — awaiting user decision
   **Rationale:** [why this exception is needed vs. fixing the drift]
   **Findings:** [evidence from Phase 2/3/4 reports]
   **Runtime activation checklist:** [if security-posture finding]
   **Review cadence:** [next review trigger]
   **Related findings:** [Phase report refs]
   **Follow-up actions:** [what happens after approval]

3. Write ALL drafts to phase5-proposed-exceptions-2026-04-14.md
4. Do NOT append to audits/exceptions.md — that is the user's decision

STAGED means: the file is written and git-tracked, but the user
must explicitly approve each entry and append it to exceptions.md.
```

**Test spec:**
- File exists and contains at least one "## Exception 30" header (or "No new exceptions proposed" if everything is clean)
- Every draft entry has Status: DRAFT
- No entry is auto-appended to `audits/exceptions.md`

**Validation:**
```bash
ls /Users/robertrhu/Projects/arhugula/audits/phase5-proposed-exceptions-2026-04-14.md
grep "DRAFT" /Users/robertrhu/Projects/arhugula/audits/phase5-proposed-exceptions-2026-04-14.md
# All entries must be DRAFT; none of them appear in exceptions.md yet
grep "Exception 30" /Users/robertrhu/Projects/arhugula/audits/exceptions.md
# Expected: 0 lines (not auto-committed)
```

**Wave:** 5
**Commit:** Batched with CA-U18/CA-U20 — staged drafts are committed to git for reference
**Risk:** Medium. User decision gate before any entry lands in `exceptions.md`.

---

### CA-U20 — Update `MEMORY.md` + `project_runtime_blockers_ledger.md`

**Artifacts:**
- Modify: `/Users/robertrhu/.claude/projects/-Users-robertrhu-Projects-arhugula/memory/MEMORY.md`
- Modify: `/Users/robertrhu/.claude/projects/-Users-robertrhu-Projects-arhugula/memory/project_runtime_blockers_ledger.md`

**Pattern reference:**
The existing MEMORY.md entry format is visible in the `<system-reminder>` context. Each entry is a `- [Link title](memory_file.md) — One-sentence description` bullet.

**Implementation sketch:**
```
1. Append to MEMORY.md:
   - [Comprehensive Audit r1 COMPLETE](project_comprehensive_audit_r1.md) — All 5 phases
     executed; N P0 findings, M proposed exceptions (30+). Report at
     audits/comprehensive-review-2026-04-14.md.

2. Create the corresponding memory file:
   ~/.claude/projects/.../memory/project_comprehensive_audit_r1.md
   with: phases run, findings summary, exception proposal status

3. If Phase 2 or Phase 3 surfaced new [S]-tagged items (security-posture blockers):
   Append to project_runtime_blockers_ledger.md with format:
   ## New runtime blocker: [description]
   - Exception: N (if proposed; otherwise "DRAFT — pending")
   - Activation condition: [what env var / action triggers it]
   - Current status: DORMANT

4. Update the "Next work" line in MEMORY.md to reflect post-audit state:
   "Next: user decision on Exception 30+ drafts; post-audit cleanup (Exception 14
   pathExclusions revert); or SP r2 rounds if findings require it."
```

**Test spec:**
- `grep "Comprehensive Audit" ~/.claude/projects/.../memory/MEMORY.md` returns 1 line
- `project_comprehensive_audit_r1.md` exists and is non-empty
- Any new [S]-tagged blocker appears in `project_runtime_blockers_ledger.md`

**Validation:**
```bash
grep "Comprehensive Audit" /Users/robertrhu/.claude/projects/-Users-robertrhu-Projects-arhugula/memory/MEMORY.md
ls /Users/robertrhu/.claude/projects/-Users-robertrhu-Projects-arhugula/memory/project_comprehensive_audit_r1.md
```

**Wave:** 5
**Commit:** Batched with CA-U18/CA-U19
**Risk:** Low. Additive memory updates.

---

### CA-U21 — Verify Pi binary + 6 extensions (Option A precondition)

**(Option A only — skip if using Option B)**

**Artifacts:**
- None (verification unit)

**Pattern reference:**
SP12 Pi integration. Justfile Pi block at lines 192-235.

**Implementation sketch:**
```
1. pi --version → capture version string
2. For each extension in list:
   ext-agent-chain, ext-purpose-gate, ext-agent-team,
   ext-subagent-widget, ext-drive-dispatch, ext-tool-counter-widget
   pi -e extensions/<name>.ts --dry-run → verify loadable
3. If any extension fails to load: document as "Option A degraded"
4. Pi binary absent → Option A not viable; recommend Option B
```

**Test spec:**
- All 6 extensions load without error
- `pi --version` output captured in pre-run notes

**Validation:**
```bash
pi --version
pi -e extensions/ext-agent-chain.ts --dry-run 2>&1 | head -3
```

**Wave:** 1 (Group F, independent from other groups)
**Commit:** Not committed (verification only)
**Risk:** Low. Non-destructive.

---

### CA-U22 — Wire Pi orchestration recipes for the 5 phases (Option A only)

**(Option A only — skip if using Option B)**

**Artifacts:**
- Modify: `/Users/robertrhu/Projects/arhugula/justfile`

**Pattern reference:**
`/Users/robertrhu/Projects/arhugula/justfile` lines 192-280 (SP12 Pi block) — pattern for Pi extension chaining recipes (`pi -e extensions/X.ts -e extensions/Y.ts`).

**Implementation sketch:**
```
Add new block after the existing === Comprehensive Audit Infrastructure === block:

# === Comprehensive Audit — Option A Pi Orchestration ===
# Requires Pi binary + 6 extensions (CA-U21 verify).

# Phase 1 with Pi progress widget
audit-phase-1:
    pi -e extensions/ext-tool-counter-widget.ts -- just phase1-byte-diff

# Phase 2 with Pi agent-team grid (16-cell dashboard)
audit-phase-2:
    pi -e extensions/ext-agent-team.ts \
       -e extensions/ext-subagent-widget.ts \
       -e extensions/ext-drive-dispatch.ts \
       -- bash scripts/phase2_sp_fanout.sh

# Phase 3 with Pi purpose-gate + tool-counter
audit-phase-3:
    pi -e extensions/ext-purpose-gate.ts \
       -e extensions/ext-tool-counter-widget.ts \
       -- just phase3-cross-cutting

# Phases 4 + 5 (agent-chain gating)
audit-phase-4-5:
    pi -e extensions/ext-agent-chain.ts -- claude "/cross-model-consensus-agent"
```

**Test spec:**
- `just --list | grep audit-phase` returns 4 recipes
- `just audit-phase-1 --dry-run` (if Pi supports it) exits 0

**Validation:**
```bash
cd /Users/robertrhu/Projects/arhugula && just --list | grep audit-phase
```

**Wave:** 1 (Group F, after CA-U21)
**Commit:** Batched with CA-U21 if Option A is chosen: `build(CA-U21-U22): Option A Pi orchestration recipes`
**Risk:** Medium. Modifies justfile. Skip entirely for Option B.

---

## Verification matrix

| Unit | Verification command |
|------|----------------------|
| CA-U01 | `ls audits/phase0-skill-matches-2026-04-14.md` |
| CA-U02 | `uv run agents/sfa/sfa_byte_diff_audit.py --help` |
| CA-U03 | `just --list \| grep phase1-byte-diff` |
| CA-U04 | `grep "UNEXPLAINED" audits/phase1-byte-parity-2026-04-14.md \| wc -l` → expect 0 |
| CA-U05 | `python3 -c "import yaml; yaml.safe_load(open('.claude/agents/sandbox-validator-agent.md').read().split('---')[1])"` |
| CA-U06 | `uv run agents/sfa/sfa_coder_validator_loop.py --help` |
| CA-U07 | `bash scripts/phase2_sp_fanout.sh --help` |
| CA-U08 | `echo "OpenAI: $([ -n "$OPENAI_API_KEY" ] && echo YES || echo NO)"` |
| CA-U09 | `just sbx --help 2>&1 \| head -3` |
| CA-U10 | `ls audits/phase2-sp*-review-2026-04-14.md \| wc -l` → expect 16 |
| CA-U11 | `uv run agents/sfa/sfa_exception_ledger_auditor.py --help` |
| CA-U12 | `uv run agents/sfa/sfa_hook_coverage_matrix.py --help` |
| CA-U13 | `uv run agents/sfa/sfa_namespace_collision_detector.py --help` |
| CA-U14 | `uv run agents/sfa/sfa_sot_consistency_checker.py --help` |
| CA-U15 | `ls audits/phase3-*-2026-04-14.md \| wc -l` → expect 5 |
| CA-U16 | `grep "name: cross-model-consensus-agent" .claude/agents/cross-model-consensus-agent.md` |
| CA-U17 | `ls audits/phase4-consensus-2026-04-14.md` |
| CA-U18 | `wc -l audits/comprehensive-review-2026-04-14.md` → expect > 100 |
| CA-U19 | `grep "DRAFT" audits/phase5-proposed-exceptions-2026-04-14.md \| wc -l` → ≥ 1 |
| CA-U20 | `grep "Comprehensive Audit" ~/.claude/projects/.../memory/MEMORY.md` |
| CA-U21 | `pi --version` (Option A only) |
| CA-U22 | `just --list \| grep audit-phase` → 4 recipes (Option A only) |

---

## Decision points

1. **Before CA-U01 (now):** Choose Option A (Pi) or Option B (Claude Code native). Option B is the default — zero setup cost. Option A requires CA-U21 + CA-U22 and ~30 min Pi init. Document choice; it determines which Group F units are in scope.

2. **Before CA-U06 (Blocker 3):** Confirm which non-Anthropic API keys are available. Minimum: 1 key (OpenAI OR Google) for Phase 2 validator model diversity. 2 keys required for Phase 4 3-model consensus. If 0 non-Anthropic keys: Phase 2 validator cannot enforce different-model constraint; Phase 4 runs single-model. This is a documented degradation, not a blocker.

3. **Before CA-U10 (Blocker 1 + 2):** User must explicitly acknowledge all of:
   - Exception 29 dormant findings will become active when `E2B_API_KEY` is exported to env
   - Exception 14 / 24 / 28 runtime activation notes reviewed
   - Phase 2 cost budget (~$12 per full run) confirmed
   This is a hard gate. Do not proceed to CA-U10 without confirmation.

4. **After CA-U17:** If any 3-way P0 disagreement surfaced in Phase 4: pause and present findings to user before proceeding to CA-U18. Each 3-way P0 requires an explicit decision (accept one model's verdict, or treat as an Exception 30+ draft).

5. **After CA-U19:** For each proposed Exception 30+ draft: user decides accept (append to `audits/exceptions.md`) or reject (close the finding without exception). This is the only gate where files outside the audit subdirectory are modified.

6. **Post CA-U20 (separate decision):** The Exception 14 Category J pathExclusions revert (per `feedback_audit_pathexclusions_temporary.md`): after the comprehensive audit confirms all SP identicality work is complete, the 6 `pathExclusions` entries in `patterns.yaml` must be reverted. This is a separate PR from the audit infrastructure itself.

---

## Blocker resolution plan

**Blocker 1 — Exception 29 activation acknowledgment:**
Resolution: Implement the pre-condition gate in `phase2_sp_fanout.sh` (CA-U07). The script checks for `E2B_API_KEY` and prints the activation checklist before launching any sandbox. The script exits with a prompt asking for user `--ack-exception-29` flag. Without this flag, the script refuses to run. Builder implements this as a `--ack-exceptions "29,14,24,28"` CLI flag. User passes it explicitly. The flag itself is the acknowledgment; no separate document needed.

**Blocker 2 — Phase 2 cost budget:**
Resolution: `phase2_sp_fanout.sh` prints an estimated cost line before launching (`Estimated cost: ~$12.00 based on 16 sandboxes × 15 min × $0.05/min. Continue? [y/N]`). The interactive prompt is the budget confirmation gate. For headless runs, a `--confirm-cost` flag bypasses the interactive prompt. The builder wires this into CA-U07.

**Blocker 3 — just-prompt multi-model API availability:**
Resolution: CA-U08 documents the available models. CA-U06 enforces that `--validator-model` != `--coder-model`. If zero non-Anthropic keys: the SFA prints "WARNING: degraded mode — validator will use [model] which is also the coder model; Phase 2 independence constraint CANNOT be met." The run proceeds but the degradation is logged into every Phase 2 report as a finding header. Phase 4 similarly degrades to 1-model mode if only 1 non-Anthropic key available, with the report noting the degradation.

**Blocker 4 — Orchestration decision (A vs B):**
Resolution: Default to Option B (Claude Code native). CA-U21 and CA-U22 are annotated "Option A only" throughout this plan. If the user decides to use Option A, execute CA-U21 first (Pi binary check), then CA-U22 (justfile wiring), before executing any phase. Option A and Option B produce identical output artifacts — the difference is only observability (grid dashboard vs flat terminal).

---

## Recommended first commit

Stage the following in the first build commit (`build(CA-U01-U03-U05): Phase 0 precheck + Phase 1 infra + Phase 2 validator subagent`):

1. `audits/phase0-skill-matches-2026-04-14.md` (CA-U01 output)
2. `agents/sfa/sfa_byte_diff_audit.py` (CA-U02)
3. `justfile` — new `=== Comprehensive Audit Infrastructure ===` block (CA-U03)
4. `.claude/agents/sandbox-validator-agent.md` (CA-U05)

Rationale: these 4 artifacts together establish the audit infrastructure shell and allow CA-U08/CA-U09 verification to proceed immediately. The remaining Phase 2 SFAs (CA-U06/CA-U07), Phase 3 SFAs (CA-U11–CA-U14), and Phase 4 subagent (CA-U16) can land in a second infra commit before any execution begins.