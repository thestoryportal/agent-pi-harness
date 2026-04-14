# Comprehensive Audit — Scout Artifact

**Date:** 2026-04-14
**Spec:** `audits/comprehensive-audit-spec.md`
**Branch:** `audit/identicality-2026-04-13`
**Phase:** Scout (first step in Scout → Plan → Build pipeline)
**Target:** Forward-looking audit infrastructure (not a retrospective SP audit round)

---

## Summary

**Total units:** 22
**Critical path length:** 10 units
**Parallelizable build groups:** 2 (infra-build + dependency-verify)
**Blockers identified:** 4 (user acknowledgments + infra preconditions — listed in §Blockers)

## Unit list

### Phase 0 — Precheck

| ID | Title | Type | Risk |
|---|---|---|---|
| CA-U01 | Run `/find-skills` precheck + document matches | script | low |

### Phase 1 — Byte-parity sweep (infra + execution)

| ID | Title | Type | Risk |
|---|---|---|---|
| CA-U02 | Build `sfa_byte_diff_audit.py` (P1-A1) | script | low |
| CA-U03 | Add `just phase1-byte-diff` recipe | config | low |
| CA-U04 | Execute Phase 1 — byte-parity sweep | test | low |

### Phase 2 — SP-level fan-out + sandboxed coder↔validator loop

| ID | Title | Type | Risk |
|---|---|---|---|
| CA-U05 | Build `@sandbox-validator-agent` subagent (P2-A1) | agent | medium |
| CA-U06 | Build `sfa_coder_validator_loop.py` (P2-A2) | script | medium |
| CA-U07 | Build `scripts/phase2_sp_fanout.sh` (P2-A3) | script | medium |
| CA-U08 | Verify SP4 just-prompt multi-model routing (dependency check) | test | low |
| CA-U09 | Verify SP15 `sbx-fork` + E2B runtime (dependency check) | test | medium |
| CA-U10 | Execute Phase 2 — 16-parallel SP fan-out with coder↔validator loops | test | high |

### Phase 3 — Cross-cutting checks (infra + execution)

| ID | Title | Type | Risk |
|---|---|---|---|
| CA-U11 | Build `sfa_exception_ledger_auditor.py` (P3-A1) | script | low |
| CA-U12 | Build `sfa_hook_coverage_matrix.py` (P3-A2) | script | low |
| CA-U13 | Build `sfa_namespace_collision_detector.py` (P3-A3) | script | low |
| CA-U14 | Build `sfa_sot_consistency_checker.py` (P3-A4) | script | low |
| CA-U15 | Execute Phase 3 — cross-cutting checks | test | low |

### Phase 4 — Multi-model consensus

| ID | Title | Type | Risk |
|---|---|---|---|
| CA-U16 | Build `@cross-model-consensus-agent` subagent (P4-A1) | agent | low |
| CA-U17 | Execute Phase 4 — reconcile borderline findings | test | medium |

### Phase 5 — Aggregate + ledger update

| ID | Title | Type | Risk |
|---|---|---|---|
| CA-U18 | Execute Phase 5 — @builder aggregates all phase outputs | test | medium |
| CA-U19 | Draft proposed Exception 30+ entries (staged, not auto-committed) | config | medium |
| CA-U20 | Update `MEMORY.md` + `project_runtime_blockers_ledger.md` | config | low |

### Orchestration (Option A only — optional)

| ID | Title | Type | Risk |
|---|---|---|---|
| CA-U21 | Verify Pi binary + 6 extensions available (Option A precondition) | test | low |
| CA-U22 | Wire Pi orchestration recipes for the 5 phases (Option A only) | config | medium |

## Blockers / ambiguities

