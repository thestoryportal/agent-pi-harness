# SP2 Audit — Scout Artifact

**Date:** 2026-04-13
**SP:** 2 — Security Hardening (damage-control)
**Phase:** Scout (audit mode, v2 two-tier methodology)
**Audit branch:** `audit/identicality-2026-04-13`
**Classification rule:** `feedback_disler_authoritative.md` — MATCH / DRIFT / MISSING only, tier-tagged

---

## Sources

**Tier 1 — byte-level authoritative**
- `~/Projects/indydevdan-harness-research/research/full-clones/claude-code-damage-control/` (pinned per `full-clones/MANIFEST.md`)

**Tier 2 — intent-level authoritative (topical)**
- `research/IndyDevDan Comprehensive/deploy_multi_agent_prompt_playbook.md` §Part 3 "Damage Control Framework" (lines 52, 118, 159)
- `research/IndyDevDan Comprehensive/indydevdan_method_comprehensive_reference.md` §Security Standards (line 240), §Damage Control row (line 309), §Part 8 install sequence (line 470), §Part 11 verification (line 482)
- `research/IndyDevDan Comprehensive/indydevdan_claude_imac_agent_blueprint.md` §Security Standards (234), §table (303), §install sequence (464)
- `research/IndyDevDan Comprehensive/indydevdan_method_claude_imac_agent_reference.md` §Security Standards (218), §install sequence (380)
- `research/IndyDevDan Comprehensive/INDYDEVDAN_PI_AGENT_HARNESS_SPEC.md` §Pi damage-control wiring (65, 178, 198, 256-258, 370, 775, 840)
- `research/IndyDevDan Comprehensive/curate_pi_harness_8f52790b.plan.md` §Pi safety policy (12, 46)

## Scope

6 SP2 features per source-of-truth §4.1:
- S01 — patterns.yaml rule engine
- S02 — Three-tier path protection (zeroAccess / readOnly / noDelete)
- S03 — Ask pattern (confirmation)
- S04 — Per-tool hook specialization (bash/edit/write)
- S05 — Distributable skill format
- S06 — Test prompt suites

**SP2 files under audit:**
- `.claude/skills/damage-control/SKILL.md`
- `.claude/skills/damage-control/patterns.yaml`
- `.claude/skills/damage-control/hooks/bash_damage_control.py`
- `.claude/skills/damage-control/hooks/edit_damage_control.py`
- `.claude/skills/damage-control/hooks/write_damage_control.py`
- `.claude/skills/damage-control/cookbook/*.md` (6 files)
- `.claude/skills/damage-control/test-prompts/*.md` (6 files)
- `.claude/hooks/bash_damage_control.py` (project-level deployed copy)
- `.claude/hooks/edit_damage_control.py` (project-level deployed copy)
- `.claude/hooks/write_damage_control.py` (project-level deployed copy)
- `.claude/hooks/patterns.yaml` (project-level deployed copy)
- `.claude/settings.json` PreToolUse wiring to damage-control hooks (SP2-relevant subset)

**Explicitly out of scope** (routed to other SPs):
- Non-damage-control hooks in `.claude/hooks/` → SP1 (`_base.py`, `session_*`, `pre_tool_use.py`, etc.)
- `.claude/commands/install.md`, `prime.md`, `sentient.md` shipped inside `claude-code-damage-control/.claude/commands/` — see ESCALATE-SP2-1 (cross-clone command overlap)
- `apps/`, `agents/sfa/` — other SPs
- Generic `permission_request.py` allowlist (SP1 Exception 8)

---

## Tier 1 — Byte-level diff vs `claude-code-damage-control` full-clone

### Skill-form files (`.claude/skills/damage-control/`)

**MATCH:** none.

**DRIFT[T1] — byte-differs AND path/filename-differs** (5 files):

