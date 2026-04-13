# ArhuGula — Documented Exceptions to the Disler-Authoritative Rule

**Created:** 2026-04-13
**Branch:** `audit/identicality-2026-04-13`
**Precedence:** Disler wins unless an exception is listed here. Every exception must cite the SP audit round that approved it and a rationale.
**Classification note:** exceptions are still **DRIFT** per `feedback_disler_authoritative.md` — this file documents conscious, user-approved deviations, not a downgrade to MATCH.

---

## Structure

Each exception entry has:

- **Path(s)** — files or directories affected
- **SP audit round** — which audit round surfaced and approved the exception
- **Decision date** — absolute date of user approval
- **Rationale** — why the deviation is justified
- **Review cadence** — when to re-examine
- **Related findings** — scout/plan references
- **Follow-up actions** — what still needs to happen

---

## Exception 1 — Audit infrastructure tier (Tier 3)

**Decision:** Decision 2B, SP1 round 1

**Path(s)** (confirmed inventions that constitute the audit pipeline itself):
- `.claude/skills/prime/SKILL.md`
- `.claude/skills/scout/SKILL.md`
- `.claude/commands/architect.md`
- `.claude/commands/harness-review.md`
- `.claude/commands/migrate.md`
- `.claude/agents/architect.md`
- `.claude/agents/scout-agent.md`

**Removed from Exception 1 after attribution round 2** (2026-04-13):
- `.claude/agents/spec-checker.md` → routed to **Exception 5** (confirmed invention, NOT audit infrastructure)
- `.claude/agents/schema-reviewer.md` → routed to **Exception 5** (confirmed invention, NOT audit infrastructure)