1. **Exception 29 activation acknowledgment** — Phase 2 requires `E2B_API_KEY`, which formally exits dormancy for SP15 security findings. User must explicitly acknowledge before CA-U10 kickoff. Same acknowledgment covers Exception 14/24/28 for other `[S]`-tagged postures encountered during fan-out.
2. **Phase 2 cost budget** — estimated ~$12 per full run (16 sandboxes × 15 min × ~$0.05/min). Confirm budget before CA-U10.
3. **just-prompt model availability** — CA-U08 must confirm valid API keys for at least 2 non-Anthropic models (GPT-5 + Gemini) for the different-model constraint in the coder↔validator loop. If only 1 non-Anthropic model is available, Phase 4 runs in degraded mode and CA-U05 validator cannot enforce diversity.
4. **Orchestration decision (A vs B)** — CA-U21 and CA-U22 are Option A only. If Option B is chosen at plan time, drop these two units.

## Critical path

```
CA-U01 (Phase 0)
  ↓
CA-U02 (byte-diff SFA) ───┐
                          ↓
CA-U03 (justfile recipe)  │
                          ↓
CA-U04 (Phase 1 run) ─────┤
                          │
CA-U05..U09 (Phase 2 infra + deps, parallel) ─┐
                                              ↓
CA-U10 (Phase 2 run — 16× sandbox fan-out) ───┤
                                              │
CA-U15 (Phase 3 run, can parallelize w/ U10)  │
                                              ↓
CA-U17 (Phase 4 — consensus on Phase 2 output)
  ↓
CA-U18 (Phase 5 aggregate)
  ↓
CA-U19 (propose exceptions)
  ↓
CA-U20 (update memory + ledger)
```

Critical path length = 10 (U01 → U02 → U04 → U05/06/07 → U10 → U17 → U18 → U19 → U20; U08/U09 verify alongside infra).

## Parallelizable groups

**Group A (Phase 1 infra, independent):** CA-U02, CA-U03
**Group B (Phase 2 infra, independent from Group A):** CA-U05, CA-U06, CA-U07, CA-U08, CA-U09
**Group C (Phase 3 infra, independent from Groups A/B):** CA-U11, CA-U12, CA-U13, CA-U14
**Group D (Phase 4 infra, independent):** CA-U16
**Group E (execution, partial parallelism):** CA-U10 and CA-U15 can run simultaneously once their infra is built (U15 needs no Phase 2 output)
**Group F (Option A only):** CA-U21 then CA-U22, independent from other groups

## External dependencies (must be available)

- `uv` (for SFA execution)
- E2B SDK + `E2B_API_KEY` (Phase 2 only)
- `just-prompt` MCP server + API keys: Anthropic (baseline), OpenAI, Google
- Full-clone tree at `~/Projects/indydevdan-harness-research/research/full-clones/`
- `audits/exceptions.md` current state (1-29)
- Pi binary + extensions (Option A only)

## Structured JSON