| ArhuGula path | Upstream path | Delta |
|---|---|---|
| `.claude/skills/damage-control/SKILL.md` | `claude-code-damage-control/.claude/skills/damage-control/SKILL.md` | 138 lines vs 9.0k upstream — ArhuGula SKILL.md describes a flat `hooks/{bash,edit,write}_damage_control.py` layout; upstream describes `hooks/damage-control-python/` + `hooks/damage-control-typescript/` split with 5 files per variant. Section headers, cookbook/testing descriptions byte-differ. |
| `.claude/skills/damage-control/patterns.yaml` | `…/damage-control/patterns.yaml` | 721 lines vs 21k upstream. Structural format match (zeroAccessPaths / readOnlyPaths / noDeletePaths / bashToolPatterns / bashToolExclusions sections) but content bytes differ. Fine-grained diff deferred to architect phase. |
| `.claude/skills/damage-control/hooks/bash_damage_control.py` | `…/hooks/damage-control-python/bash-tool-damage-control.py` | 365 lines / 13k vs 11k upstream. **Path and filename both diverge**: upstream has `damage-control-python/` subdirectory + hyphen-separated basename. ArhuGula flattens to `hooks/` and uses underscore basename. |
| `.claude/skills/damage-control/hooks/edit_damage_control.py` | `…/hooks/damage-control-python/edit-tool-damage-control.py` | 165 lines / 6.0k vs 4.4k upstream. Same path/filename drift. |
| `.claude/skills/damage-control/hooks/write_damage_control.py` | `…/hooks/damage-control-python/write-tool-damage-control.py` | 181 lines / 6.6k vs 4.4k upstream. Same path/filename drift. |

**DRIFT[T1] — invention** (files in ArhuGula skill with no upstream counterpart):
- `.claude/skills/damage-control/hooks/.gitkeep` — ArhuGula-only
- `.claude/skills/damage-control/cookbook/.gitkeep` — ArhuGula-only
- `.claude/skills/damage-control/test-prompts/.gitkeep` — ArhuGula-only

**MATCH[T1] — cookbook and test-prompts bodies** (12 files, byte-identical after excluding `.gitkeep` placeholders):
- `.claude/skills/damage-control/cookbook/build_for_windows.md`
- `.claude/skills/damage-control/cookbook/install_damage_control_ag_workflow.md`
- `.claude/skills/damage-control/cookbook/list_damage_controls.md`
- `.claude/skills/damage-control/cookbook/manual_control_damage_control_ag_workflow.md`
- `.claude/skills/damage-control/cookbook/modify_damage_control_ag_workflow.md`
- `.claude/skills/damage-control/cookbook/test_damage_control.md`
- `.claude/skills/damage-control/test-prompts/README.md`
- `.claude/skills/damage-control/test-prompts/sentient.md`
- `.claude/skills/damage-control/test-prompts/sentient_v1.md`
- `.claude/skills/damage-control/test-prompts/sentient_v2.md`
- `.claude/skills/damage-control/test-prompts/sentient_v3.md`
- `.claude/skills/damage-control/test-prompts/sentient_v4.md`

These 12 files are confirmed `diff -rq` MATCH and constitute the only SP2 MATCH set.

**MISSING[T1]** — files present upstream, absent in ArhuGula (7 files):

*damage-control-python subdirectory (Python reference implementation):*
- `…/hooks/damage-control-python/python-settings.json` (2.0k) — installation template showing how to wire skill hooks into `.claude/settings.json`
- `…/hooks/damage-control-python/test-damage-control.py` (14k) — Python test harness for validating the hooks

*damage-control-typescript subdirectory (Bun/TypeScript reference implementation) — entire tree missing:*
- `…/hooks/damage-control-typescript/bash-tool-damage-control.ts` (12k)
- `…/hooks/damage-control-typescript/edit-tool-damage-control.ts` (4.7k)
- `…/hooks/damage-control-typescript/write-tool-damage-control.ts` (4.7k)
- `…/hooks/damage-control-typescript/test-damage-control.ts` (15k)
- `…/hooks/damage-control-typescript/typescript-settings.json` (2.0k)

Total missing: ~55k of upstream distributable content (2 subdirectories, 7 files).

### Project-form files (`.claude/hooks/`)

**MATCH:** none — no Tier-1 reference exists for any of these paths.

**DRIFT[T1] — invention** (4 files, project-level copies with no upstream counterpart anywhere in the damage-control clone):

