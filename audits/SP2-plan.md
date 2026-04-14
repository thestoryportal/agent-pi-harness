# SP2 Audit — Revert Plan

**Date:** 2026-04-13
**SP:** 2 — Security Hardening (damage-control)
**Phase:** Architect (audit mode, v2 methodology)
**Input:** `audits/SP2-scout.md`, SP2 Phase A outcome (Ex4 + Ex5 + Ex3 item 10 landed 2026-04-13)
**Audit branch:** `audit/identicality-2026-04-13`

## Summary

| Classification | Commit count | File touches |
|---|---:|---:|
| AUTO-REVERT | 4 | ~8 |
| DECISION-REQUIRED | 12 | ~30 |
| ESCALATE | 4 | — (routing or gate items) |
| SP1 resume pass unblocked after D10+D11 gate | 18 | varies |

**Estimated total SP2 commits:** 16 (AUTO-REVERT + DECISION-REQUIRED, pending user gate decisions) + 18 SP1 resume-pass commits after SP2 unblocks them.

### Phase A state (2026-04-13, pre-architect)

Four Phase A commits landed before this plan: `c04bc09` (D3), `36bac66` (Ex4 builder), `7fd0f3c` (Ex4 validator), `9ed2995` (Ex5), plus `21fd4c4` paperwork. SP2-3 RESOLVED. Ex4 + Ex5 RESOLVED. Exception 3 reduced from 19 commits to 18.

---

## Commit plan (dependency-ordered)

### Commit 1 — Fix fnmatch over-reach in damage-control match_path() (AR1)

- **Classification:** AUTO-REVERT (bug fix, no user decision needed)
- **Tier:** T1 (correctness, not drift)
- **Action:** Replace the `fnmatch.fnmatch()` glob matching in `match_path()` with path-segment-aware matching via `pathlib.PurePath.match()` or an explicit segment-aware algorithm. The current implementation fails for the rule `.claude/hooks/*.py` against subdirectory files because `fnmatch` does not treat `/` as a separator — `*` greedily consumes across path boundaries. Affects 3 per-tool hooks + the catch-all `pre_tool_use.py`.
- **Files touched:**
  - `.claude/hooks/edit_damage_control.py` — rewrite `match_path()` function (lines 42-93)
  - `.claude/hooks/write_damage_control.py` — rewrite `match_path()` (lines 42-93; currently byte-identical to edit)
  - `.claude/hooks/pre_tool_use.py` — rewrite `match_path()` (lines 48-80)
  - `.claude/hooks/bash_damage_control.py` — audit `check_path_patterns()` + `glob_to_regex()` for the same issue; likely no change needed (already uses `[^\s/]*` in the regex conversion which DOES respect `/`)
- **Upstream source:** none — this is an ArhuGula bug in ArhuGula-invented helper code (`match_path` does not exist in upstream because upstream uses a simpler path check)
- **Blast radius:** high — every PreToolUse path check runs through this function. Requires regression coverage.
- **Verification:** Re-run `audits/sp2_verify.py` with new test cases added for subdirectory `.py` files under `.claude/hooks/utils/`. Expected: match on top-level `.claude/hooks/setup.py`, NO match on `.claude/hooks/utils/tts/elevenlabs_tts.py`.
- **Depends on:** D10 user decision (whether top-level `.claude/hooks/*.py` rule is narrowed or kept)
- **Rollback:** `git revert <commit-sha>` restores fnmatch behavior
- **Commit message:** `audit: SP2 AR1 — fix match_path() fnmatch over-reach (path-segment-aware glob)`

Note: this commit is itself blocked by the current `.claude/hooks/*.py` readOnlyPaths rule. Requires D10 resolution first (temporary bypass, narrowing, or audit-mode flag).

---

### Commit 2 — Delete `.gitkeep` placeholders in damage-control skill

