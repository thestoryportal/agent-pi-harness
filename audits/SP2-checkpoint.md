# SP2 Audit — Resume Checkpoint

**Date saved:** 2026-04-13 (mid-session checkpoint)
**Branch:** `audit/identicality-2026-04-13`
**Last commit:** `c693420` (SP1 Ex3.D4-C 8 leaf hook reverts)
**State:** SP2 Phase A + Phase B (AR1-4) + SP1 resume-pass COMPLETE; Phases D-I pending

---

## Resume in one paragraph

A previous session executed SP2 Phase A (rule narrowing) + Phase B (AR1-4) + the entire SP1 resume-pass (18 logical commits). All locked decisions for D1-D12 + E1-E4 are listed below. Next steps: Phase D (layout restore D1-D5+D9), Phase E (D6/D7 architectural switchover, HIGH RISK), Phase F (D8 patterns.yaml content audit + E1 fix), Phase G (D12 install.md merge), Phase H (re-tighten D10/D11 rules), Phase I (final verify). Read this file, then `audits/SP2-plan.md` for D-item detail, then proceed to Phase D.

## How to resume after `/prime`

1. Read this file (audits/SP2-checkpoint.md) — full state
2. Read audits/SP2-plan.md — D-item details and rationale (skim, not full)
3. Read audits/SP1-plan.md Appendix C — SP1 gate outcomes if cross-references needed
4. Begin Phase D (layout restore) — see "Remaining work" section

## Authorization in effect (granted by user this session)

- **D10 = Option A** + **AR1 one-shot bypass** (already used) + **narrow scope**: covers AR1 + 18 SP1 resume-pass commits ALL LANDED
- **D11 = Option A**: temporary removal of `.claude/settings.json` rule, restore at Phase H
- **D6-D9, D12, E1-E4** = architect recommendations approved en bloc by user instruction "use max thinking, find optimal solutions, implement without decision gates"
- **D8 = Option C structured audit, executed in-session** (NOT a sub-artifact gate)
- **Implicit broader auth**: user said "implement those selections" = execute all locked decisions without further per-action gates beyond D10/D11 narrow scope (which is fully consumed)

## Decisions locked (all 12 D + 4 E items resolved)

| ID | Resolution | Notes |
|---|---|---|
| D1 | (B) Keep underscore filenames as exception per CLAUDE.md §Naming | Document as exception only |
| D2 | (A) Restore upstream split layout | `damage-control-python/` + `damage-control-typescript/` |
| D3 | (A) Restore all 5 TypeScript reference files | ~38k, marked as reference impls |
| D4 | (A) Restore test-damage-control.py (14k) | Converts S06 from decorative → BUILT |
| D5 | (A) Restore python-settings.json (2.0k) | Installation template |
| D6 | (A) Skill canonical at `.claude/skills/damage-control/hooks/damage-control-python/` | Forward-compatible with SP6 |
| D7 | (A) patterns.yaml single-source at skill location | Pairs with D6 |
| D8 | (C) Structured line-by-line audit of 172-line SP14 hardening delta | Per-round attribution → Exception 14 |
| D9 | (A) SKILL.md byte-identical to upstream | Unlocked by D2+D3 approval |
| D10 | (A) Narrow `.claude/hooks/*.py` to 7-file security-critical explicit list | 7 files: session_start, permission_request, pre_tool_use, _base, bash/edit/write_damage_control |
| D11 | (A) Temporary removal during work, restore as-is at Phase H | |
| D12 | (A) Merge damage-control install.md as extension section | SP1's install-and-maintain base wins; damage-control content appends |
| E1 | Folded into D8 (add `.env*.example` pathExclusion) | Add new pathExclusions field to patterns.yaml |
| E2 | Routed to SP6 (global-install intent) | SP2 chose forward-compatible per-project skill path |
| E3 | Routed to SP12 (Pi curation + share contract) | SP2 leaves wholesale-copy as-is |
| E4 | Revisit Exception 1 at SP1 mini-gate (hooks-mastery canonical for prime.md) | |