| File | Size | Notes |
|---|---:|---|
| `.claude/hooks/bash_damage_control.py` | 386 lines / 14k | Upstream has no project-level copy; skill copy lives at `damage-control-python/bash-tool-damage-control.py`. ArhuGula's project copy is **21 lines larger than its own skill copy** — internal divergence. |
| `.claude/hooks/edit_damage_control.py` | 165 lines / 6.0k | No upstream project-level copy. Byte-identical to skill copy. |
| `.claude/hooks/write_damage_control.py` | 181 lines / 6.6k | No upstream project-level copy. Byte-identical to skill copy. |
| `.claude/hooks/patterns.yaml` | 893 lines / 36k | No upstream project-level copy; skill has it at `.claude/skills/damage-control/patterns.yaml`. ArhuGula's project copy is **172 lines larger than its own skill copy** — internal divergence. Captures SP14 rounds 1–10 hardening additions. |

**Intra-ArhuGula staleness finding:** the skill-form and project-form copies have diverged. `bash_damage_control.py` and `patterns.yaml` differ between skill and project; `edit_damage_control.py` and `write_damage_control.py` match. The skill copies are stale relative to the deployed project copies. The skill is meant to be the "distributable single source of truth" per upstream SKILL.md §Skill Structure, but ArhuGula's skill copy is not the source of truth in practice.

### Tier 1 Summary

| Bucket | Count |
|---|---:|
| MATCH[T1] | 12 (cookbook + test-prompts bodies only) |
| DRIFT[T1] — skill-form byte modifications with path/filename drift | 5 (SKILL.md, patterns.yaml, 3 hooks) |
| DRIFT[T1] — project-form inventions (no upstream counterpart) | 4 (3 hooks + patterns.yaml at `.claude/hooks/`) |
| DRIFT[T1] — inventions (tree placeholders) | 3 (`.gitkeep` files) |
| MISSING[T1] — upstream files absent locally | 7 (Python: 2; TypeScript: 5) |
| Intra-ArhuGula staleness | 2 (bash hook + patterns.yaml skill copy stale vs project copy) |

### Top Tier-1 findings

1. **Upstream ships damage-control as a pure skill; ArhuGula duplicates it at project level.** Upstream's entire damage-control payload lives under `.claude/skills/damage-control/` with `python-settings.json` as an installation template. ArhuGula copied the Python hook bodies into project-level `.claude/hooks/` and wired them directly in `.claude/settings.json`, while also keeping (stale) copies inside the skill. This is the core architectural drift for SP2.
2. **Upstream ships a TypeScript reference implementation; ArhuGula ships zero TypeScript.** 5 files totaling ~38k of `damage-control-typescript/` content are MISSING[T1]. No ArhuGula counterpart. No decision gate entry exists for whether ArhuGula should ship both variants or only Python.
3. **Upstream ships two test harnesses (`test-damage-control.py` 14k, `test-damage-control.ts` 15k); ArhuGula ships none.** SP2 feature S06 claims test-prompt suites as BUILT, but the `test-prompts/*.md` files are adversarial prompts used to validate the hooks interactively — the runnable harness that actually executes them is missing.
4. **Filename convention drift**: upstream uses `bash-tool-damage-control.py` / `edit-tool-damage-control.py` / `write-tool-damage-control.py`. ArhuGula renamed to `bash_damage_control.py` / etc. Per project CLAUDE.md naming convention, hook files use underscores, so ArhuGula's rename is **internally consistent** — but still DRIFT from Tier-1 byte-identicality. Decision-gate item.
5. **Directory layout drift**: upstream splits implementations into `hooks/damage-control-python/` + `hooks/damage-control-typescript/`. ArhuGula flattens to `hooks/` and drops the language-variant segregation. Decision-gate item.
6. **ArhuGula's skill copy is stale relative to the deployed project copy.** `bash_damage_control.py` skill copy is 21 lines behind; `patterns.yaml` skill copy is 172 lines behind. The skill is supposed to be the distributable source of truth per SKILL.md §Skill Structure, but SP14 rounds 1–10 hardening landed only in the project copy. Either the skill is dead code, or it needs to be kept in sync. Decision-gate item.

---

