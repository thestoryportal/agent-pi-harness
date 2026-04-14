# ArhuGula Comprehensive Audit — Code Review + QA + Identicality

**Date:** 2026-04-14
**Branch:** `audit/identicality-2026-04-13` (or follow-up)
**Status:** SPEC — awaiting scout decomposition
**Supersedes:** SP1-r1..SP16-r1 per-SP audit rounds (linear; this is parallelized holistic)

## 0. Purpose

One-pass comprehensive review of the complete ArhuGula codebase across three axes:

1. **Identicality** — Tier 1 byte-parity vs upstream full-clones (mechanical)
2. **Code review** — subjective quality across all 16 SPs (subagent fan-out)
3. **QA** — functional correctness of runtime entry points (sandbox testing)

Output: `audits/comprehensive-review-<date>.md` + new Exception entries where warranted + updated `project_runtime_blockers_ledger.md`.

## 1. Scope

**In-scope:**
- All 16 SPs (SP1-SP16), all currently BUILT + AUDIT R1 COMPLETE
- `.claude/` tree (hooks, commands, agents, skills, settings)
- `apps/` (drive, listen, direct, observe, dropzone, prompt-testing, sandbox_*, voice)
- `agents/sfa/` (SP7 single-file agents)
- `justfile` (all SP blocks)
- `audits/exceptions.md` (1-29, consistency check)
- `MEMORY.md` + all memory files
- SoT cross-references (§1/§4/§8/§11)

**Out of scope:**
- Upstream full-clones (read-only reference)
- Research docs under `~/Projects/indydevdan-harness-research/`
- `~/.claude/skills/library/` global catalog (reviewed as reference only)
- Feature-level GAP work (no outstanding GAPs)
- Fixing findings (audit is read-only; fixes are follow-up)
- n8n or other external services (runtime boundary)

## 2. Mandate

- **Identicality**: every Tier 1 file must either (a) byte-match upstream or (b) have an active exception in `audits/exceptions.md`
- **Code review**: every SP must pass @validator + @sandbox-validator with zero P0 findings (P1+ documented as exceptions)
- **QA**: every justfile entry point with a no-credential smoke path must succeed; credentialed paths are dormancy-checked only
- **Consistency**: `audits/exceptions.md` ↔ live code ↔ memory ↔ SoT must all agree

## 3. Phase 0 — Skill Discovery (Precheck)

**Goal**: Avoid reinventing skills that already exist.

**Workflow**:
1. Run `/find-skills` against the global library catalog for each proposed new artifact
2. Keywords: `diff-analyzer`, `dead-code`, `drift-detector`, `ledger-auditor`, `hook-graph`, `namespace-collision`, `sot-consistency`, `byte-diff`, `exception-auditor`, `cross-model-consensus`
3. For every match, evaluate whether it can replace a new SFA/subagent
4. Emit `audits/phase0-skill-matches-<date>.md` with decisions

**Duration**: ~10 min
**Parallelism**: none
**Outputs**: match report + final artifact list (potentially reduced)

## 4. Phase 1 — Byte-Parity Sweep (Mechanical SFA)

**Goal**: Mechanical identicality confirmation. Every Tier 1 file byte-matches upstream OR has an active exception.

**Implementation**: new single-file agent `agents/sfa/sfa_byte_diff_audit.py` (artifact **P1-A1**)

**Workflow**:
1. Read the 3-tier clone map from SoT §1 (all 16 SPs → upstream full-clone paths)
2. For each SP, enumerate the ArhuGula paths that should be byte-identical
3. Run `diff -q <local> <upstream>` on every file (parallelizable via xargs)
4. Cross-reference every DRIFT against `audits/exceptions.md` (lookup by path)
5. Emit structured output: per-SP table with MATCH / DRIFT-explained / DRIFT-unexplained / MISSING counts
6. Write report to `audits/phase1-byte-parity-<date>.md`
7. Exit code 0 if no unexplained drift; exit 1 otherwise

**Inputs**:
- SoT §1 (SP → upstream mapping)
- `audits/exceptions.md` (active exception list)
- Full-clone tree at `~/Projects/indydevdan-harness-research/research/full-clones/`

**Outputs**:
- `audits/phase1-byte-parity-<date>.md`
- Unexplained drift list → becomes Phase 2 priority targets

**Duration**: ~10 min
**Parallelism**: xargs -P (native OS parallelism; no E2B needed)
**Pi role** (Option A): optional `ext-tool-counter-widget` for progress
**Claude Code role** (Option B): direct `just` recipe invocation