- **Classification:** AUTO-REVERT
- **Tier:** T1 (invention removal)
- **Action:** Delete the 3 `.gitkeep` placeholder files that are ArhuGula-invented and have no upstream counterpart. Upstream distribution does not need `.gitkeep` because the hooks/cookbook/test-prompts directories are non-empty.
- **Files touched:**
  - `.claude/skills/damage-control/hooks/.gitkeep` — delete
  - `.claude/skills/damage-control/cookbook/.gitkeep` — delete
  - `.claude/skills/damage-control/test-prompts/.gitkeep` — delete
- **Upstream source:** none (files absent upstream)
- **Blast radius:** isolated (no consumers)
- **Depends on:** (none)
- **Rollback:** `git revert` (files recreated)
- **Commit message:** `audit: SP2 AR2 — remove .gitkeep invention placeholders from damage-control skill`

---

### Commit 3 — Restore upstream `sentient.md` command

- **Classification:** AUTO-REVERT
- **Tier:** T1 (MISSING → restore)
- **Action:** Copy `claude-code-damage-control/.claude/commands/sentient.md` byte-identical into ArhuGula at `.claude/commands/sentient.md`. This is a 1.1k adversarial test-prompt launcher that invokes the `test-prompts/sentient*.md` suite. Currently MISSING[T1] per SP2-scout.md.
- **Files touched:**
  - `.claude/commands/sentient.md` — create
- **Upstream source:** `~/Projects/indydevdan-harness-research/research/full-clones/claude-code-damage-control/.claude/commands/sentient.md`
- **Blast radius:** isolated (new file, no existing references)
- **Depends on:** (none)
- **Rollback:** `git rm` restores absence
- **Commit message:** `audit: SP2 AR3 — restore sentient.md adversarial test launcher from upstream`

---

### Commit 4 — Verify match_path() fix with expanded probe suite

- **Classification:** AUTO-REVERT (test coverage)
- **Tier:** Meta (audit tooling)
- **Action:** Expand `audits/sp2_verify.py` to cover the fnmatch-over-reach regression cases. Add test cases for subdirectory writes (`utils/tts/*.py`, `utils/llm/*.py`), top-level writes (`setup.py`, `session_start.py`), and the unblocked-already paths (`.claude/commands/`, `.claude/agents/`). Re-run and confirm expected allow/block decisions match the new `match_path()` semantics.
- **Files touched:**
  - `audits/sp2_verify.py` — expand
- **Depends on:** Commit 1 (fnmatch fix)
- **Commit message:** `audit: SP2 AR4 — expand sp2_verify.py probe suite with fnmatch regression cases`

---

## Decision gate items

Architect classifies the twelve open decisions with a recommendation, rationale, and trade-off. User resolves at the decision gate.

### D1 — Filename convention (hyphen vs underscore)

**Files:** `.claude/skills/damage-control/hooks/{bash,edit,write}_damage_control.py` + `.claude/hooks/{bash,edit,write}_damage_control.py`
**Upstream form:** `bash-tool-damage-control.py`, `edit-tool-damage-control.py`, `write-tool-damage-control.py` (hyphen-separated)
**ArhuGula form:** `bash_damage_control.py`, `edit_damage_control.py`, `write_damage_control.py` (underscore)
**Conflict:** CLAUDE.md Naming Conventions §Naming says "hook files use underscores" — ArhuGula's rename is internally consistent with project rules, but violates Tier 1 byte-identicality.
**Options:**
- (A) Rename to hyphen form, update all references in settings.json + patterns.yaml comments + tests. Touches ~15 files. Brings Tier 1 MATCH but violates ArhuGula convention.
- (B) Keep underscore form, document as SP2 exception. No file touches; preserves convention consistency.
**Architect recommendation:** **(B)** — the convention rule in CLAUDE.md predates this audit and is cited consistently across every other hook file. Breaking it only for damage-control creates inconsistency. Document as exception, record the reason: "hook files use underscores per CLAUDE.md §Naming, which overrides upstream filename form."