## Tier 2 — Intent diff vs Comprehensive docs

### Philosophy / installation intent

**MATCH[T2]:**
- PreToolUse defense-in-depth principle — `comprehensive_reference:309` lists damage-control under "PreToolUse | Defense-in-depth". ArhuGula wires all three damage-control hooks on PreToolUse per `.claude/settings.json`.
- Ask patterns (exit 0 with `permissionDecision:ask` JSON) match `deploy_multi_agent_prompt_playbook.md:118` "Damage Control Hooks" section describing the three-tier block/ask/allow model.
- patterns.yaml as single source of truth for rules matches `INDYDEVDAN_PI_AGENT_HARNESS_SPEC.md:65` ("damage-control-rules.yaml — Security patterns, same format as Claude Code") and :178 ("Teams, agents, tools, themes, damage-control rules — all declarative").

**DRIFT[T2]:**
- `comprehensive_reference:470` + `blueprint:464` + `reference:380` describe the installation sequence as: "Install Damage Control hooks from repo" (i.e., from cloned `disler/claude-code-damage-control`) **AND** separately "Create `.claude/hooks/pre_tool_use.py`" as a second hook. ArhuGula merged both into the damage-control hook set (three files) and DOES have a separate `pre_tool_use.py` — but ArhuGula's `pre_tool_use.py` is coupled to `patterns.yaml` via `_base.py`, which is an invention. Upstream's intent is that damage-control hooks and the project pre-tool hook are **independent**.
- `INDYDEVDAN_PI_AGENT_HARNESS_SPEC.md:256-258` registers damage-control as a **cloned-and-installed-globally** skill (source URL: `disler/claude-code-damage-control/.../SKILL.md`) — i.e., the intent is that `~/.claude/skills/damage-control/` holds the skill and projects reference it via skill registry. ArhuGula copies the skill into per-project `.claude/skills/damage-control/` instead of treating the user-global `~/.claude/skills/` as the canonical location. DRIFT from "installed globally" intent.
- `comprehensive_reference:240` / `blueprint:234` / `reference:218` describe "Security Standards (Damage Control)" as a layered policy. ArhuGula's layering is functionally correct (three tiers matching upstream) but the policy content is ArhuGula-specific (SP14 round 1–10 additions absent from upstream doc's listed patterns).

**MISSING[T2]:**
- `curate_pi_harness_8f52790b.plan.md:46` describes a **curated** damage-control policy for Pi ("curated from the reference repo rather than copied wholesale"). ArhuGula has no curation layer — project-level `patterns.yaml` is an ad-hoc accumulation, not a curated subset. (SP12 concern, routed.)
- `INDYDEVDAN_PI_AGENT_HARNESS_SPEC.md:198` describes `damage-control.ts` (Pi extension) reading the **same** patterns.yaml format as Claude Code. SP12 Pi extension exists in ArhuGula, but the pattern-file share contract with SP2 is not tested or documented.

### Tier 2 Summary

| Bucket | Count |
|---|---:|
| MATCH[T2] | 3 (defense-in-depth, ask-pattern model, patterns.yaml contract) |
| DRIFT[T2] | 3 (pre_tool_use.py separation, global-install vs per-project, policy content expansion) |
| MISSING[T2] | 2 (curation layer, Pi-share contract documentation) |

### Top Tier-2 findings

1. **Upstream intent is "install globally" via `~/.claude/skills/damage-control/`.** ArhuGula copies the skill per-project. Decision-gate item: adopt global-install intent, or document the per-project deviation.
2. **Upstream treats `pre_tool_use.py` as independent from damage-control hooks.** ArhuGula couples them via shared `patterns.yaml` loading. SP1 Exception 8 already holds `pre_tool_use.py` as drift; SP2 should document the intent separation explicitly.
3. **No curation layer.** Tier 2 (Pi spec) explicitly asks for a curated policy, not wholesale copy. ArhuGula ships wholesale copy + 172-line SP14 addendum. Route curation work to SP12.

---

## Cross-tier reconciliation

### Items flagged by both tiers (T1 revert first, then T2 fix)

