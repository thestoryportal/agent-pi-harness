# Phase 0 — Skill Discovery Precheck

**Date:** 2026-04-14
**Unit:** CA-U01
**Phase:** 0 (precheck for Comprehensive Audit infrastructure build)
**Purpose:** Avoid reinventing skills/agents/SFAs that already exist in the local library or the external skill registry.

## Sources consulted

1. **Local global catalog** — `~/.claude/skills/library/library.yaml` (82 lines, ArhuGula-native only)
2. **External skill registry** — `npx skills search <query>` via the open agent skills CLI (https://skills.sh/)

## Proposed artifacts (from spec §9)

The Comprehensive Audit plan proposes 9 new artifacts:

**Single-file agents (5):**
- P1-A1: `sfa_byte_diff_audit.py`
- P2-A2: `sfa_coder_validator_loop.py`
- P3-A1: `sfa_exception_ledger_auditor.py`
- P3-A2: `sfa_hook_coverage_matrix.py`
- P3-A3: `sfa_namespace_collision_detector.py`
- P3-A4: `sfa_sot_consistency_checker.py`

**Specialized subagents (3):**
- P2-A1: `@sandbox-validator-agent`
- P4-A1: `@cross-model-consensus-agent`
- P3-A5: `@exception-auditor-agent` (optional, may be subsumed by P3-A1 SFA)

**Shell scripts (1):**
- P2-A3: `scripts/phase2_sp_fanout.sh`

## 1. Local catalog sweep

`~/.claude/skills/library/library.yaml` lists only ArhuGula-native harness infrastructure:
- 4 skills: `damage-control`, `library`, `prime`, `scout`
- 7 agents: `architect`, `builder`, `schema-reviewer`, `scout-agent`, `security`, `spec-checker`, `validator`
- 6 prompts: `architect`, `build`, `harness-review`, `install`, `maintenance`, `migrate`

**Zero direct matches** for the 9 proposed artifacts. The local catalog contains session-level review infrastructure (`@validator`, `@security`, `/harness-review`) that is **reused by** the new artifacts but does not replace them:

- `@validator` is read-only and session-scoped; it does not enforce a different-model constraint and cannot run inside an E2B sandbox. The proposed `@sandbox-validator-agent` extends this pattern.
- `@security` provides the adversarial system-prompt style that the sandbox validator will inherit.
- `/harness-review` is the multi-agent review command; the Comprehensive Audit's Phase 2 reuses this pattern per-SP inside each sandbox.
- `schema-reviewer` is the closest structural analog for `sfa_sot_consistency_checker.py` but is domain-specific (database schemas, not SoT cross-references).

**Verdict:** local catalog provides reusable building blocks, not replacements.

## 2. External registry search

Searched the open agent skills registry with 6 keyword queries:

| Query | Results | Top matches |
|---|---|---|
| `audit` | 452 skills | `qa-auditor` (3★), `dependency-auditor`, `isms-audit-expert`, `qms-audit-expert`, `skill-security-analyzer`, `infra-auditor` (all 0★/0 installs) |
| `diff` | 261 skills | `video-comparer` (147★), `typescript-review` — all domain-mismatched |
| `drift` | 31 skills | `design-system-governance` (design-token drift), `terraform-iac` (cloud state drift), `infra-auditor` (0★) |
| `code review` | 330 skills | `receiving-code-review` by obra (**13,645★**), `subagent-driven-development`, `github-code-review` (0★) |
| `consensus` | 40 skills | **`consensus` (0★, 0 installs)**, `hive-mind-advanced`, `cfn-loop-orchestration`, `plan-down` |
| `sandbox` | 55 skills | `flow-nexus-platform`, `flow-nexus-neural` (E2B wrappers, no validator pattern) |
| `validator` | 190 skills | `validator-role-skill` (0★), `slack-gif-creator` (14,487★, wrong domain) |

### Detailed review of the 2 closest matches

**consensus** (tylerburleigh/claude-model-chorus)
- Description: "Multi-model consultation with parallel execution and configurable synthesis strategies"
- Concept match: **very close** — maps directly to P4-A1 `@cross-model-consensus-agent`
- Adoption signal: **0 stars, 0 installs** — zero trust signal
- Source: https://github.com/tylerburleigh/claude-model-chorus
- Updated: 2026-01-07
- **Verdict:** REJECT. Concept is right but zero adoption means we'd need to vet the implementation line-by-line, which costs more than building natively. Build P4-A1 using SP4 `just-prompt` directly (already trusted infrastructure).

**cfn-loop-orchestration** (masharratt/claude-flow-novice)
- Description: "CFN Loop workflow orchestration — three-loop structure management with gate checks and consensus. Use when coordinating Loop 3 implementers and Loop 2 validators, managing iteration..."
- Concept match: **very close** — maps to P2-A2 `sfa_coder_validator_loop.py` structure (Loop 3 = coder, Loop 2 = validator, consensus = reconciliation)
- Adoption signal: **0 stars, 0 installs**
- Source: https://github.com/masharratt/claude-flow-novice
- Updated: 2026-01-07
- **Verdict:** REJECT. Same reasoning as `consensus` — concept is right, zero trust. Build P2-A2 natively from SP7 SFA patterns + SP4 just-prompt + SP15 sbx-fork primitives already in-tree.

### Adjacent skills worth noting (for pattern inspiration, NOT replacement)

- **`receiving-code-review`** by obra (13,645 stars) — behavioral skill for how an agent handles code review feedback. Does not replace any proposed artifact, but the *pattern* is relevant to how the coder agent inside the P2-A2 loop should interpret validator verdicts. Consider reading the SKILL.md for prompt-design inspiration for the coder agent's refactor-after-fail phase.
- **`subagent-driven-development`** — "dispatches fresh subagent for each task with code review between tasks" — structural pattern match for Wave 1 infra build, not audit execution. Consider as a future optimization for the `/build` workflow itself, not this audit.
- **`infra-auditor`** — "Audit infrastructure status, health, and compliance without modifications - provides observability and drift detection" — structural template for report-only audit SFAs (P3-A1..P3-A4). Zero stars, so treat as an API-shape reference only, not a dependency.
- **`design-system-governance`** — "Detect and track design token drift between Figma design systems and code implementations - report-only skill that identifies inconsistencies" — domain mismatch (design tokens vs code files) but report-only drift detection pattern is conceptually what P1-A1 + P3-A1 do.

## 3. Final artifact list

**No matches replace any proposed artifact.** All 9 artifacts must be built natively.

| Artifact | Build decision | Notes |
|---|---|---|
| P1-A1 `sfa_byte_diff_audit.py` | BUILD | No registry match; follows SP7 `sfa_bash` + `sfa_codebase_context` patterns |
| P2-A1 `@sandbox-validator-agent` | BUILD | Reuses @validator + @security prompt style; adds E2B isolation + different-model constraint (SP4 just-prompt routing); inspired by `cfn-loop-orchestration` concept but not dependent on it |
| P2-A2 `sfa_coder_validator_loop.py` | BUILD | No trusted match; reuses SP7 SFA pattern + SP4 just-prompt + SP15 sbx-fork primitives |
| P2-A3 `scripts/phase2_sp_fanout.sh` | BUILD | Purely ArhuGula-specific; no external equivalent expected |
| P3-A1 `sfa_exception_ledger_auditor.py` | BUILD | Follows SP7 `sfa_codebase_context` pattern; ArhuGula-specific (reads our `exceptions.md` format) |
| P3-A2 `sfa_hook_coverage_matrix.py` | BUILD | Follows SP7 `sfa_codebase_context` pattern; ArhuGula-specific (reads our `.claude/settings.json` + agent frontmatter) |
| P3-A3 `sfa_namespace_collision_detector.py` | BUILD | Follows SP7 `sfa_bash` pattern; ArhuGula-specific (scans our `.claude/` tree layout) |
| P3-A4 `sfa_sot_consistency_checker.py` | BUILD | Follows SP7 `sfa_codebase_context` pattern; ArhuGula-specific (reads SoT section layout) |
| P3-A5 `@exception-auditor-agent` | SKIP | Subsumed by P3-A1 SFA per spec. Revisit only if the SFA output needs conversational framing. |
| P4-A1 `@cross-model-consensus-agent` | BUILD | No trusted match; reuses SP4 just-prompt directly as the underlying primitive |

**Result:** 9 artifacts to build → **8 to build** (P3-A5 skipped per spec). Build plan from `audits/comprehensive-audit-plan.md` remains valid as-is.

## 4. Recommendations for the build agent

When building each artifact, the `@builder` agent should reference:

- **For all SFAs:** `/Users/robertrhu/Projects/arhugula/agents/sfa/sfa_bash_editor_agent_anthropic_v3.py` (uv-run shebang + inline deps), `sfa_codebase_context_agent_v3.py` (codebase walking), `sfa_duckdb_anthropic_v2.py` (structured output)
- **For `@sandbox-validator-agent`:** `/Users/robertrhu/Projects/arhugula/.claude/agents/team/validator.md` (frontmatter + prompt structure) + `.claude/agents/security.md` (adversarial posture)
- **For `@cross-model-consensus-agent`:** SP4 just-prompt CLI — read `apps/just-prompt/` for the available models list before finalizing the prompt
- **For `P2-A2` coder↔validator loop:** SP15 sbx-fork `apps/sandbox_workflows/src/modules/forks.py` for the fork dispatch pattern, SP4 just-prompt for model-routing primitives, SP7 SFAs for the CLI wrapper shape

## 5. Blockers and decisions

- **No blockers surfaced by Phase 0.** Proceed to Wave 1 infra build.
- **No decisions deferred to user.** The 0-star adoption of `consensus` and `cfn-loop-orchestration` is a clear rejection per the find-skills skill's own "verify quality" guidance ("Prefer skills with 1K+ installs. Be cautious with anything under 100.").

## 6. Next step

Proceed to **Wave 1 — Infra build**, starting with the recommended first commit batch:

- CA-U02 (`sfa_byte_diff_audit.py`)
- CA-U03 (`just phase1-byte-diff` recipe)
- CA-U05 (`@sandbox-validator-agent` subagent)

Plus CA-U01 output (this file) as part of the same commit.