**SP audit round:** SP1 round 1 (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**
These files are the audit pipeline itself — the `/scout`, `/architect`, `/build`, `/harness-review` commands and their supporting subagents/skills are what execute the identicality audit. Deleting them per the Disler-authoritative rule would break the audit mid-run (bootstrap paradox).

**Tier framing:** The user's authoritative hierarchy is Tier 1 (Disler full-clones, byte-level) → Tier 2 (IndyDevDan Comprehensive docs, intent-level) → ArhuGula (the target of the audit). This exception defines an implicit **Tier 3 — audit-orchestration infrastructure**, which lives above the Disler-replicated harness and is inherently ArhuGula-native because Disler does not ship a self-audit tool. The identicality goal applies to the harness being audited (Tiers 1+2), not to the tooling that audits it (Tier 3).

**Review cadence:** Quarterly, or whenever a Disler repo adds a self-audit pattern we could import.

**Related findings:**
- `audits/SP1-scout.md` — ESCALATE-T1 items E1, E2, E3
- `audits/SP1-plan.md` — D4 decision, E1–E3 escalation entries
- Attribution search round 1 (2026-04-13): 9 of 10 candidate files NO MATCH in 19 full-clones; builder.md + validator.md FOUND in hooks-mastery `agents/team/`
- Attribution search round 2 (2026-04-13): targeted search for `spec-checker.md` + `schema-reviewer.md` in `the-library` + `claude-code-is-programmable` — CONFIRMED NO MATCH across all 19 clones; both routed to Exception 5

**Follow-up actions:**
1. (Complete) Attribution round 2: CONFIRMED NO MATCH for spec-checker + schema-reviewer across all 19 full-clones
2. Tier-3 files stay permanently under this exception; expansion of Tier 3 requires explicit user approval + new exception entry
3. Quarterly review to check if Disler has added any self-audit patterns

---

## Exception 2 — Validator-forced drift on upstream Python files

**Decision:** Decision 1D, SP1 round 1

**Path(s):**
- `.claude/status_lines/status_line_v2.py` — upstream has unused `import os`; ArhuGula's `ruff_validator.py` PostToolUse hook blocked the byte-identical copy; ArhuGula version omits the import

**SP audit round:** SP1 round 1 (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**
ArhuGula's `ruff_validator.py` PostToolUse hook blocks file writes that fail ruff lint checks. When upstream Disler repos have lint issues (unused imports, line length, missing docstrings, etc.), the validator **forces** the committed version to deviate from upstream byte-identicality. This is a genuine methodology tension between the audit goal (byte-identical upstream) and the validation pipeline (upstream-clean code).

**Decision:** accept validator-forced drift as a known, per-file exception. The validator hooks themselves are **SP3 (Validation Pipeline)** scope. The proper resolution is either to set the validators to log-only during audit commits, or to add `# ruff: noqa` markers at the top of restored files. Both options are deferred to SP3 audit.

**Review cadence:** At SP3 audit round. When SP3 scout classifies the validator hooks, this exception's resolution must be part of SP3's plan.

**Related findings:**
- `audits/SP1-plan.md` — Appendix A "third-round discovery — ruff validator forces drift from upstream"
- Commit `9f74fc3` in `audit/identicality-2026-04-13` — the specific file where this was observed

**Follow-up actions:**
1. SP3 scout: classify validator hooks (`ruff_validator.py`, `ty_validator.py`, and any others) as blocking vs advisory
2. SP3 architect: propose a policy — e.g., validators run in advisory mode during audit commits, blocking mode at all other times
3. SP3 build: execute the policy change
4. SP3 verify: re-run affected file restores (including `status_line_v2.py`) with upstream byte-identical content; remove the deviation from this exception

---

## Exception 3 — SP2-blocked SP1 reverts

**Decision:** Option 2 path, SP1 round 1

**Affected commits (8 of 14 in SP1-plan.md):**
1. Commit 1 — `.claude/hooks/utils/tts/*.py` (4 files)
2. Commit 2 — `.claude/hooks/utils/llm/*.py` (4 files)
3. Commit 4 — `.claude/settings.json` statusLine block revert
4. Commit 5 — `.claude/statusline.sh` deletion
5. Commit 6 — `.claude/hooks/setup_init.py` + `setup_maintenance.py` restore
6. Commit 7 — `.claude/settings.json` Setup hook wiring revert
7. Commit 8 — `.claude/hooks/setup.py` deletion
8. Commit 14 — `.claude/hooks/session_start.py` `REQUIRED_HOOKS` purge

**SP audit round:** SP1 round 1 (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**
These 8 commits touch paths that are either intentionally protected by `readOnlyPaths` in `patterns.yaml` (existing hook files, `.claude/settings.json`) or unintentionally blocked by the fnmatch over-reach bug (the rule `.claude/hooks/*.py` matches subdirectories because Python's `fnmatch.fnmatch()` does not treat `/` as special). The audit cannot self-unlock per `feedback_damage_control_self_unlock.md`.

Cleaner path: let SP2 audit fix the underlying bug (`patterns.yaml` narrowing or hook code change), then re-run these 8 commits as an **SP1 resume pass**.

**Review cadence:** When SP2 audit closes.

**Related findings:**
- `audits/SP1-plan.md` — Appendix A (blocked commits table)
- `project_sp2_architectural_gaps.md` memory — already documents the fnmatch over-reach as a P0 SP2 follow-up
- Builder execution reports from 2026-04-13 SP1 run (Commit 1 block + Commit 4 block)

**Follow-up actions:**
1. SP2 scout: identifies the fnmatch bug + `.claude/settings.json` in `readOnlyPaths`
2. SP2 architect: proposes `patterns.yaml` narrowing or `write_damage_control.py` path-matching fix
3. SP2 build: executes the fix
4. SP2 verify: re-runs SP1 Commits 1, 2, 4, 5, 6, 7, 8, 14 against fixed rules
5. Mark SP1 as "SP1 round 1 complete" once those 8 commits land
6. Update this exception to "resolved"

---

## Exception 4 — `builder.md` + `validator.md` mis-location + content drift

**Decision:** Decision 3B, SP1 round 1

**Path(s):**
- `.claude/agents/builder.md` — upstream path is `claude-code-hooks-mastery/.claude/agents/team/builder.md`; ArhuGula has it at flat `agents/` level. Structural content delta: ArhuGula uses sonnet model with simplified hooks; upstream uses opus with complex ruff+type validation hooks.
- `.claude/agents/validator.md` — upstream path is `claude-code-hooks-mastery/.claude/agents/team/validator.md`; same flat-vs-subdirectory mismatch. Content delta: ArhuGula uses sonnet + plan mode + read-only focus; upstream uses opus + task-based workflow.

**SP audit round:** SP1 round 1 (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**
Both files are **FOUND** upstream (unlike Exception 1's inventions), but need two actions to reach MATCH:
1. `git mv` from `.claude/agents/` (flat) to `.claude/agents/team/` (upstream layout)
2. Content revert to upstream byte-identical

Both actions are likely blocked by the same SP2 fnmatch / `readOnlyPaths` issue affecting Exception 3 — specifically, `.claude/agents/` is expected to also be in `readOnlyPaths` based on the pattern of blocks observed with `.claude/hooks/` and `.claude/settings.json`. SP2 fixup batch should include verifying and unblocking `.claude/agents/` edits.

**Review cadence:** When SP2 audit closes (same as Exception 3).

**Related findings:**
- Attribution search round 1 (2026-04-13) — E1 results: FOUND in hooks-mastery `agents/team/`
- `audits/SP1-plan.md` — E1 escalation

**Follow-up actions:**
1. SP2 scout: verify `.claude/agents/` is in `readOnlyPaths` (expected yes)
2. SP2 fixup batch: `git mv` from flat `agents/` to `agents/team/` for both files
3. SP2 fixup batch: revert content of both files to upstream byte-identical
4. SP1 resume pass: verify move + content revert landed correctly
5. Update this exception to "resolved"

---

## Exception 5 — Confirmed invention deletions (deferred to SP2)

**Decision:** Attribution round 2 classification, SP1 round 1

**Path(s):**
- `.claude/agents/spec-checker.md` — invention, classify DELETE per Disler-authoritative rule
- `.claude/agents/schema-reviewer.md` — invention, classify DELETE per Disler-authoritative rule

**SP audit round:** SP1 round 1 (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**
Attribution round 2 (2026-04-13) confirmed both files have zero upstream source across all 19 Disler full-clones. Primary search: neither exists in `the-library` or `claude-code-is-programmable`. Secondary re-verify: glob + grep across all full-clones returned NO MATCH in every repo. These are genuine ArhuGula inventions, not mis-routed files.

Under the Disler-authoritative rule, confirmed inventions must be deleted. However, deletion requires removing files in `.claude/agents/`, which is expected to be in `readOnlyPaths` based on the pattern of blocks observed with `.claude/hooks/` and `.claude/settings.json` during SP1 round 1. Deletion is deferred to SP2 fixup batch.

**Distinction from Exception 1:** These two files are **NOT audit infrastructure** — they are unused/low-value inventions (spec compliance checker, data schema validator) that the audit pipeline itself doesn't depend on. They don't need the Tier-3 preservation carve-out. They're just drift that needs to be removed.

**Review cadence:** When SP2 audit closes.

**Related findings:**
- `audits/SP1-scout.md` — ESCALATE-T1 item E1 (subset)
- `audits/SP1-plan.md` — E1 routing recommendation
- Attribution round 1 report (2026-04-13): NO MATCH across all full-clones
- Attribution round 2 report (2026-04-13): CONFIRMED NO MATCH (primary + secondary re-verify)

**Follow-up actions:**
1. SP2 scout: verify `.claude/agents/` is in `readOnlyPaths` (expected yes)
2. SP2 fixup batch: `rm .claude/agents/spec-checker.md` + `rm .claude/agents/schema-reviewer.md`
3. SP2 verify: confirm both files are absent
4. Update this exception to "resolved"

---

## Active exceptions summary

| # | Title | SP | Date | Status | Review when |
|---|---|---|---|---|---|
| 1 | Audit infrastructure tier (Tier 3) | SP1 r1 | 2026-04-13 | active | Quarterly |
| 2 | Validator-forced drift (ruff) | SP1 r1 | 2026-04-13 | active | SP3 audit |
| 3 | SP2-blocked SP1 reverts (8 commits) | SP1 r1 | 2026-04-13 | active | SP2 audit |
| 4 | builder/validator location + content | SP1 r1 | 2026-04-13 | active | SP2 audit |
| 5 | Confirmed invention deletions (spec-checker, schema-reviewer) | SP1 r1 | 2026-04-13 | active | SP2 audit |

## How to close an exception

1. The SP audit round listed in "Review when" runs
2. That audit's plan includes a "resolve SP1 exception N" item
3. The build phase executes the resolution
4. The verify phase confirms the exception is actually resolved (file is now MATCH, etc.)
5. This file is updated to move the exception from "active" to "resolved" (with resolution date)
6. Closed exceptions move to an archive section at the bottom of this file

## Tier-3 architecture note

Per Exception 1, ArhuGula's audit infrastructure lives at **Tier 3** above the Disler-replicated harness. This is a one-time user-approved architectural decision (2026-04-13) that establishes:

- **Tier 1**: Disler full-clones at `~/Projects/indydevdan-harness-research/research/full-clones/` (byte-level authoritative)
- **Tier 2**: IndyDevDan Comprehensive docs at `~/Projects/indydevdan-harness-research/research/IndyDevDan Comprehensive/` (intent-level authoritative)
- **Tier 3**: ArhuGula audit-orchestration infrastructure (audit-native, has no Disler counterpart, stays ArhuGula-specific)
- **Target of audit**: the Disler-replicated portion of ArhuGula (Tiers 1+2 conformance)

New files added under Tier 3 require a separate user decision and an entry in this exceptions file. Tier 3 does **not** expand silently.