## 5. Phase 2 — SP-Level Fan-Out + Sandboxed Coder↔Validator Loop

**Goal**: Subjective code review + QA per SP, in parallel, with a coder↔validator iteration loop inside each sandbox.

**Implementation**: 16-parallel E2B sandboxes via SP15 `sbx-fork` (one SP per sandbox), each running a coder↔validator loop.

**Coder↔validator loop architecture**:

```
┌──────────────────────────────── E2B Sandbox ────────────────────────────────┐
│                                                                              │
│  ┌─── Coder Agent (Claude Opus via claude-agent-sdk) ───┐                    │
│  │    - Reads SP scope manifest                         │                    │
│  │    - Runs SP3 static pipeline (ruff/ty/mypy)         │                    │
│  │    - Runs no-credential smoke tests                  │                    │
│  │    - Generates review + proposed diffs (to /tmp)     │                    │
│  └──────────────────────────────┬──────────────────────┘                    │
│                                 │ submits findings + diffs                   │
│                                 ▼                                            │
│  ┌─── Sandbox Validator Agent (DIFFERENT model) ────────┐                    │
│  │    Model: GPT-5 or Gemini via SP4 just-prompt        │                    │
│  │    System prompt: @security adversarial variant      │                    │
│  │    Temperature: 0.1                                   │                    │
│  │    Runs:                                              │                    │
│  │      1. Static verification of coder findings         │                    │
│  │      2. Independent adversarial review pass           │                    │
│  │      3. Structured JSON verdict                       │                    │
│  └──────────────────────────────┬──────────────────────┘                    │
│                                 │                                            │
│             ┌───────── verdict: pass | fail | escalate ──────┐               │
│             │                                                │               │
│             ▼                                                ▼               │
│     verdict = pass                                 verdict = fail            │
│     OR iter_count = 3                               iter_count < 3           │
│             │                                                │               │
│             ▼                                                ▼               │
│     emit to mailbox                             return findings to coder    │
│     terminate sandbox                            coder refactors → resubmit │
│                                                          (loop)              │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Loop properties** (hard requirements):
- **Isolation**: sandbox gets read-only mount of the ArhuGula tree; coder writes diffs to `/tmp` inside sandbox, NEVER to main repo
- **Objectivity**: validator MUST use a different model than coder (enforced via just-prompt routing; e.g., coder=Claude Opus, validator=GPT-5 or Gemini)
- **Adversarial posture**: validator system prompt is the @security subagent variant, not a passive checker
- **Determinism**: both agents run at `temperature=0.1`, structured JSON output schemas
- **Iteration cap**: 3 coder↔validator cycles max; on cap, escalate to human with full loop transcript
- **Verdict schema**: `{"verdict": "pass|fail|escalate", "findings": [{"severity": "P0..P3", "file": "...", "line": N, "evidence": "...", "fix": "..."}], "iterations": N, "final_diff": "..."}`

**New artifacts**:
- **P2-A1** — `@sandbox-validator-agent` subagent definition at `.claude/agents/sandbox-validator-agent.md`. Adversarial validator with different-model constraint enforced in frontmatter + system prompt.
- **P2-A2** — `agents/sfa/sfa_coder_validator_loop.py`. Single-file agent that runs inside each sandbox; orchestrates the coder↔validator loop, handles iteration cap, emits to mailbox.
- **P2-A3** — `scripts/phase2_sp_fanout.sh`. Kicks off 16 `sbx-fork` invocations with per-SP context bundles (file manifest + memory file + SoT section + exceptions subset).

**Inputs**:
- Phase 1 output (unexplained drift list → priority targets)
- Per-SP memory files from `~/.claude/projects/.../memory/project_sp*_r1_resume.md`
- Per-SP section of SoT §4
- `audits/exceptions.md` full file

**Outputs**:
- 16× per-SP reports at `audits/phase2-sp<N>-review-<date>.md`
- Aggregate summary at `audits/phase2-summary-<date>.md`
- Shared mailbox file `audits/phase2-mailbox.jsonl` (structured events per sandbox)

**Duration**: ~1.5 hr (dominated by slowest sandbox, not sum)
**Parallelism**: 16 E2B sandboxes simultaneously
**Runtime cost**: ~16 sandboxes × ~15 min × ~$0.05/min = **~$12 per full run**

**Pi role** (Option A): `ext-agent-team` grid dashboard (one cell per SP), `ext-subagent-widget` per fork, `ext-drive-dispatch` routes work to `claude -p` subprocesses
**Claude Code role** (Option B): `sbx-fork` directly with flat terminal output

## 6. Phase 3 — Cross-Cutting Checks (Sequential)

**Goal**: Catch the things per-SP fan-out misses — holistic integrity.

**Checks** (one sequential session, read-only):

1. **Exception-ledger ↔ code drift** — every exception in `audits/exceptions.md` must have its `Path(s)` still present in git
   - Implementation: **P3-A1** — `sfa_exception_ledger_auditor.py`

2. **Hook coverage matrix** — for every subagent spawn point in `.claude/agents/*.md`, verify which project-level hooks (damage-control, patterns.yaml, permissions) actually cover the spawn. Catches the SP15 Exception 29 #3 pattern (fork subagent Bash outside damage-control).
   - Implementation: **P3-A2** — `sfa_hook_coverage_matrix.py`

3. **Cross-SP namespace collisions** — duplicate command/skill/agent names across `.claude/commands/`, `.claude/skills/`, `.claude/agents/`. Catches the Exception 23 pattern (4-way `prime.md` collision).
   - Implementation: **P3-A3** — `sfa_namespace_collision_detector.py`

4. **SoT §1/§4/§8/§11 consistency** — SP counts, feature counts, status markers must agree across all four sections.
   - Implementation: **P3-A4** — `sfa_sot_consistency_checker.py`

5. **MEMORY.md ↔ memory files ↔ code** — every memory file referenced in MEMORY.md exists; every claim in a memory file about code paths still holds.
   - Implementation: grep-based, may be a sub-step of P3-A1 or a separate SFA.

6. **Runtime-blocker ledger ↔ exceptions.md** — every exception tagged `[S]` in the runtime-blocker ledger must have a corresponding security-posture block in exceptions.md.
   - Implementation: grep-based, likely a sub-step.

**Inputs**:
- `audits/exceptions.md`
- All memory files
- `MEMORY.md`
- SoT full file
- Full .claude/ tree

**Outputs**:
- `audits/phase3-cross-cutting-<date>.md`

**Duration**: ~30 min
**Parallelism**: none (holistic by design)
**Pi role** (Option A): `ext-purpose-gate` (enforce cross-cut focus), `ext-tool-counter` (depth monitor)
**Claude Code role** (Option B): vanilla session with Grep/Read

## 7. Phase 4 — Multi-Model Consensus

**Goal**: Reconcile borderline findings from Phase 2 via cross-model review.

**Workflow**:
1. Phase 2 aggregator surfaces findings marked "borderline" (validator + security disagreed, or coder↔validator loop hit iteration cap)
2. Bundle each borderline finding into a structured prompt
3. Invoke SP4 `just-prompt` with model fan-out: `anthropic:claude-opus-4-6 openai:gpt-5 google:gemini-2.5-pro`
4. Parse each model's verdict (agree / disagree / refine)
5. Reconciliation rules:
   - **Unanimous agree** → lock severity + priority, no further action
   - **2-of-3 agree** → adopt majority verdict, note dissent
   - **3-way disagreement** → escalate to human with all three opinions
6. Emit reconciled verdicts to `audits/phase4-consensus-<date>.md`

**New artifacts**:
- **P4-A1** — `@cross-model-consensus-agent` subagent wrapping just-prompt

**Codex escalation path** (held in reserve): if Phase 4 surfaces systematic blind spots that just-prompt's GPT-5 model doesn't catch, escalate to a parallel Codex CLI session with heavy priming (SP memory file + exceptions.md + full-clone path + task prompt).

**Inputs**:
- Phase 2 borderline findings
- `audits/exceptions.md` + SoT context per finding

**Outputs**:
- `audits/phase4-consensus-<date>.md`
- Updated Phase 2 finding set with locked priorities

**Duration**: ~15 min
**Parallelism**: implicit via just-prompt (models run in parallel)
**Pi role**: None (just-prompt runs as subprocess)

## 8. Phase 5 — Aggregate + Ledger Update

**Goal**: Single comprehensive report; propose new exceptions where needed.

**Workflow**:
1. `@builder` agent reads all prior phase outputs:
   - `audits/phase0-skill-matches-*.md`
   - `audits/phase1-byte-parity-*.md`
   - `audits/phase2-sp*-review-*.md` + summary
   - `audits/phase3-cross-cutting-*.md`
   - `audits/phase4-consensus-*.md`
2. Writes consolidated `audits/comprehensive-review-<date>.md`:
   - Executive summary (pass/fail per axis)
   - Per-SP verdict table
   - Aggregated findings by priority (P0/P1/P2/P3)
   - Proposed new exception entries (numbered Exception 30+)
   - Recommended action items
3. For each new finding not covered by an existing exception:
   - Propose Exception 30, 31, ... with full `audits/exceptions.md` format
   - Stage as draft in `audits/phase5-proposed-exceptions-<date>.md` (NOT auto-committed)
4. Update `MEMORY.md` index with phase output references
5. Update `project_runtime_blockers_ledger.md` if new runtime-gated findings

**Inputs**:
- All prior phase outputs

**Outputs**:
- `audits/comprehensive-review-<date>.md` (primary deliverable)
- `audits/phase5-proposed-exceptions-<date>.md` (draft exceptions, awaiting user decision)
- Updated `MEMORY.md`
- Updated runtime-blocker ledger

**Duration**: ~15 min
**Parallelism**: none
**Pi role** (Option A): `ext-agent-chain` gates Phase 5 after Phase 4 completes
**Claude Code role** (Option B): sequential `@builder` invocation

## 9. New Artifacts — Summary

**Single-file agents (5 new):**
| ID | Path | Phase | Purpose |
|---|---|---|---|
| P1-A1 | `agents/sfa/sfa_byte_diff_audit.py` | 1 | Byte-diff orchestrator |
| P2-A2 | `agents/sfa/sfa_coder_validator_loop.py` | 2 | Per-sandbox loop driver |
| P3-A1 | `agents/sfa/sfa_exception_ledger_auditor.py` | 3 | Stale exception detector |
| P3-A2 | `agents/sfa/sfa_hook_coverage_matrix.py` | 3 | Subagent hook inheritance check |
| P3-A3 | `agents/sfa/sfa_namespace_collision_detector.py` | 3 | Cross-SP collision check |
| P3-A4 | `agents/sfa/sfa_sot_consistency_checker.py` | 3 | SoT cross-reference check |

**Specialized subagents (3 new):**
| ID | Path | Phase | Purpose |
|---|---|---|---|
| P2-A1 | `.claude/agents/sandbox-validator-agent.md` | 2 | Adversarial validator for coder↔validator loop |
| P4-A1 | `.claude/agents/cross-model-consensus-agent.md` | 4 | just-prompt wrapper for multi-model review |
| P3-A5 | `.claude/agents/exception-auditor-agent.md` | 3 | Optional — may be subsumed by P3-A1 SFA |

**Shell scripts (1 new):**
- **P2-A3** — `scripts/phase2_sp_fanout.sh`: kicks off 16 sbx-fork invocations with per-SP context bundles

**Pre-existing dependencies (reused, not built):**
- `@validator`, `@security`, `@builder`, `@scout-agent`, `@architect` subagents
- SP4 `just-prompt` for multi-model routing
- SP15 `sbx-fork` for E2B parallelism
- SP9 `/infinite` for optional wave-based iteration
- SP5 `pocket-pick` for surfacing prior audit precedents
- SP3 validator pipeline (ruff/ty/mypy)
- SP14 `@bowser-qa-agent` for UI surfaces (if any)
- SP11 `promptfoo` for prompt-level assertions

## 10. Orchestration Options

Both options produce the same output artifacts. They differ in observability and setup cost.

### Option A — Pi Orchestrator (Recommended Default)

**Shell**: `just pi-full` (drive-dispatch + listen-submit + damage-control + theme-cycler)

**Phase-to-extension mapping**:

| Phase | Pi extension | Role |
|---|---|---|
| Outer | `ext-agent-chain` | Sequential phase gates (1→2→3→4→5) |
| Outer | `ext-purpose-gate` | Per-phase focus discipline |
| Phase 0 | (none needed) | /find-skills is a simple session call |
| Phase 1 | `ext-tool-counter-widget` (optional) | Progress widget for SFA |
| Phase 2 | `ext-agent-team` | **Load-bearing** — grid dashboard, one cell per SP fork |
| Phase 2 | `ext-subagent-widget` | Per-fork live streaming |
| Phase 2 | `ext-drive-dispatch` | Routes work to `claude -p` subprocesses |
| Phase 3 | `ext-purpose-gate` | Cross-cut focus enforcement |
| Phase 3 | `ext-tool-counter` | Investigation depth monitor |
| Phase 4 | (none) | just-prompt runs as subprocess |
| Phase 5 | `ext-agent-chain` | Gates Phase 5 after Phase 4 |

**Setup cost**: ~30 min (Pi init + extension wiring, if not already done)
**Observability**: full grid dashboard for Phase 2, live progress for Phase 3-5
**When to pick**: first comprehensive run, or whenever you want to watch 16 parallel SPs as a grid

### Option B — Claude Code Native (Simpler)

**Shell**: current Claude Code session

**Approach**:
- Phase 0: `/find-skills` invocation
- Phase 1: `just phase1-byte-diff` (calls `sfa_byte_diff_audit.py`)
- Phase 2: `scripts/phase2_sp_fanout.sh` → 16 sbx-fork calls directly; outputs to flat mailbox file
- Phase 3: single Claude Code session, sequential SFA calls
- Phase 4: `uv run just-prompt ...` subprocess
- Phase 5: `@builder` subagent invocation

**Setup cost**: ~0 min (everything already in place)
**Observability**: flat terminal logs per sandbox, no grid
**When to pick**: subsequent re-runs once methodology is proven, or when Pi setup cost isn't warranted

**Default**: Option A for the first run. Option B for subsequent passes.

## 11. Success Criteria

**Pass conditions (all must hold for LAND verdict):**
- Phase 1: zero unexplained byte drift across all Tier 1 files
- Phase 2: every SP passes validator with zero P0 findings; coder↔validator loops all resolve within 3 iterations
- Phase 3: all 6 cross-cutting checks green OR flagged with proposed new exceptions
- Phase 4: borderline findings reconciled (no 3-way model disagreements escalated to human)
- Phase 5: comprehensive report published, new exceptions drafted, MEMORY.md + ledger updated

**Fail conditions (any blocks landing):**
- Unexplained byte drift (Phase 1)
- P0 finding without a proposed mitigation or exception (Phase 2)
- Stale exception pointing at non-existent code (Phase 3)
- 3-way model disagreement on a P0 severity (Phase 4)

## 12. Dependencies

**Infrastructure**:
- **E2B credits + `E2B_API_KEY`** → **ACTIVATES EXCEPTION 29 DORMANT FINDINGS**. Running this audit formally exits dormancy for SP15 security posture.
- just-prompt with API keys for Anthropic, OpenAI, Google (SP4)
- Full-clone tree at `~/Projects/indydevdan-harness-research/research/full-clones/` (read-only)
- `uv` for SFA execution
- Pi binary installed + extensions wired (Option A only)

**Documentation prerequisites**:
- `audits/exceptions.md` current state (1-29)
- `project_runtime_blockers_ledger.md` current state
- SoT at `~/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md`

**Runtime activation acknowledgment**: by running this audit, the user formally reviews Exception 14 / 24 / 28 / 29 (all `[S]`-tagged). Must be confirmed before Phase 2 kickoff.

## 13. Risk Management

**Rollback**: all new artifacts are additive (new SFAs, new subagents, new audit reports). No code is patched during the audit. Phase 5 proposes exception drafts; these are staged, not auto-committed. User makes final landing decision.

**Abort conditions**:
- Any sandbox crash during Phase 2 → drop that SP, continue with remaining 15
- just-prompt API errors → Phase 4 runs in single-model degraded mode
- Phase 3 reveals a blocking structural issue → halt, report, await user decision
- Damage-control hook block during Phase 2 coder write → stop and ask user (per `feedback_damage_control_self_unlock.md`)

**Data loss**: none. All artifacts are written, not deleted. Full transcript per phase.

## 14. Definition of Done

- [ ] Phase 0: /find-skills matches evaluated, artifact list finalized
- [ ] Phase 1: byte-parity sweep report published, zero unexplained drift OR mapping proposed
- [ ] Phase 2: 16 SP reports + aggregate summary, all coder↔validator loops converged
- [ ] Phase 3: cross-cutting check report published, all 6 checks green or flagged
- [ ] Phase 4: borderline findings reconciled via multi-model consensus
- [ ] Phase 5: comprehensive review + draft exceptions + MEMORY.md + ledger updates
- [ ] User decision captured on each proposed Exception 30+
- [ ] Follow-up branch created if findings require code fixes (out of audit scope)