## Commits landed this session (16 commits, 0642ec3..c693420)

### Phase A — rule narrowing (1 commit)
- `0642ec3` — SP2 Phase A: temporarily comment out `.claude/hooks/*.py` + `.claude/settings.json` from readOnlyPaths

### Phase B — AR1-AR4 (4 commits)
- `4ed10ed` — SP2 AR1: fnmatch → PurePath.match() in edit/write/pre_tool_use damage-control hooks
- `e119d81` — SP2 AR2: delete 3 .gitkeep placeholders from skill
- `b4cd745` — SP2 AR3: restore sentient.md from upstream
- `64626bc` — SP2 AR4: expand sp2_verify.py with 8 fnmatch regression cases (all empirically pass)

### Phase C — SP1 resume-pass (11 commits, 18 logical items)
- `d4aaf27` — Ex3.D4-C: post_tool_use.py revert (FIRST leaf — disables ruff+ty validators)
- `6b2ab76` — Ex3.1: utils/tts/ restore (4 files)
- `82da87f` — Ex3.2: utils/llm/ restore (4 files)
- `a48e41d` — Ex3.4: settings.json statusLine revert
- `c6f3d62` — Ex3.5: statusline.sh delete
- `04a43ba` — Ex3.6: setup_init.py + setup_maintenance.py restore
- `a80d3ab` — Ex3.7: settings.json Setup wiring revert
- `25382fb` — Ex3.8: setup.py delete
- `3f93598` — Ex3.9 (D1a): Bash(mv:*) restored to settings.json allow list
- `d9a19e2` — Ex3.14: REQUIRED_HOOKS list updated (setup.py → setup_init/maintenance)
- `c693420` — Ex3.D4-C: 8 remaining leaf hook reverts bundled (notification, pre_compact, stop, subagent_start/stop, user_prompt_submit, post_tool_use_failure, session_end)

## Critical state notes

- **patterns.yaml hook rule:** COMMENTED OUT (Phase A). Phase H must restore as 7-file explicit list (D10=A).
- **patterns.yaml settings.json rule:** COMMENTED OUT (Phase A). Phase H must restore as-is (D11=A).
- **172-line SP14 delta in patterns.yaml:** untouched. Phase F (D8 audit) addresses it.
- **post_tool_use.py:** reverted to upstream 48-line minimal form. **ruff_validator.py and ty_validator.py are no longer invoked** — file Writes/Edits skip lint/type checking. SP3 audit will need to re-implement the validator pipeline.
- **logs/ directory:** untracked, created by reverted post_tool_use.py. Add to .gitignore in Phase H.
- **Whitespace drift:** Write tool stripped trailing whitespace on blank lines for several reverted hooks. Functionally byte-identical to upstream but not literally byte-identical. Document as minor exception or accept silently.
- **Validators (ruff_validator.py, ty_validator.py):** files exist on disk under `.claude/hooks/validators/` but are dormant. Do NOT delete in SP2 — they belong to SP3 audit scope.

## Remaining work — Phases D through I

### Phase D: SP2 layout restore (D1-D5, D9)
**Goal:** damage-control skill structurally byte-identical to upstream split layout.

Steps:
1. `mkdir .claude/skills/damage-control/hooks/damage-control-python` and `damage-control-typescript`
2. Move existing `.claude/skills/damage-control/hooks/{bash,edit,write}_damage_control.py` into `damage-control-python/` (keep underscore form per D1=B; document as exception)
3. Restore 5 TS files byte-identical from upstream into `damage-control-typescript/`:
   - bash-tool-damage-control.ts, edit-tool-damage-control.ts, write-tool-damage-control.ts, test-damage-control.ts, typescript-settings.json
4. Restore `test-damage-control.py` (14k) into `damage-control-python/`
5. Restore `python-settings.json` (2.0k) into `damage-control-python/`
6. Revert `.claude/skills/damage-control/SKILL.md` byte-identical to upstream (~9.0k)