```json
{
  "spec": "audits/comprehensive-audit-spec.md",
  "project": "comprehensive-audit",
  "total_units": 22,
  "critical_path_length": 10,
  "units": [
    {
      "id": "CA-U01",
      "title": "Run /find-skills precheck + document matches",
      "type": "script",
      "artifacts": ["audits/phase0-skill-matches-<date>.md"],
      "source_repo": "the-library (global catalog)",
      "dependencies": [],
      "validation": "Phase 0 report enumerates every proposed artifact with match/no-match verdict",
      "risk": "low",
      "phase": 0
    },
    {
      "id": "CA-U02",
      "title": "Build sfa_byte_diff_audit.py (P1-A1)",
      "type": "script",
      "artifacts": ["agents/sfa/sfa_byte_diff_audit.py"],
      "source_repo": "single-file-agents (SP7 pattern)",
      "dependencies": ["CA-U01"],
      "validation": "SFA walks 3-tier clone map, emits MATCH/DRIFT table, cross-refs exceptions.md",
      "risk": "low",
      "phase": 1
    },
    {
      "id": "CA-U03",
      "title": "Add just phase1-byte-diff recipe",
      "type": "config",
      "artifacts": ["justfile"],
      "source_repo": null,
      "dependencies": ["CA-U02"],
      "validation": "just --list shows phase1-byte-diff; just phase1-byte-diff runs without error",
      "risk": "low",
      "phase": 1
    },
    {
      "id": "CA-U04",
      "title": "Execute Phase 1 — byte-parity sweep",
      "type": "test",
      "artifacts": ["audits/phase1-byte-parity-<date>.md"],
      "source_repo": null,
      "dependencies": ["CA-U02", "CA-U03"],
      "validation": "Report published; exit 0 if zero unexplained drift, exit 1 otherwise",
      "risk": "low",
      "phase": 1
    },
    {
      "id": "CA-U05",
      "title": "Build @sandbox-validator-agent subagent (P2-A1)",
      "type": "agent",
      "artifacts": [".claude/agents/sandbox-validator-agent.md"],
      "source_repo": "hooks-mastery (team/validator + team/security patterns)",
      "dependencies": ["CA-U01"],
      "validation": "Subagent definition passes schema check; different-model constraint documented in frontmatter + system prompt",
      "risk": "medium",
      "phase": 2
    },
    {
      "id": "CA-U06",
      "title": "Build sfa_coder_validator_loop.py (P2-A2)",
      "type": "script",
      "artifacts": ["agents/sfa/sfa_coder_validator_loop.py"],
      "source_repo": "single-file-agents (SP7 pattern) + just-prompt (SP4 routing) + sbx-fork (SP15 runtime)",
      "dependencies": ["CA-U05", "CA-U08"],
      "validation": "Loop orchestrator runs inside a sandbox, cycles coder↔validator up to 3 iterations, emits structured verdict to mailbox",
      "risk": "medium",
      "phase": 2
    },
    {
      "id": "CA-U07",
      "title": "Build scripts/phase2_sp_fanout.sh (P2-A3)",
      "type": "script",
      "artifacts": ["scripts/phase2_sp_fanout.sh"],
      "source_repo": null,
      "dependencies": ["CA-U06", "CA-U09"],
      "validation": "Shell driver kicks off 16 sbx-fork invocations with per-SP context bundles, aggregates mailbox output",
      "risk": "medium",
      "phase": 2
    },
    {
      "id": "CA-U08",
      "title": "Verify SP4 just-prompt multi-model routing",
      "type": "test",
      "artifacts": [],
      "source_repo": "just-prompt (SP4)",
      "dependencies": [],
      "validation": "just-prompt responds for anthropic + openai + google; at least 2 non-Anthropic models available for different-model constraint",
      "risk": "low",
      "phase": 2
    },
    {
      "id": "CA-U09",
      "title": "Verify SP15 sbx-fork + E2B runtime",
      "type": "test",
      "artifacts": [],
      "source_repo": "agent-sandboxes (SP15)",
      "dependencies": [],
      "validation": "sbx --help succeeds; E2B_API_KEY valid (but NOT stored in env until user acknowledges Exception 29)",
      "risk": "medium",
      "phase": 2
    },
    {
      "id": "CA-U10",
      "title": "Execute Phase 2 — 16-parallel SP fan-out with coder↔validator loops",
      "type": "test",
      "artifacts": ["audits/phase2-sp<N>-review-<date>.md (16 files)", "audits/phase2-summary-<date>.md", "audits/phase2-mailbox.jsonl"],
      "source_repo": null,
      "dependencies": ["CA-U04", "CA-U07", "CA-U08", "CA-U09"],
      "validation": "All 16 SP reports published; each has a {pass|fail|escalate} verdict; coder↔validator loops all converged within 3 iterations or escalated to human",
      "risk": "high",
      "phase": 2
    },
    {
      "id": "CA-U11",
      "title": "Build sfa_exception_ledger_auditor.py (P3-A1)",
      "type": "script",
      "artifacts": ["agents/sfa/sfa_exception_ledger_auditor.py"],
      "source_repo": "single-file-agents",
      "dependencies": ["CA-U01"],
      "validation": "Walks audits/exceptions.md, checks every Path(s) exists in git, flags stale",
      "risk": "low",
      "phase": 3
    },
    {
      "id": "CA-U12",
      "title": "Build sfa_hook_coverage_matrix.py (P3-A2)",
      "type": "script",
      "artifacts": ["agents/sfa/sfa_hook_coverage_matrix.py"],
      "source_repo": "single-file-agents",
      "dependencies": ["CA-U01"],
      "validation": "Walks .claude/settings.json + .claude/agents/*.md, builds subagent-to-hook coverage matrix, flags gaps (SP15 Ex29 #3 pattern)",
      "risk": "low",
      "phase": 3
    },
    {
      "id": "CA-U13",
      "title": "Build sfa_namespace_collision_detector.py (P3-A3)",
      "type": "script",
      "artifacts": ["agents/sfa/sfa_namespace_collision_detector.py"],
      "source_repo": "single-file-agents",
      "dependencies": ["CA-U01"],
      "validation": "Detects duplicate names across .claude/commands|skills|agents (Exception 23 prime.md pattern)",
      "risk": "low",
      "phase": 3
    },
    {
      "id": "CA-U14",
      "title": "Build sfa_sot_consistency_checker.py (P3-A4)",
      "type": "script",
      "artifacts": ["agents/sfa/sfa_sot_consistency_checker.py"],
      "source_repo": "single-file-agents",
      "dependencies": ["CA-U01"],
      "validation": "Cross-references SoT §1/§4/§8/§11 counts + status markers, flags mismatches",
      "risk": "low",
      "phase": 3
    },
    {
      "id": "CA-U15",
      "title": "Execute Phase 3 — cross-cutting checks",
      "type": "test",
      "artifacts": ["audits/phase3-cross-cutting-<date>.md"],
      "source_repo": null,
      "dependencies": ["CA-U11", "CA-U12", "CA-U13", "CA-U14"],
      "validation": "All 6 checks run (4 SFAs + 2 grep sub-steps); report green or flagged with proposed exceptions",
      "risk": "low",
      "phase": 3
    },
    {
      "id": "CA-U16",
      "title": "Build @cross-model-consensus-agent subagent (P4-A1)",
      "type": "agent",
      "artifacts": [".claude/agents/cross-model-consensus-agent.md"],
      "source_repo": "just-prompt (SP4)",
      "dependencies": ["CA-U08"],
      "validation": "Subagent fan-outs to 3 models via just-prompt, parses verdicts, applies reconciliation rules (unanimous/majority/3-way)",
      "risk": "low",
      "phase": 4
    },
    {
      "id": "CA-U17",
      "title": "Execute Phase 4 — multi-model consensus on borderline findings",
      "type": "test",
      "artifacts": ["audits/phase4-consensus-<date>.md"],
      "source_repo": null,
      "dependencies": ["CA-U10", "CA-U16"],
      "validation": "Every borderline finding from Phase 2 has a locked verdict; 3-way disagreements escalated to human",
      "risk": "medium",
      "phase": 4
    },
    {
      "id": "CA-U18",
      "title": "Execute Phase 5 — @builder aggregates all phase outputs",
      "type": "test",
      "artifacts": ["audits/comprehensive-review-<date>.md"],
      "source_repo": null,
      "dependencies": ["CA-U04", "CA-U10", "CA-U15", "CA-U17"],
      "validation": "Comprehensive report published with executive summary, per-SP verdict table, aggregated priorities",
      "risk": "medium",
      "phase": 5
    },
    {
      "id": "CA-U19",
      "title": "Draft proposed Exception 30+ entries (staged, NOT auto-committed)",
      "type": "config",
      "artifacts": ["audits/phase5-proposed-exceptions-<date>.md"],
      "source_repo": null,
      "dependencies": ["CA-U18"],
      "validation": "Every new finding without existing coverage gets a draft Exception entry in full exceptions.md format",
      "risk": "medium",
      "phase": 5
    },
    {
      "id": "CA-U20",
      "title": "Update MEMORY.md + project_runtime_blockers_ledger.md",
      "type": "config",
      "artifacts": ["~/.claude/projects/.../memory/MEMORY.md", "~/.claude/projects/.../memory/project_runtime_blockers_ledger.md"],
      "source_repo": null,
      "dependencies": ["CA-U19"],
      "validation": "Memory index references the comprehensive review; runtime-blocker ledger reflects any new [S]-tagged items",
      "risk": "low",
      "phase": 5
    },
    {
      "id": "CA-U21",
      "title": "Verify Pi binary + 6 extensions (Option A precondition)",
      "type": "test",
      "artifacts": [],
      "source_repo": "pi-vs-claude-code (SP12)",
      "dependencies": [],
      "validation": "pi --version succeeds; ext-agent-chain / ext-purpose-gate / ext-agent-team / ext-subagent-widget / ext-drive-dispatch / ext-tool-counter-widget all loadable",
      "risk": "low",
      "phase": "orch-A"
    },
    {
      "id": "CA-U22",
      "title": "Wire Pi orchestration recipes for the 5 phases (Option A only)",
      "type": "config",
      "artifacts": ["justfile (new audit-phase-N recipes)"],
      "source_repo": null,
      "dependencies": ["CA-U21"],
      "validation": "just audit-phase-1 through just audit-phase-5 recipes exist; each dispatches to the correct Pi extension stack",
      "risk": "medium",
      "phase": "orch-A"
    }
  ],
  "blockers": [
    "Exception 29 activation acknowledgment (Phase 2 precondition)",
    "Phase 2 cost budget ~$12 per run",
    "just-prompt multi-model API availability",
    "Orchestration option A vs B decision"
  ],
  "parallelizable_groups": [
    {"name": "Phase 1 infra", "units": ["CA-U02", "CA-U03"]},
    {"name": "Phase 2 infra", "units": ["CA-U05", "CA-U06", "CA-U07", "CA-U08", "CA-U09"]},
    {"name": "Phase 3 infra", "units": ["CA-U11", "CA-U12", "CA-U13", "CA-U14"]},
    {"name": "Phase 4 infra", "units": ["CA-U16"]},
    {"name": "Option A Pi (optional)", "units": ["CA-U21", "CA-U22"]},
    {"name": "Execution parallel (U10 + U15)", "units": ["CA-U10", "CA-U15"]}
  ],
  "recommended_order": [
    "CA-U01",
    "CA-U02", "CA-U03", "CA-U05", "CA-U08", "CA-U09", "CA-U11", "CA-U12", "CA-U13", "CA-U14", "CA-U16", "CA-U21",
    "CA-U06", "CA-U07", "CA-U22",
    "CA-U04",
    "CA-U10", "CA-U15",
    "CA-U17",
    "CA-U18", "CA-U19", "CA-U20"
  ]
}
```