1. **Skill vs project duplication of hook bodies** — DRIFT[T1] (no upstream project-level copy) AND DRIFT[T2] (upstream intent is install globally into `~/.claude/skills/`). Single architectural fix: move the skill to `~/.claude/skills/damage-control/`, drop `.claude/hooks/*_damage_control.py` project copies, wire `settings.json` hooks to reference the global skill path. Blast radius: every damage-control hook invocation path + settings.json PreToolUse block.
2. **patterns.yaml dual copy** — DRIFT[T1] (project copy is invention) AND DRIFT[T2] (should be curated subset, not wholesale copy). Fix: maintain one copy at skill location, drop the `.claude/hooks/patterns.yaml` copy, update hook `load_patterns()` to point at the skill path.

### T2-only gaps

1. Curation layer — SP12 scope
2. Pi-share contract documentation — SP12 scope

### Routing recommendations for architect

**SP2-owned AUTO-REVERTs (high confidence, no conflict):**
- Restore upstream `damage-control-python/` subdirectory layout with hyphen-separated filenames (5 files: bash/edit/write hooks, python-settings.json, test-damage-control.py)
- Restore upstream `damage-control-typescript/` tree (5 files) — or escalate as "does ArhuGula ship both variants?"
- Drop ArhuGula `.gitkeep` placeholders (3 files)
- Revert SKILL.md to upstream byte (describes the upstream directory layout; ArhuGula's flat layout becomes invalid)
- Revert skill-form `patterns.yaml` to upstream byte

**SP2-owned DECISION-REQUIRED (conflicts with SP14 hardening / deployed state):**
- Project-level `.claude/hooks/{bash,edit,write}_damage_control.py` copies: delete, or keep as deployed-copy exception
- Project-level `.claude/hooks/patterns.yaml` copy: delete (use skill copy via updated path), or keep as exception-7 extension
- 21 extra lines in project `bash_damage_control.py` vs skill copy: port to skill copy (sync) or drop (revert)
- 172 extra lines in project `patterns.yaml` vs skill copy: port to skill copy (sync), drop (revert), or preserve as documented hardening delta
- Adopt upstream hyphen filename convention, or keep ArhuGula underscore convention as naming-convention exception
- Flatten vs two-variant `damage-control-python/` + `-typescript/` layout
- Ship TypeScript implementation (5 files) or document as language-variant exception (Python-only)

**Route to other SPs:**
- Curated Pi policy — SP12
- pre_tool_use.py independence — SP1 Exception 8 stays
- Global-install intent — SP6 (Library Distribution) + SP2 joint

**ESCALATE to user at decision gate:**
- ESCALATE-SP2-1 — Cross-clone command overlap (see below)
- ESCALATE-SP2-2 — fnmatch over-reach bug (see below)
- ESCALATE-SP2-3 — `.claude/commands/` / `.claude/agents/` over-restriction assumption (see below)

---

## Structural findings (SP1 resume-pass blockers)

### ESCALATE-SP2-2 — fnmatch over-reach in `readOnlyPaths`

`.claude/hooks/patterns.yaml` line 754 declares:

```yaml
readOnlyPaths:
  ...
  - ".claude/hooks/*.py"
  - ".claude/settings.json"
```

`edit_damage_control.py:62-82` (`match_path()`) and the equivalent in `write_damage_control.py` use Python's `fnmatch.fnmatch()` against the normalized and expanded path. `fnmatch` does **not** treat `/` as a path separator — `*` matches any character including `/`. Result: the rule `.claude/hooks/*.py` matches `.claude/hooks/utils/tts/elevenlabs_tts.py`, `.claude/hooks/utils/llm/anth.py`, etc., because the single `*` greedily consumes `utils/tts/elevenlabs_tts`.

**Impact on SP1 resume pass (11 blocked commits per Exception 3):**
- Commits 1, 2 (restore `utils/tts/*.py` + `utils/llm/*.py` trees) — **confirmed blocked** by this rule; Write tool → `write_damage_control.py` → `match_path` → fnmatch returns True on the nested .py paths.
- Commits 4, 7 (settings.json reverts) — blocked by the separate `.claude/settings.json` rule, not by fnmatch.
- Commits 5, 8 (statusline.sh deletion, setup.py deletion) — blocked by the `.claude/hooks/*.py` rule extended by fnmatch to cover both files (setup.py at top level, statusline.sh matches `.sh` not `.py` — actually `.claude/statusline.sh` would NOT match `.claude/hooks/*.py`). Needs architect-phase empirical verification.
- Commit 6 (restore `setup_init.py` + `setup_maintenance.py`) — blocked by `.claude/hooks/*.py` at top level.
- Commit 14 (purge `REQUIRED_HOOKS` in `session_start.py`) — blocked by `.claude/hooks/*.py`.
- D4 Option C leaf-hook reverts (9 files in `.claude/hooks/*.py`) — blocked.

**Fix options (architect phase):**
- **Option A — patterns.yaml narrowing.** Replace `.claude/hooks/*.py` with two explicit rules: one for the top-level damage-control hooks (keep), and leave `_base.py` + sub-tree files unprotected. Trade-off: loses blanket protection for new top-level hooks.
- **Option B — hook code fix.** Modify `match_path()` to use `pathlib.PurePath.match()` or `fnmatch.filter()` on path segments, which DO treat `/` as a separator. This is the more correct fix.
- **Option C — replace glob with explicit file list.** Enumerate the 16 top-level `.claude/hooks/*.py` files by name. Ugly but unambiguous.

Cross-references:
- Memory: `project_sp2_architectural_gaps.md` — already documents this as a P0 SP2 follow-up
- `audits/SP1-plan.md` — Exception 3 blast radius

### ESCALATE-SP2-3 — Over-restriction assumption for `.claude/commands/` and `.claude/agents/`

**STATUS: RESOLVED 2026-04-13 (SP2 Phase A).** Empirical verification via `audits/sp2_verify.py` confirmed neither path is in any restricted-path tier. All three blocked operations landed as atomic commits: D3 maintenance.md revert (`c04bc09`), Exception 4 builder.md move (`36bac66`) + validator.md move (`7fd0f3c`), Exception 5 invention deletion (`9ed2995`). Original finding preserved below for audit trail.

---


`audits/exceptions.md` Exception 3 (item 10 — D3 maintenance.md revert) and Exception 4 (builder.md/validator.md move) both assert these operations are "blocked because `.claude/commands/` / `.claude/agents/` is expected to be in `readOnlyPaths`". Scout grep of `.claude/hooks/patterns.yaml` finds **neither path in `readOnlyPaths`, `zeroAccessPaths`, or `noDeletePaths`**:

```
readOnlyPaths entries matching /.claude/:
  - ".claude/hooks/*.py"
  - ".claude/settings.json"

zeroAccessPaths entries matching /.claude/:
  - ".claude/logs/"

noDeletePaths entries matching /.claude/:
  - ~/.claude/
  - CLAUDE.md
```

Neither `.claude/commands/` nor `.claude/agents/` is in any restricted path list. The SP1 plan's assertion that these operations "are expected to be blocked" was based on extrapolation from the blocks observed on `.claude/hooks/` and `.claude/settings.json`, not empirical verification.

**Scout finding:** D3 (maintenance.md content revert), Exception 4 (builder.md/validator.md `git mv` + content revert), and Exception 5 (spec-checker.md/schema-reviewer.md deletion) may **not be blocked** at the patterns.yaml layer. Architect phase must verify empirically. If unblocked, three of the SP1 resume-pass items can land without waiting for SP2 fixes.

Caveat: `bash_damage_control.py` may have additional bash-level checks for `git mv` or `rm` on `.claude/` paths that would still block Exception 4/5 via a different mechanism. Not verified in scout.

### ESCALATE-SP2-4 — `.env.example` block (confirming SP1 ESCALATE-T1 E1)

`.claude/hooks/patterns.yaml:621` declares `".env.*"` in `zeroAccessPaths`. Via fnmatch, this pattern matches `.env.example` (the `*` greedily matches "example"). This explains why SP1 scout was blocked from byte-diffing `.env.example` against the upstream `install-and-maintain` version. Fix options:
- Add `.env.example` to the `bashToolExclusions` allowlist (line 874 already allows `\bcat\s+\.env\.example`, but this is bash-level only; Edit/Write tools bypass this).
- Narrow `.env.*` to exclude `*.example` suffix — requires zeroAccessPaths exclusion semantics not currently supported.
- Add explicit allow rule in `match_path()`.

Cross-references: SP1 scout ESCALATE-T1 E1, now resolved as SP1 Exception 9 (confirmed invention). Exception 9's "confirmed no upstream" finding is actually correct, but the block reason is verified as this zeroAccessPaths rule.

### ESCALATE-SP2-1 — Cross-clone command overlap

`claude-code-damage-control/.claude/commands/` ships three files OUTSIDE the skill directory:
- `install.md` — differs from `install-and-maintain/.claude/commands/install.md` (the canonical SP1 source for install.md)
- `prime.md` — differs from both `install-and-maintain/.claude/commands/prime.md` AND `claude-code-hooks-mastery/` (which has no install.md but has prime.md at a different location)
- `sentient.md` (1.1k) — damage-control-unique, adversarial test-prompt launcher

**Conflict with SP1:** SP1 audit reverted `install.md` to `install-and-maintain` byte (commit `b47306f`). SP2 upstream (damage-control) has a **different** `install.md`. Under the Disler-authoritative rule, which clone wins when multiple clones ship the same-named file?

**Scout resolution proposal:** The SP2-relevant command is the **damage-control-specific** content in install.md — i.e., the portion that installs damage-control hooks. The SP1 revert kept only the `install-and-maintain` base. The damage-control-unique content should be **merged** into the install sequence as a damage-control installation step, not replace the SP1 revert. Architect phase must extract the damage-control delta from `claude-code-damage-control/install.md` vs `install-and-maintain/install.md` and route it into SP2 as an extension.

**`sentient.md` is MISSING[T1]**: ArhuGula has no `.claude/commands/sentient.md`. Upstream ships this 1.1k file as an adversarial test-launcher that references the `test-prompts/sentient*.md` suite. Since ArhuGula ships the test-prompts but not the launcher command, the test prompts cannot be invoked via the documented workflow. Route to SP2 AUTO-REVERT: restore upstream `sentient.md`.

### SP2 structural summary

| ID | Finding | Tier | Impact |
|---|---|---|---|
| ESCALATE-SP2-1 | Cross-clone command overlap (install.md, prime.md, sentient.md) | T1 | Decision gate — merge damage-control delta into SP1 base + restore sentient.md |
| ESCALATE-SP2-2 | fnmatch over-reach in readOnlyPaths | T1 | Code fix (Option B preferred) — unblocks 11 SP1 resume commits |
| ESCALATE-SP2-3 | `.claude/commands/` / `.claude/agents/` over-restriction assumption | T1 | Architect verify — may unblock SP1 D3 + Exception 4 + Exception 5 without code fix |
| ESCALATE-SP2-4 | `.env.example` zeroAccessPaths block | T1 | Confirms SP1 ESCALATE-T1 E1; resolution = allowlist semantics extension |

---

## Artifact metadata

- **Prior state:** SP1 round 1 decision gate + mini-gate closed (commits 98c658c, 3b72fb1, fe23e4c). All SP1 paperwork final; 11 resume-pass commits blocked on SP2 scout → architect → build → verify.
- **Branch:** `audit/identicality-2026-04-13` @ HEAD 98c658c
- **Tier 1 clone:** `~/Projects/indydevdan-harness-research/research/full-clones/claude-code-damage-control/` (pinned 2026-04-13 per `full-clones/MANIFEST.md`)
- **Out-of-scope deferrals routed to:** SP12 (Pi curation layer, share contract), SP6 (global-install intent), SP1 (`pre_tool_use.py` stays Exception 8)
- **Next phase:** Architect — consume this scout + SP1-plan.md Appendix C to produce SP2-plan.md with AUTO-REVERT + DECISION-REQUIRED + ESCALATE classifications.
- **Related memory entries:** `project_sp2_architectural_gaps.md`, `feedback_damage_control_self_unlock.md`, `feedback_disler_authoritative.md`, `project_sp1_r1_resume.md`