Source: `~/Projects/indydevdan-harness-research/research/full-clones/claude-code-damage-control/.claude/skills/damage-control/`

Watch out: skill's `bash/edit/write_damage_control.py` are STALE relative to project copies (21-line + 172-line drift). Either move stale ones (then Phase E syncs project content into them) OR sync first then move. Architectural cleaner: Phase E does the sync, so just move stale skill files in Phase D and let Phase E overwrite content.

### Phase E: D6/D7 architectural switchover (HIGH RISK, live session depends on hooks)
**Goal:** Skill becomes single canonical source for hooks + patterns.yaml.

3-step verifiable switchover (do NOT bundle):

**Step 1 (additive sync):**
- Copy current project `.claude/hooks/{bash,edit,write}_damage_control.py` content into `.claude/skills/damage-control/hooks/damage-control-python/{bash,edit,write}_damage_control.py` (overwrites stale skill copies from Phase D)
- Copy `.claude/hooks/patterns.yaml` content into `.claude/skills/damage-control/patterns.yaml` (overwrites stale 721-line skill copy)
- Project hooks still active. No functional change. Commit.

**Step 2 (the switch):**
- Update `.claude/settings.json` PreToolUse matchers to load hooks from skill paths:
  - `Bash` → `uv run "$CLAUDE_PROJECT_DIR"/.claude/skills/damage-control/hooks/damage-control-python/bash_damage_control.py`
  - `Edit|MultilineEdit|NotebookEdit` → `.../edit_damage_control.py`
  - `Write` → `.../write_damage_control.py`
- Patch `load_patterns()` in all 4 hook files (bash, edit, write, pre_tool_use) to load from `.claude/skills/damage-control/patterns.yaml` instead of `.claude/hooks/patterns.yaml`
- Commit. Verify next tool call succeeds (one Edit/Write/Bash should work).
- ROLLBACK PLAN: `git revert HEAD` restores both settings.json and load_patterns().

**Step 3 (cleanup):**
- Delete `.claude/hooks/{bash,edit,write}_damage_control.py` (project copies, no longer used)
- Delete `.claude/hooks/patterns.yaml` (project copy, no longer used)
- Note: `.claude/hooks/pre_tool_use.py` STAYS at the project location — it's part of the kept-as-Exception-8 set per SP1 D6 decision; it just loads patterns.yaml from the new skill path
- Commit.

### Phase F: D8 patterns.yaml content audit + E1 fix
**Goal:** Audit 172-line SP14 hardening delta, document Exception 14 with per-rule justification, fix E1.

Steps:
1. Diff `.claude/skills/damage-control/patterns.yaml` (now canonical after Phase E) against upstream `~/Projects/indydevdan-harness-research/research/full-clones/claude-code-damage-control/skills/damage-control/patterns.yaml`
2. Use `git log --follow --all .claude/hooks/patterns.yaml` (or the new skill path) to find SP14 commits that added each rule
3. For each kept rule, write Exception 14 subsection citing the SP14 round + threat scenario
4. Revert any rule known to be over-tuned/buggy (consult `feedback_curl_short_flag_bundling.md`)
5. Fix E1: add `pathExclusions` field with `.env*.example` entries; add early-exit check in `check_path()` (edit/write hooks), `check_read()` (pre_tool_use), and `_check_single_command()` (bash hook) to skip blocked paths if they match exclusions
6. Commit Exception 14 + patterns.yaml content edits

Memory references for context:
- `project_sp2_architectural_gaps.md`
- `feedback_curl_short_flag_bundling.md`
- `feedback_disler_authoritative.md`

### Phase G: D12 install.md merge
**Goal:** Merge damage-control install.md content as extension section.

Steps:
1. Read current `.claude/commands/install.md` (install-and-maintain base, landed in SP1 commit `b47306f` per SP1 plan)
2. Read upstream `~/Projects/indydevdan-harness-research/research/full-clones/claude-code-damage-control/.claude/commands/install.md`
3. Identify damage-control-specific content (likely a "Damage Control Installation" section)
4. Append/merge as a new section at the end of current install.md
5. Commit