## Recommended execution order (narrative)

1. **CA-U01** — Phase 0 precheck (sequential, informs artifact list)
2. **Parallel build wave** (all independent of each other, depend only on CA-U01):
   - CA-U02 Phase 1 SFA
   - CA-U03 Phase 1 recipe
   - CA-U05 Phase 2 validator subagent
   - CA-U08 Phase 2 just-prompt verify
   - CA-U09 Phase 2 sbx-fork verify
   - CA-U11–U14 Phase 3 SFAs (4 of them)
   - CA-U16 Phase 4 consensus agent
   - CA-U21 Option A Pi verify (skip if Option B)
3. **Phase 2 + Option A second wave** (depend on first wave):
   - CA-U06 Phase 2 loop SFA (needs CA-U05, CA-U08)
   - CA-U07 Phase 2 fan-out script (needs CA-U06, CA-U09)
   - CA-U22 Option A Pi wiring (skip if Option B)
4. **Phase 1 execution:**
   - CA-U04 — Phase 1 byte-parity sweep
5. **Phase 2 + Phase 3 parallel execution:**
   - CA-U10 — Phase 2 fan-out (heavy, ~1.5 hr, ~$12)
   - CA-U15 — Phase 3 cross-cutting (can run alongside)
6. **Phase 4 reconciliation:**
   - CA-U17 — multi-model consensus on borderline findings
7. **Phase 5 tail:**
   - CA-U18 — @builder aggregate
   - CA-U19 — propose exceptions (staged)
   - CA-U20 — update memory + ledger

## Next step

Hand this artifact to `/architect` via `architect audits/comprehensive-audit-scout.md` to produce the implementation plan (sequencing, agent assignments, commit boundaries, verification steps per unit).