---

### D2 — Directory layout (flat vs split)

**Files:** `.claude/skills/damage-control/hooks/`
**Upstream form:** `hooks/damage-control-python/*.py` (5 files) + `hooks/damage-control-typescript/*.ts` (5 files)
**ArhuGula form:** `hooks/*.py` flat (3 files)
**Options:**
- (A) Restore upstream split: `mkdir damage-control-python/`, move the 3 existing files in, restore the 2 missing Python files (depends on D4+D5), optionally restore TypeScript tree (depends on D3).
- (B) Keep flat layout, document as exception.
**Architect recommendation:** **(A)** — the split exists upstream because the intent is to ship multiple language variants from the same skill distribution. Flattening is a self-contained decision that erases the variant dimension. Even if D3 = Python-only, the `damage-control-python/` subdirectory is meaningful as a "Python implementation" namespace. Restoring the split costs ~3 file moves and matches upstream exactly for the paths that ship.
**Depends on:** D1 (filename convention — rename happens during move)

---

### D3 — TypeScript variant ship policy

**Files:** MISSING — 5 TypeScript files totaling ~38k (upstream `hooks/damage-control-typescript/`)
**Options:**
- (A) Restore all 5 TypeScript files byte-identical. No code consumer yet (ArhuGula runs Python hooks). The `.ts` files are distributable reference implementations for users who prefer a Bun-based hook runtime.
- (B) Drop as language-variant exception. Document rationale: "ArhuGula is a Python-only project; TypeScript hooks are unused reference implementations."
**Architect recommendation:** **(A) with scope caveat** — the upstream SKILL.md explicitly advertises both variants. Shipping only Python silently narrows the distribution. Restore the 5 files (~38k) with a README note that they are reference implementations for TS users, not wired to run. Zero code consumer change.
**Blast radius:** +5 files, zero existing references

---

### D4 — Python test harness restoration

**File:** MISSING — `hooks/damage-control-python/test-damage-control.py` (14k upstream)
**Options:**
- (A) Restore byte-identical. Wires into `test-prompts/sentient*.md` suite (already present in ArhuGula) so the existing test prompts become runnable.
- (B) Drop. Mark SP2 feature S06 as "adversarial prompts present, automated harness absent — manual testing only."
**Architect recommendation:** **(A)** — the test-prompts are currently decorative without the runner. Restoring the harness converts SP2 feature S06 from mis-classified BUILT to actually BUILT. Low risk, high value.

---

### D5 — Installation template `python-settings.json`

**File:** MISSING — `hooks/damage-control-python/python-settings.json` (2.0k upstream)
**Options:**
- (A) Restore byte-identical. This is a reference template showing how to wire the skill hooks into a project's `.claude/settings.json`. No execution, no consumer.
- (B) Drop. Rely on the SKILL.md + cookbook for installation guidance.
**Architect recommendation:** **(A)** — zero cost, clarifies the intended installation pattern, and is the bridge between the skill and a consuming project's `settings.json`.
**Depends on:** D6 (if skill is the authoritative location, this template is referenced from there)

---

### D6 — Skill-form vs project-form hook location

**Files:**
- Skill copies: `.claude/skills/damage-control/hooks/*_damage_control.py`
- Project copies: `.claude/hooks/*_damage_control.py` (wired via `settings.json`)

**Scout finding:** the skill copies are stale (21 lines behind on bash hook). Upstream's canonical pattern is skill-only — distribution, then `python-settings.json` shows users how to wire.