### Phase H: Re-tighten patterns.yaml rules
**Goal:** Restore D10/D11 rules in their final form per gate decisions.

Edit `.claude/skills/damage-control/patterns.yaml` (canonical after Phase E):
1. Replace the commented-out `# - ".claude/hooks/*.py"` with explicit 7-file list per D10=A. **CRITICAL:** after Phase E, the bash/edit/write damage-control files live at `.claude/skills/damage-control/hooks/damage-control-python/`, so the 7-file list should reference THOSE skill paths, not the old project paths. Use:
   ```yaml
     - ".claude/hooks/session_start.py"
     - ".claude/hooks/permission_request.py"
     - ".claude/hooks/pre_tool_use.py"
     - ".claude/hooks/_base.py"
     - ".claude/skills/damage-control/hooks/damage-control-python/bash_damage_control.py"
     - ".claude/skills/damage-control/hooks/damage-control-python/edit_damage_control.py"
     - ".claude/skills/damage-control/hooks/damage-control-python/write_damage_control.py"
   ```
2. Uncomment `- ".claude/settings.json"` (per D11=A)
3. Add `logs/` to `.gitignore` (untracked from reverted post_tool_use.py)
4. Commit

### Phase I: Final verification
1. Run `uv run audits/sp2_verify.py` — all AR4 fnmatch regression cases should still pass
2. Verify session can start fresh: open new `claude` session, confirm session_start health check passes
3. Verify hooks load from new skill paths via a test edit
4. Update `audits/exceptions.md` with new Exception 14 entry (D8 audit) and exception entries for D1 (filename convention) + any stylistic drift
5. Update `~/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md` Section 1 to mark SP2 audit complete with date
6. Optionally archive or delete `audits/sp2_verify.py` per AR4 commit ("disposable probe")
7. Update memory: replace `project_sp2_r1_resume.md` with SP2-COMPLETE note + delete this checkpoint file

## Files-to-read at next session start (priority order)

1. **This file** — `audits/SP2-checkpoint.md`
2. `audits/SP2-plan.md` — D-item rationale (skim)
3. `audits/SP1-plan.md` Appendix C — SP1 gate outcomes (only if needed)
4. Memory entries auto-loaded via MEMORY.md:
   - `project_sp2_r1_resume.md` (will be updated to point here)
   - `project_sp2_architectural_gaps.md`
   - `feedback_damage_control_self_unlock.md`
   - `feedback_disler_authoritative.md`
   - `feedback_curl_short_flag_bundling.md`
5. `arhugula-source-of-truth.md` Section 1 (build status)

## Anti-footguns for the next session

- **Phase E Step 2 is the riskiest moment of SP2.** If the load_patterns() change has a bug, the next hook invocation fail-closes and blocks everything. Do Step 2 as a single atomic commit, verify with one tool call BEFORE Step 3 (deletion). If the verify fails, `git revert HEAD` immediately.
- **Whitespace drift on reverted hooks** is a known limitation of the Write tool. Don't waste cycles trying to achieve true byte-identicality on the leaf hook files; document as minor stylistic exception in `audits/exceptions.md` and move on.
- **The user said "implement without decision gates"** but this does NOT mean ignore `feedback_damage_control_self_unlock.md` for new authorization scenarios. The current narrow-scope authorization for D10/D11 is fully consumed. Any NEW patterns.yaml rule changes (e.g., adding new readOnlyPaths entries beyond the 7-file restoration) require fresh authorization.
- **Phase F's E1 fix touches all 4 damage-control hooks** (adds exclusion check). It does NOT touch the protected files in a way that requires bypass — patterns.yaml rules are already commented out, and Phase F runs BEFORE Phase H re-tightening.
- **Don't bundle Phase E steps.** The 3-step approach is for safety, not aesthetics.