**Options:**
- (A) **Skill is canonical.** Authoritative copies live at `.claude/skills/damage-control/hooks/damage-control-python/*.py`; update `settings.json` PreToolUse hooks to invoke from the skill path; delete project-level copies. Matches upstream intent exactly.
- (B) **Project is canonical.** Delete skill copies entirely (they're stale anyway); keep only the project-level copies wired via `settings.json`. Simpler live path but loses the skill's distributable nature.
- (C) **Both exist + sync mechanism.** Write a one-way sync script / CI check that ensures the skill copies match the project copies. More code, more state.
**Architect recommendation:** **(A)** — aligns with Tier 1 upstream intent (damage-control is a skill, not project hooks) AND Tier 2 intent (install globally per `INDYDEVDAN_PI_AGENT_HARNESS_SPEC.md:256-258`). This closes both sub-items of Scout top-finding #1 in one decision. Migration plan:
1. Port the 21-line delta in project bash hook → skill copy (single merge)
2. Port the 172-line patterns.yaml delta → skill copy (D8 dependency)
3. Update `settings.json` PreToolUse to point at `.claude/skills/damage-control/hooks/damage-control-python/*.py`
4. Delete project-level copies
5. Verify hooks still fire via `audits/sp2_verify.py`
**Blast radius:** very high — affects every PreToolUse invocation. Full session verification required post-commit.
**Depends on:** D1, D2, D8, D10

---

### D7 — Project-level `patterns.yaml` policy

**Files:**
- `.claude/hooks/patterns.yaml` (893 lines, 36k — live copy)
- `.claude/skills/damage-control/patterns.yaml` (721 lines, stale copy)
- Upstream (21k, 1 file at `skills/damage-control/patterns.yaml`)

**Options:**
- (A) Single authoritative copy at skill location; hooks load from skill path; delete project copy. Requires patching `load_patterns()` in all 4 hooks. Pairs with D6.
- (B) Keep two copies, establish sync via D6 path.
**Architect recommendation:** **(A)** — pairs with D6 decision. Single source of truth reduces staleness risk (which already materialized: the 172-line delta exists because the copies drifted apart).

---

### D8 — `patterns.yaml` content delta (SP14 rounds 1-10)

**Finding:** project-level patterns.yaml is 172 lines longer than the skill copy and roughly 172 lines longer than upstream. The delta captures SP14 rounds 1-10 hardening.

**Options:**
- (A) **Revert to upstream byte.** Lose SP14 hardening. Not acceptable per `feedback_disler_authoritative.md`: "drift is drift, but these memories explain *why* we drifted — not *whether* it is drift."
- (B) **Keep hardening, document as exception.** All 172 lines tracked as SP14 hardening preserved under a new Exception 14. Explicit rationale: "threat model specific to adversarial-review harness."
- (C) **Audit the 172-line delta line-by-line.** Accept rules that are general-purpose hardening; revert rules that are over-tuned or have unintended over-reach (like the `.claude/hooks/*.py` rule if D10 narrows it).
**Architect recommendation:** **(C)** — the 172 lines are not all equivalent. Some are demonstrated value (SP14 round 3 MCP namespace gate, round 4 token-sequence matching, round 10 V-3 length cap), some may be over-tuned (round 9 curl short-flag convention blocked bugs of its own per memory). A line-by-line pass identifies exactly what stays, what moves to explicit exceptions, and what reverts. This is architect+scout+build work — propose creating `audits/SP2-patterns-yaml-audit.md` as a dedicated sub-artifact.
**Blast radius:** medium (changes to patterns.yaml affect every PreToolUse call)
**Depends on:** D6, D7, D10

---

### D9 — `SKILL.md` content

**Finding:** ArhuGula SKILL.md is 138 lines describing the flat layout. Upstream is 9.0k describing the split layout + Python/TypeScript variants + installation paths.

**Options:**
- (A) Revert byte-identical to upstream. Requires D2=A (split layout) and D3=A (TS shipped) for the description to match reality.
- (B) Keep ArhuGula form, document as exception.
**Architect recommendation:** **(A) if D2+D3=A, (B) otherwise.** The SKILL.md must describe the actual layout accurately. Revert is conditional on the layout decisions.
**Depends on:** D2, D3

---

### D10 — `readOnlyPaths` rule for `.claude/hooks/*.py`

**Finding:** The rule is intentional (prevent hook modification during session). But during audit, it blocks 16 SP1 resume-pass commits that need to revert hook files to upstream.

**Options:**
- (A) **Narrow rule to security-critical hooks only.** List: `session_start.py`, `permission_request.py`, `pre_tool_use.py`, `_base.py`, `bash_damage_control.py`, `edit_damage_control.py`, `write_damage_control.py`. Non-security hooks (9 leaf reverts + utils/tts + utils/llm + setup.py + session_start.py REQUIRED_HOOKS edit) become editable. Unblocks SP1 resume pass commits 1, 2, 6, 8, 14, D4 Option C.
- (B) **Audit-scoped bypass.** Add env var `ARHUGULA_AUDIT_MODE=1` that relaxes `.claude/hooks/*.py` and `.claude/settings.json` read-only rules when set. Requires explicit flag in every audit-phase bash invocation. Closes faster but introduces a new bypass mechanism.
- (C) **Temporary rule removal for SP1 resume pass.** Comment out the rule, land the 18 commits, re-enable the rule. Requires 2 patterns.yaml edits.
- (D) **Keep rule, accept SP1 gaps.** 16 commits stay blocked permanently; SP1 round 1 never closes.
**Architect recommendation:** **(A)** — narrowest blast radius + preserves the security intent (security-critical hooks stay protected) + matches Exception 8's architecture (security-critical set already established). Zero new bypass surface. Commits to add:
1. Narrow `.claude/hooks/*.py` to the 7-file explicit list above
2. Land the 16 SP1 resume commits
3. Optional: widen back after completion (if user prefers fresh sessions to not edit any hooks)
**Per `feedback_damage_control_self_unlock.md`: explicit user authorization required.**

---

### D11 — `readOnlyPaths` rule for `.claude/settings.json`

**Finding:** The rule blocks the 3 remaining SP1 resume-pass `settings.json` edits (D1a Bash(mv:*) restore, Commit 4 statusLine revert, Commit 7 Setup hook wiring revert).

**Options:**
- (A) **Temporary removal.** Comment out the rule, land 3 commits, re-add. Lowest blast radius.
- (B) **Narrow via field-level allowlist.** Requires a more sophisticated rule engine (JSON path matching instead of file-level). Not supported by current `match_path()` — would need a new check layer.
- (C) **Audit bypass flag.** Same as D10 option B.
- (D) **Accept gap.** 3 commits stay permanently blocked.
**Architect recommendation:** **(A)** — the same pattern as D10. Land the 3 commits atomically under audit authorization, then re-enable.
**Per `feedback_damage_control_self_unlock.md`: explicit user authorization required.**

---

### D12 — Cross-clone install.md reconciliation (from ESCALATE-SP2-1)

**Finding:** `claude-code-damage-control/.claude/commands/install.md` differs from `install-and-maintain/.claude/commands/install.md` (the SP1 revert source). SP1 landed the `install-and-maintain` version; SP2 needs to decide how the damage-control-specific content lands.

**Options:**
- (A) **Merge as an extension section.** Keep SP1's `install-and-maintain` base; add a "Damage Control Installation" section at the end matching the damage-control clone's content delta. Multi-source synthesis.
- (B) **Switch base to damage-control version.** Overwrites SP1's revert. Risks losing install-and-maintain-specific content.
- (C) **Maintain two install commands.** `/install` (basic) from install-and-maintain + `/install-damage-control` (or similar) from damage-control clone.
**Architect recommendation:** **(A)** — SP1 already committed to the install-and-maintain base. Damage-control's install.md sections can be appended/merged as a damage-control-specific addition. Preserves both sources.

---

## Escalation items

### E1 — `.env.*` zeroAccessPaths over-reach (SP2-4)

The `.env.*` pattern in zeroAccessPaths uses fnmatch which matches `.env.example`. This blocks byte-comparison of `.env.example` against upstream AND would block any future Read/Write to `.env.example`.

**Resolution:** fix in D8 (line-by-line patterns.yaml audit). Add explicit allow rule for `.env.example` / `.env*.example` / `.envrc.example` (similar to existing `bashToolExclusions` line 874 pattern but at match_path level). Or introduce exclusion semantics in `match_path()` (negative patterns). Escalated to architect for choice.

---

### E2 — Global-install intent (SP6 routing)

Tier 2 (`INDYDEVDAN_PI_AGENT_HARNESS_SPEC.md:256-258`) explicitly registers damage-control as a globally-installed skill (`~/.claude/skills/damage-control/`). ArhuGula ships it per-project. This is a SP6 (Library Distribution) concern — how skills are propagated across projects vs. installed globally.

**Resolution:** Route to SP6 audit. SP2 leaves damage-control at `.claude/skills/damage-control/` per-project; SP6 decides whether to migrate to user-global.

---

### E3 — Pi curation layer + share contract (SP12 routing)

Tier 2 Pi docs describe damage-control as a CURATED subset of the Claude Code rules, not a wholesale copy. ArhuGula has no curation layer. And the Pi `damage-control.ts` extension's `patterns.yaml` share contract with SP2 is not documented.

**Resolution:** Route both to SP12 audit. SP2 leaves the wholesale-copy pattern as-is.

---

### E4 — Cross-clone prime.md 3-way disagreement (from ESCALATE-SP2-1)

`prime.md` differs between `claude-code-damage-control`, `claude-code-hooks-mastery`, and `install-and-maintain` — three-way disagreement. SP1 already tracked `prime.md` as Tier-3 audit infrastructure (Exception 1) but that classification predates this finding. The fact that upstream clones ship a prime.md means `prime.md` is NOT an ArhuGula invention — it has an upstream root.

**Resolution:** Revisit Exception 1 at a subsequent mini-gate. Route the prime.md reconciliation question separately: which clone's prime.md does ArhuGula revert against? Likely answer: hooks-mastery (the SP1 canonical source for non-install/maintenance content), with damage-control's version treated as a supplementary invocation pattern.

---

## Unblocks inventory (SP1 resume pass)

After D10 + D11 user decisions land, the following SP1 resume-pass commits unblock:

| Commit | Action | Gate blocker | Unblock path |
|---|---|---|---|
| Ex3.1 | Restore `utils/tts/*.py` (4 files) | fnmatch over-reach | Fixed by Commit 1 (AR1) |
| Ex3.2 | Restore `utils/llm/*.py` (4 files) | fnmatch over-reach | Fixed by Commit 1 (AR1) |
| Ex3.4 | Revert settings.json statusLine | .claude/settings.json exact match | D11 |
| Ex3.5 | Delete `.claude/statusline.sh` | (static analysis: not blocked) | Can land now |
| Ex3.6 | Restore setup_init.py + setup_maintenance.py | top-level `.claude/hooks/*.py` match | D10 |
| Ex3.7 | Revert settings.json Setup hook wiring | .claude/settings.json exact match | D11 |
| Ex3.8 | Delete `setup.py` | bash DELETE_PATTERNS × `.claude/hooks/*.py` | D10 |
| Ex3.9 | D1a restore `Bash(mv:*)` in settings.json | .claude/settings.json exact match | D11 |
| Ex3.14 | Purge REQUIRED_HOOKS in session_start.py | top-level `.claude/hooks/*.py` match | D10 |
| Ex3.D4-C | 9 leaf-hook reverts (notification, pre_compact, stop, subagent_*, post_tool_use, user_prompt_submit, post_tool_use_failure, session_end) | top-level `.claude/hooks/*.py` match | D10 |

**Total unblocked after SP2 gate:** 18 commits. 1 already-landable (Ex3.5 statusline.sh delete) is opportunistically bundled with Commit 4 of SP1 resume pass.

---

## Dependency graph

```
AR1 (fnmatch fix) ─┬── depends on D10 (rule narrowing for self-edit)
                   └── enables Ex3.1, Ex3.2 (subdirectory writes)

D10 (.claude/hooks/*.py rule narrowing) ──┬── enables AR1 commit
                                          ├── enables Ex3.6, Ex3.8, Ex3.14, D4-C (top-level hook edits)
                                          └── required per self-unlock memory rule

D11 (.claude/settings.json rule) ──── enables Ex3.4, Ex3.7, Ex3.9

D2 (layout) ──┬── depends on D1 (rename)
              ├── depends on D3 (TS variant scope)
              └── blocks D9 (SKILL.md content)

D6 (skill canonical) ──┬── depends on D1, D2, D8, D10
                       └── closes Scout top-finding #1

D8 (patterns.yaml audit) ──┬── depends on D6, D7, D10
                            └── closes Scout top-finding #6

AR2 (.gitkeep cleanup) — independent
AR3 (sentient.md restore) — independent
AR4 (probe expansion) — depends on AR1
```

---

## Cross-SP routing

| Item | Route to | Reason |
|---|---|---|
| Global-install intent | SP6 | Library Distribution owns skill propagation |
| Curation layer | SP12 | Pi integration owns curated subset |
| Pi-share contract | SP12 | Pi extension wires into patterns.yaml |
| prime.md 3-way disagreement | SP1 mini-gate | Cross-cuts Exception 1 |
| Subagent set expansion (from SP1 DRIFT[T2]) | SP3 | validator/reviewer archetype question |

---

## Architect recommendations summary

**Close at gate without further scouting:**
- AR1-4 (fixed by design): fnmatch fix, `.gitkeep` cleanup, sentient.md restore, probe expansion
- D1 (convention): Option B (keep underscore, exception)
- D2 (layout): Option A (restore split)
- D3 (TypeScript): Option A (restore 5 files)
- D4 (test harness): Option A (restore)
- D5 (settings template): Option A (restore)
- D9 (SKILL.md): Option A conditional on D2+D3

**Requires user decision at gate:**
- D6 (skill-canonical vs project-canonical) — architectural commitment
- D7 (patterns.yaml location) — architectural commitment (pairs with D6)
- D8 (patterns.yaml content audit) — work-scope decision (new sub-artifact?)
- D10 (hook rule narrowing) — self-unlock authorization per memory rule
- D11 (settings.json rule policy) — self-unlock authorization per memory rule
- D12 (cross-clone install.md) — content-merge call

**Route out:**
- E1 (.env.example) — ArhuGula-side patterns.yaml audit (D8 sub-item)
- E2 (global-install) — SP6
- E3 (Pi curation + share) — SP12
- E4 (prime.md) — SP1 mini-gate

---

## Artifact metadata

- **Prior state:** SP2 Phase A landed 5 commits (c04bc09..21fd4c4) resolving Ex3 item 10 + Ex4 + Ex5 + paperwork.
- **Branch:** `audit/identicality-2026-04-13` @ HEAD `21fd4c4`
- **Input:** `audits/SP2-scout.md` (classifications + 4 ESCALATE items)
- **Output:** this plan → decision gate → build phase
- **Next step:** Decision gate review of D1–D12. Recommended gate order: D10 + D11 first (unblocks AR1 and 18 SP1 commits), then D1–D5 (layout/content cluster), then D6–D9 (architectural), then D12.
- **Estimated SP2 duration:** 16 SP2 commits + 18 SP1 resume-pass commits = 34 total commits after D10+D11 authorization.
- **Memory references:** `project_sp1_r1_resume.md`, `project_sp2_architectural_gaps.md`, `feedback_damage_control_self_unlock.md`, `feedback_disler_authoritative.md`, `feedback_curl_short_flag_bundling.md` (SP14 round 9 relevant to D8).
