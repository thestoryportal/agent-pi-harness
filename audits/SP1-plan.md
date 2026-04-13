# SP1 Audit — Revert Plan

**Date:** 2026-04-13
**SP:** 1 — CC Harness
**Phase:** Architect (audit mode, v2 methodology)
**Input:** `audits/SP1-scout.md`
**Audit branch:** `audit/identicality-2026-04-13`

## Summary

| Classification | Commit count | File touches |
|---|---:|---:|
| AUTO-REVERT | 11 | 25 |
| DECISION-REQUIRED | 7 | 21 |
| ESCALATE | 8 | 11 |

**Estimated total commits:** 18 (AUTO-REVERT + DECISION-REQUIRED, pending user gate decisions)

---

## Commit plan (dependency-ordered)

### Commit 1 — Restore utils/tts/ tree (4 files)

- **Classification:** AUTO-REVERT
- **Tier:** T1
- **Action:** Copy the four TTS utility files verbatim from upstream hooks-mastery into `.claude/hooks/utils/tts/`. No ArhuGula file is removed; this is purely additive.
- **Files touched:**
  - `.claude/hooks/utils/tts/elevenlabs_tts.py` — create
  - `.claude/hooks/utils/tts/openai_tts.py` — create
  - `.claude/hooks/utils/tts/pyttsx3_tts.py` — create
  - `.claude/hooks/utils/tts/tts_queue.py` — create
- **Upstream source:** `~/Projects/indydevdan-harness-research/research/full-clones/claude-code-hooks-mastery/.claude/hooks/utils/tts/`
- **Blast radius:** isolated (new files only, no consumers yet)
- **Depends on:** (none)
- **Rollback:** `git revert <commit-sha>` (standard)
- **Commit message:** `audit: SP1 — restore utils/tts/ tree from hooks-mastery`

---

### Commit 2 — Restore utils/llm/ tree (4 files)

- **Classification:** AUTO-REVERT
- **Tier:** T1
- **Action:** Copy the four LLM utility files verbatim from upstream hooks-mastery into `.claude/hooks/utils/llm/`. Purely additive.
- **Files touched:**
  - `.claude/hooks/utils/llm/anth.py` — create
  - `.claude/hooks/utils/llm/oai.py` — create
  - `.claude/hooks/utils/llm/ollama.py` — create
  - `.claude/hooks/utils/llm/task_summarizer.py` — create
- **Upstream source:** `~/Projects/indydevdan-harness-research/research/full-clones/claude-code-hooks-mastery/.claude/hooks/utils/llm/`
- **Blast radius:** isolated (new files only)
- **Depends on:** (none)
- **Rollback:** `git revert <commit-sha>` (standard)
- **Commit message:** `audit: SP1 — restore utils/llm/ tree from hooks-mastery`

---

### Commit 3 — Restore status_lines/ tree

- **Classification:** AUTO-REVERT
- **Tier:** T1
- **Action:** Copy `status_line_v6.py` and the full `status_lines/` versioned directory from upstream into `.claude/status_lines/`. This creates the upstream Python status line. Do NOT yet change `settings.json`; that follows in Commit 4. The `.claude/statusline.sh` ArhuGula invention is removed only after settings.json is updated (Commit 5).
- **Files touched:**
  - `.claude/status_lines/status_line_v6.py` — create
  - `.claude/status_lines/status_line_v7.py` — create (if present upstream)
  - `.claude/status_lines/status_line_v8.py` — create (if present upstream)
  - `.claude/status_lines/status_line_v9.py` — create (if present upstream)
- **Upstream source:** `~/Projects/indydevdan-harness-research/research/full-clones/claude-code-hooks-mastery/.claude/status_lines/`
- **Blast radius:** isolated (new files, settings still points at statusline.sh)
- **Depends on:** (none)
- **Rollback:** `git revert <commit-sha>` (standard)
- **Commit message:** `audit: SP1 — restore status_lines/ tree from hooks-mastery`

---

### Commit 4 — Revert settings.json statusLine to upstream Python form

- **Classification:** AUTO-REVERT (statusLine only; the permission allow-list drift is handled separately in D1)
- **Tier:** T1
- **Action:** Change the `statusLine` block in `.claude/settings.json` from `bash "$CLAUDE_PROJECT_DIR"/.claude/statusline.sh` back to the upstream `uv run`-based Python invocation pointing at `status_line_v6.py`. This commit touches ONLY the `statusLine` key.
- **Files touched:**
  - `.claude/settings.json` — modify (statusLine block only)
- **Upstream source:** `~/Projects/indydevdan-harness-research/research/full-clones/claude-code-hooks-mastery/.claude/settings.json` (statusLine block)
- **Blast radius:** hooks-wide (statusLine runs every tick; wrong path = blank status bar)
- **Depends on:** Commit 3 (`status_line_v6.py` must exist before settings.json points to it)
- **Rollback:** `git revert <commit-sha>` (standard)
- **Commit message:** `audit: SP1 — revert settings.json statusLine to upstream Python form`

---

### Commit 5 — Delete .claude/statusline.sh (ArhuGula invention)

- **Classification:** AUTO-REVERT
- **Tier:** T1
- **Action:** Delete `.claude/statusline.sh`. No upstream equivalent; ArhuGula-invented bash wrapper replaced by Python status line now restored.
- **Files touched:**
  - `.claude/statusline.sh` — delete
- **Upstream source:** N/A (deletion of invention)
- **Blast radius:** isolated (settings.json already updated in Commit 4 to not reference it)
- **Depends on:** Commit 4 (settings.json must no longer reference this file before it is deleted)
- **Rollback:** `git revert <commit-sha>` (standard)
- **Commit message:** `audit: SP1 — delete .claude/statusline.sh (ArhuGula invention, no upstream)`

---

### Commit 6 — Restore setup_init.py and setup_maintenance.py from install-and-maintain

- **Classification:** AUTO-REVERT
- **Tier:** T1
- **Action:** Copy `setup_init.py` (183 lines) and `setup_maintenance.py` (117 lines) verbatim from upstream install-and-maintain into `.claude/hooks/`. Do NOT yet delete ArhuGula's `setup.py`; that follows in Commit 8 after settings.json wiring is updated.
- **Files touched:**
  - `.claude/hooks/setup_init.py` — create
  - `.claude/hooks/setup_maintenance.py` — create
- **Upstream source:** `~/Projects/indydevdan-harness-research/research/full-clones/install-and-maintain/.claude/hooks/`
- **Blast radius:** isolated (new files; setup.py still present and wired)
- **Depends on:** (none)
- **Rollback:** `git revert <commit-sha>` (standard)
- **Commit message:** `audit: SP1 — restore setup_init.py + setup_maintenance.py from install-and-maintain`

---

### Commit 7 — Revert settings.json Setup hook wiring to init/maintenance matchers

- **Classification:** AUTO-REVERT (Setup block only; SP2 damage-control wiring handled in D2)
- **Tier:** T1
- **Action:** Replace the single `Setup` entry (pointing to `setup.py`) in `.claude/settings.json` with the upstream two-entry matcher pattern from install-and-maintain: `matcher: "init"` → `setup_init.py` and `matcher: "maintenance"` → `setup_maintenance.py`. **Do not** touch the PreToolUse damage-control matchers in this commit — those are D2's scope.
- **Files touched:**
  - `.claude/settings.json` — modify (Setup block only)
- **Upstream source:** `~/Projects/indydevdan-harness-research/research/full-clones/install-and-maintain/.claude/settings.json` (Setup block)
- **Blast radius:** hooks-wide (Setup hook routing changes)
- **Depends on:** Commit 6 (`setup_init.py` and `setup_maintenance.py` must exist before settings.json routes to them)
- **Rollback:** `git revert <commit-sha>` (standard)
- **Commit message:** `audit: SP1 — revert settings.json Setup hook wiring to init/maintenance matchers`

---

### Commit 8 — Delete setup.py (ArhuGula consolidation, replaced by init/maintenance split)

- **Classification:** AUTO-REVERT
- **Tier:** T1
- **Action:** Delete `.claude/hooks/setup.py`. Upstream has `setup_init.py` + `setup_maintenance.py`; ArhuGula consolidated both into `setup.py` (95L vs upstream's 300L combined). Settings.json no longer wires to it after Commit 7.
- **Files touched:**
  - `.claude/hooks/setup.py` — delete
- **Upstream source:** N/A (deletion; replacements already committed in Commit 6)
- **Blast radius:** isolated (no settings.json reference remains after Commit 7)
- **Depends on:** Commit 7 (settings.json must not reference setup.py before deletion)
- **Rollback:** `git revert <commit-sha>` (standard)
- **Commit message:** `audit: SP1 — delete setup.py (replaced by upstream init/maintenance split)`

---

### Commit 9 — Restore install-hil.md from install-and-maintain

- **Classification:** AUTO-REVERT
- **Tier:** T1
- **Action:** Copy `install-hil.md` verbatim from upstream install-and-maintain into `.claude/commands/`. Hardware-in-the-loop install variant, purely additive.
- **Files touched:**
  - `.claude/commands/install-hil.md` — create
- **Upstream source:** `~/Projects/indydevdan-harness-research/research/full-clones/install-and-maintain/.claude/commands/install-hil.md`
- **Blast radius:** isolated (new file)
- **Depends on:** (none)
- **Rollback:** `git revert <commit-sha>` (standard)
- **Commit message:** `audit: SP1 — restore install-hil.md from install-and-maintain`

---

### Commit 10 — Rename maintain.md to maintenance.md (upstream filename)

- **Classification:** AUTO-REVERT
- **Tier:** T1
- **Action:** `git mv .claude/commands/maintain.md .claude/commands/maintenance.md`. Upstream filename is `maintenance.md`; ArhuGula renamed it to `maintain.md`. Content delta is a separate DECISION-REQUIRED item (D3) that will modify the file after the rename is committed.
- **Files touched:**
  - `.claude/commands/maintain.md` → `.claude/commands/maintenance.md` — rename
- **Upstream source:** `~/Projects/indydevdan-harness-research/research/full-clones/install-and-maintain/.claude/commands/maintenance.md`
- **Blast radius:** isolated (any reference to `maintain.md` in the justfile must also be updated; see Commit 11)
- **Depends on:** (none)
- **Rollback:** `git revert <commit-sha>` (standard)
- **Commit message:** `audit: SP1 — rename maintain.md → maintenance.md (upstream filename)`

---

### Commit 11 — Update justfile references from maintain.md to maintenance.md

- **Classification:** AUTO-REVERT
- **Tier:** T1
- **Action:** Find all `just maintain` / `maintain.md` references in the justfile and update them to `maintenance` / `maintenance.md` to match the renamed command file.
- **Files touched:**
  - `justfile` — modify (command name references only)
- **Upstream source:** N/A (consequence of Commit 10)
- **Blast radius:** isolated (justfile recipe wiring only)
- **Depends on:** Commit 10 (rename must precede reference updates)
- **Rollback:** `git revert <commit-sha>` (standard)
- **Commit message:** `audit: SP1 — update justfile references to renamed maintenance.md`

---

### Commit 12 — Revert install.md to upstream (drop SP4/SP8/SP13 scope creep)

- **Classification:** AUTO-REVERT
- **Tier:** T1
- **Action:** Replace `.claude/commands/install.md` with the upstream version from install-and-maintain. The ArhuGula version forward-loads Playwright, Pi-agent, and Swift checks (SP4/SP8/SP13 content) into the SP1 install command. Those checks belong in their respective SPs' install extensions, not the base SP1 install command.
- **Files touched:**
  - `.claude/commands/install.md` — modify (replace with upstream content)
- **Upstream source:** `~/Projects/indydevdan-harness-research/research/full-clones/install-and-maintain/.claude/commands/install.md`
- **Blast radius:** isolated (command file; no other files depend on its content)
- **Depends on:** (none)
- **Rollback:** `git revert <commit-sha>` (standard)
- **Commit message:** `audit: SP1 — revert install.md to upstream (remove SP4/SP8/SP13 scope creep)`

---

### Commit 13 — Revert build.md to upstream hooks-mastery form

- **Classification:** AUTO-REVERT
- **Tier:** T1
- **Action:** Replace `.claude/commands/build.md` with the upstream version from hooks-mastery. Structural content delta between ArhuGula and upstream.
- **Files touched:**
  - `.claude/commands/build.md` — modify (replace with upstream content)
- **Upstream source:** `~/Projects/indydevdan-harness-research/research/full-clones/claude-code-hooks-mastery/.claude/commands/build.md`
- **Blast radius:** isolated
- **Depends on:** (none)
- **Rollback:** `git revert <commit-sha>` (standard)
- **Commit message:** `audit: SP1 — revert build.md to upstream hooks-mastery form`

---

### Commit 14 — Purge future-SP validators from session_start.py REQUIRED_HOOKS

- **Classification:** AUTO-REVERT
- **Tier:** T2
- **Action:** Edit `.claude/hooks/session_start.py` to remove SP3/SP14 validator references (`ruff_validator.py`, `ty_validator.py`) from the `REQUIRED_HOOKS` list. These are not SP1 hooks; their inclusion causes false-negative health check failures on a fresh clone before SP3 ships. Remove only the future-SP entries; do not touch the rest of the health check logic (which is DECISION-REQUIRED for `_base.py` removal).
- **Files touched:**
  - `.claude/hooks/session_start.py` — modify (REQUIRED_HOOKS list only)
- **Upstream source:** N/A (T2 intent fix; no byte-for-byte upstream reference for this specific list)
- **Blast radius:** isolated (health check scope only)
- **Depends on:** (none) — this is a contained list edit independent of the `_base.py` question
- **Rollback:** `git revert <commit-sha>` (standard)
- **Commit message:** `audit: SP1 — purge SP3/SP14 validators from session_start REQUIRED_HOOKS`

---

## Decision gate items

### D1 — Revert settings.json extended Bash permission allow-list

- **Proposed action:** Remove the additional Bash allow entries that ArhuGula added beyond the upstream set: `Bash(brew:*)`, `Bash(tmux:*)`, `Bash(just:*)`, `Bash(yq:*)`, `Bash(node:*)`, `Bash(xcode-select:*)`, `Bash(which:*)`, `Bash(test:*)`, `Bash(cat:*)`, `Skill`. Upstream `claude-code-hooks-mastery/settings.json` allows: `mkdir`, `uv`, `find`, `mv`, `grep`, `npm`, `ls`, `cp`, `Write`, `Edit`, `chmod`, `touch`. Also note upstream has `Bash(mv:*)` which ArhuGula dropped.
- **Memory conflict:** `feedback_disler_authoritative.md`: "When auditing, use exactly three buckets: MATCH, DRIFT, MISSING. There is no 'intentional delta' / 'ArhuGula hardening' / 'ArhuGula adaptation' classification. Drift is drift regardless of rationale."
  `feedback_damage_control_self_unlock.md`: "When any damage-control hook blocks a tool call, treat the block as a hard stop." — reverting the allow-list does NOT conflict with damage-control (damage-control operates via hook patterns, not via settings.json allow entries). No direct memory conflict on the allow-list itself beyond the audit rule.
- **Trade-off:** Reverting to the minimal upstream allow-list means `just`, `brew`, `tmux`, `yq`, `node`, `cat`, `which`, `test`, `xcode-select` would all require user permission clicks during ArhuGula sessions. These tools are used in nearly every ArhuGula workflow (`just` especially). If kept, ArhuGula diverges from upstream for documented convenience. If reverted, the harness is byte-identical but more friction-heavy at runtime. Upstream also has `Bash(mv:*)` which ArhuGula dropped — that must be restored regardless.
- **Recommendation:** Split into two actions: **(a)** AUTO-REVERT restore `Bash(mv:*)` which was dropped from upstream — no trade-off. **(b)** DECISION by user: revert the nine ArhuGula additions or keep as explicit exception. If kept as exception, document in `audits/exceptions.md` with rationale.
- **If approved to revert:** Inserts as Commit 4b immediately after Commit 4 — modify settings.json permissions block to exactly match upstream hooks-mastery list.
- **If kept as exception:** Add a new file `audits/exceptions.md` documenting the nine extra Bash permissions as an ArhuGula deviation with rationale.

---

### D2 — Remove SP2 damage-control hook wiring from settings.json PreToolUse

- **Proposed action:** Remove the three SP2-owned PreToolUse matchers from `.claude/settings.json` that wire `bash_damage_control.py`, `edit_damage_control.py`, and `write_damage_control.py`. These are SP2 scope (not in upstream hooks-mastery). Upstream settings.json has a single empty-matcher PreToolUse entry.
- **Memory conflict:** `feedback_damage_control_self_unlock.md`: "When any damage-control hook blocks a tool call, treat the block as a hard stop. Do NOT edit `patterns.yaml` to remove entries... unless the user explicitly authorizes that specific unlock-and-edit action in the current turn."
  `project_sp2_architectural_gaps.md`: "the hooks are the security foundation everything else depends on, so these should be addressed before any future sub-project relies on the hook layer as a trustworthy boundary."
- **Trade-off:** The SP2 damage-control hooks are registered in `settings.json`. Removing the wiring disables SP2 protections for the duration of the audit branch — patterns.yaml rules stop being enforced, `readOnlyPaths` / `zeroAccessPaths` / `noDeletePaths` become inoperative. The audit branch is not production, but unregistering damage-control while editing sensitive hook files is exactly the risk scenario the memory warns about. Reverting is the correct audit posture per `feedback_disler_authoritative.md`, but the security cost is real.
- **Recommendation:** **Keep SP2 wiring in settings.json as a documented exception during the audit.** After the audit branch merges, a separate SP2 audit will handle SP2 scope. Add a comment in settings.json explaining the deviation. Do NOT revert this during SP1 audit.
- **If approved to revert:** Inserts as Commit 7a (before Commit 7 setup wiring). Remove the three damage-control PreToolUse matchers and replace with upstream's single empty-matcher form.
- **If kept as exception:** Note in `audits/exceptions.md`: "settings.json PreToolUse damage-control wiring kept from SP2 to preserve security protections during audit; will be audited under SP2 scope."

---

### D3 — Revert maintenance.md content to upstream

- **Proposed action:** After the rename in Commit 10, replace the content of `maintenance.md` with the upstream install-and-maintain `maintenance.md` content. The current content has structural delta beyond just the filename difference.
- **Memory conflict:** None directly. However, the justfile (40+ recipes) may reference internal sections or headings of the maintenance command. Content revert could break those references.
- **Trade-off:** Upstream `maintenance.md` is scoped to a minimal install-and-maintain workflow. ArhuGula's version may contain ArhuGula-specific maintenance steps. Full revert to upstream content drops any ArhuGula-specific maintenance instructions that may not exist elsewhere.
- **Recommendation:** Revert to upstream content. Any ArhuGula-specific maintenance steps that are genuinely needed should be added as a separate `maintenance-local.md` extension (following the IndyDevDan extension pattern) rather than modifying the base command. This keeps the base byte-identical and adds local extensions separately.
- **If approved to revert:** Inserts as Commit 10b immediately after Commit 10. Replace maintenance.md content with upstream verbatim.
- **If kept as exception:** Document in `audits/exceptions.md`.

---

### D4 — Revert all 13 core hooks to upstream form (remove _base.py coupling)

**HIGHEST-IMPACT ITEM — ARCHITECT RECOMMENDS ESCALATE.**

- **Proposed action:** Replace each of the 13 `.claude/hooks/*.py` files with their upstream counterparts from hooks-mastery. Delete `.claude/hooks/_base.py`. This removes: `Logger`, `emit_event`, `handle_health_check`, `read_stdin`, `run_hook` helpers; `ARHUGULA_SESSION_ID` env var injection; `.env` whitelist/denylist with INJECT marker; structured JSONL event logging from every hook.
- **Memory conflict:** `feedback_disler_authoritative.md`: "hook `_base.py` helper; `setup.py` consolidation..." is explicitly listed as a known drift item.
  Counter-pressure from `project_sp2_architectural_gaps.md`: "the hooks are the security foundation everything else depends on."
- **Trade-off:** This is the highest blast-radius item in the plan. Reverting removes the entire observability infrastructure (JSONL event logging, session IDs, structured payloads). The upstream hooks-mastery hooks are minimal — e.g., `stop.py` uses random completion messages, `pre_tool_use.py` only detects `rm -rf`, `permission_request.py` has no `ALLOWED_TOOLS` gate. Reverting would also lose the `.env` secret denylist in `session_start.py` and the `ALLOWED_TOOLS`/`ALLOWED_BASH_PREFIXES` stricter allowlist in `permission_request.py`. Blast radius is system-wide — every hook changes simultaneously. This also disables the `ARHUGULA_SESSION_ID` that other tooling may depend on.
- **Recommendation:** **ESCALATE to user.** This single item touches 14 files, eliminates all observability, and weakens the permission model. It should be a separate, explicit user decision rather than batched with other reverts. If approved, must be done as its own atomic group of commits (one per hook file + one for `_base.py` deletion) so each is independently revertable. Sequencing: revert leaf hooks first (`notification`, `pre_compact`, `subagent_start`, `subagent_stop`, `session_end`, `stop`, `user_prompt_submit`, `post_tool_use`, `post_tool_use_failure`), then security-critical hooks (`permission_request`, `pre_tool_use`), then `session_start` last (it orchestrates the health check), then delete `_base.py`.
- **If approved to revert:** Inserts as Commits 15–28 (one per hook + `_base.py`). All depend on D2 resolution since damage-control hooks interact with `pre_tool_use`.
- **If kept as exception:** Document `_base.py` and all 13 hook modifications in `audits/exceptions.md` with rationale per tier.

---

### D5 — Revert permission_request.py ALLOWED_TOOLS / ALLOWED_BASH_PREFIXES stricter allowlist

- **Proposed action:** Revert `permission_request.py` to upstream form (from hooks-mastery), removing the ArhuGula-added `ALLOWED_TOOLS` and `ALLOWED_BASH_PREFIXES` stricter allowlist. Upstream `permission_request.py` runs with `--log-only` flag.
- **Memory conflict:** `feedback_disler_authoritative.md`: `ALLOWED_TOOLS` allowlist in `permission_request.py` is explicitly named as a known drift item. Removing it reduces the permission gate.
- **Trade-off:** This is a sub-item of D4. The `ALLOWED_TOOLS` gate is part of the `_base.py`-coupled architecture. If D4 is approved (full hook revert), this automatically resolves. If D4 is kept-as-exception, this item must be decided independently. Either revert `permission_request.py` individually to upstream's `--log-only` form, or keep the strict allowlist as a documented exception.
- **Recommendation:** **Defer to D4 decision.** If D4 is kept-as-exception, keep this as a named exception in `audits/exceptions.md`. If D4 is approved, this is covered.
- **If approved independently:** Inserts between leaf hooks and security hooks in the D4 commit sequence.
- **If kept as exception:** Named entry in `audits/exceptions.md`.

---

### D6 — Revert pre_tool_use.py patterns.yaml loading (zeroAccessPaths + MCP namespace gates)

- **Proposed action:** Revert `pre_tool_use.py` to upstream form (upstream only detects `rm -rf`). The ArhuGula version loads `patterns.yaml` to enforce `zeroAccessPaths` and gate all `mcp__*` namespace tool calls.
- **Memory conflict:** `project_sp2_architectural_gaps.md`: "Grep/Glob walks into zeroAccessPaths files via ripgrep... The hook never sees the files ripgrep actually opens — it only checks the target directory."
  `feedback_damage_control_self_unlock.md`: "treat the block as a hard stop." Reverting `pre_tool_use.py` eliminates the zeroAccessPaths check entirely, which is worse than the existing gap.
- **Trade-off:** The SP2 architectural gap is that zeroAccessPaths only checks the path argument, not what ripgrep walks into. Reverting `pre_tool_use.py` to upstream's `rm -rf`-only detection completely removes that check. This would be a regression below even the current gapped state.
- **Recommendation:** **Keep as documented exception, regardless of D4 decision.** The upstream `pre_tool_use.py` is weaker than ArhuGula's even with its known gap. Document as exception in `audits/exceptions.md` with explicit rationale: "pre_tool_use.py kept in ArhuGula form; upstream's rm-rf-only detection is insufficient and would be a security regression."
- **If approved to revert:** Part of D4 commit sequence. Inserts in security-critical hook group.
- **If kept as exception:** Named entry in `audits/exceptions.md` (recommended path).

---

### D7 — Delete package.json and .tool-versions (ArhuGula inventions)

- **Proposed action:** Delete `package.json` and `.tool-versions`. Neither upstream (hooks-mastery nor install-and-maintain) ships these files. They are ArhuGula inventions with no upstream equivalent.
- **Memory conflict:** No direct memory conflict. No hardening memory covers these files.
- **Trade-off:** `package.json` may declare Node.js dependencies used by later SPs or scripts. `.tool-versions` pins tool versions via asdf/mise — removing it allows version drift. Both are scaffolding files that may have been added for genuine operational reasons (e.g., node version pinning for SP14 Playwright). Deletion is safe only if no justfile recipe or hook depends on the content of these files.
- **Recommendation:** Revert both if no SP-owned code references them. Builder agent should verify with `grep -r "package.json\|.tool-versions" justfile .claude/` before executing. If references exist, escalate.
- **If approved to revert:** Inserts as Commit 14b (after Commit 14, leaf files, low blast radius).
- **If kept as exception:** Document in `audits/exceptions.md`.

---

## Escalation items

### E1 — 6 core subagent definitions have no SP1 upstream reference

- **Scout finding:** `.claude/agents/builder.md`, `validator.md`, `spec-checker.md`, `schema-reviewer.md`, `architect.md`, `scout-agent.md` are absent from both SP1 upstream repos (hooks-mastery and install-and-maintain). Candidate source: `agentic-finance-review` (SP3).
- **Why it's escalated:** Architect cannot route these without locating the source repo. If they originate in `agentic-finance-review` (SP3 scope), then the SP1 audit should note them as "SP3-sourced" and leave them in place; they are not SP1 drift. If they have no upstream source, they are ArhuGula inventions and must be deleted. `builder.md` and `validator.md` DO exist in upstream hooks-mastery under `agents/team/` subdirectory — those two can be AUTO-REVERT compared, but the other four have no T1 reference.
- **Options:**
  1. Route to SP3 audit: assume these belong to SP3 scope (`agentic-finance-review`). Leave in place pending SP3 audit.
  2. Treat all 6 as inventions: delete all, including `builder.md` and `validator.md` (which have upstream counterparts under `agents/team/` subdirectory vs ArhuGula's flat `agents/` placement).
  3. Partial: auto-match `builder.md` + `validator.md` against upstream `agents/team/` equivalents; escalate the other 4 as inventions.
- **Recommended next step:** Run a targeted scout on the `agentic-finance-review` full-clone for `spec-checker.md`, `schema-reviewer.md`, `architect.md`, `scout-agent.md`. If found, route to SP3. If not found in any full-clone, classify as inventions and delete.

---

### E2 — 3 commands have no SP1 upstream reference (harness-review.md, architect.md, migrate.md)

- **Scout finding:** `.claude/commands/harness-review.md`, `.claude/commands/architect.md`, `.claude/commands/migrate.md` are absent from both SP1 upstream repos. May trace to another Disler repo.
- **Why it's escalated:** These commands are load-bearing for the ArhuGula development workflow (`just build`, `just harness-review`, etc.). Deleting them breaks the four-layer architecture. Attribution must be confirmed before action.
- **Options:**
  1. Route to SP3 attribution search (same as E1).
  2. Classify as ArhuGula inventions. Document in `audits/exceptions.md` as pipeline workflow commands with no upstream byte source.
  3. Defer: keep in place during SP1 audit, address when the relevant SP's audit runs.
- **Recommended next step:** Search all full-clones for these filenames before deciding. The orchestrator can run this as a targeted grep across `research/full-clones/`.

---

### E3 — 2 skills have no SP1 upstream reference (prime/SKILL.md, scout/SKILL.md)

- **Scout finding:** `.claude/skills/prime/SKILL.md` and `.claude/skills/scout/SKILL.md` are absent from both SP1 upstream repos.
- **Why it's escalated:** These are the meta-level skill definitions for two core pipeline commands. No Disler full-clone shows a `skills/` directory with `SKILL.md` files in this form. This may be a T2-only feature or an ArhuGula invention.
- **Options:**
  1. Classify as ArhuGula inventions, delete, and document in exceptions.
  2. Defer to SP5/SP6 attribution search (skills might be sourced there).
  3. Keep as T2-only feature: the comprehensive docs reference skills but no T1 clone implements the `SKILL.md` format.
- **Recommended next step:** Search the-library and pocket-pick full-clones for the `SKILL.md` convention. If not found anywhere, classify as invention.

---

### E4 — .env.example byte comparison blocked (damage-control hook during scout)

- **Scout finding:** Scout could not complete byte-level comparison of `.env.example` because the damage-control hook blocked the Read tool during the scan.
- **Why it's escalated:** Without seeing the file content, architect cannot determine whether it is MATCH, DRIFT, or MISSING relative to upstream. The upstream repos may or may not ship `.env.example`.
- **Options:**
  1. User manually diffs `.env.example` against upstream equivalents and provides the result before the builder runs.
  2. Builder agent skips `.env.example` during execution and flags it as a manual-verification item in the post-plan state.
  3. The user temporarily authorizes one-shot Read of `.env.example` per `feedback_damage_control_self_unlock.md` procedure, scout re-scans, architect updates this item.
- **Recommended next step:** **Option 3** — one-shot user-authorized Read of `.env.example` by the scout agent, then this escalation resolves. Option 1 is also acceptable.

---

### E5 — scripts/run-claude.py scope routing (SP1 vs SP12)

- **Scout finding:** `scripts/run-claude.py` is attributed to SP12 (`claude-code-is-programmable`) in the MANIFEST but is physically present in ArhuGula at SP1 scaffolding time.
- **Why it's escalated:** If this is SP12 scope, the SP1 audit should note it as "out of scope" and leave it for the SP12 audit. If the SP1 source-of-truth entry for "programmatic wrapper" is wrong and this really belongs in SP12, the source-of-truth must be updated.
- **Options:**
  1. Route to SP12 audit scope. Note in SP1 audit as "SP12-owned file, excluded from SP1 findings."
  2. Keep in SP1 scope. Find a T1 byte reference in install-and-maintain or hooks-mastery.
  3. Classify as ArhuGula invention at SP1 level (no T1 reference for a Python runner script in either SP1 repo).
- **Recommended next step:** **Option 1** — route to SP12. Most likely correct answer.

---

### E6 — fork-terminal skill (T2-only, no T1 reference)

- **Scout finding:** `fork-terminal` skill is referenced in `comprehensive_reference §Part 5 Category 1` as a core skill for spawning parallel agents. Not present in any full-clone.
- **Why it's escalated:** Architect cannot build from T2 description alone per methodology rules. No byte reference exists.
- **Options:**
  1. Build from T2 description. Classify as T2-only feature, implement what the docs describe.
  2. Defer as known gap. Record in `audits/exceptions.md` as "T2-only, no T1 byte source, deferred."
  3. User locates the feature in an unlisted Disler repo and provides T1 reference.
- **Recommended next step:** **Option 2** — defer. If a T1 source is later found, this becomes AUTO-REVERT.

---

### E7 — pocket-pick local skill registration (T2-only, SP5 boundary)

- **Scout finding:** `comprehensive_reference §Part 1, Part 8 Phase 4` references pocket-pick MCP local registration. Global skill exists per `feedback_library_global.md`; not locally registered in `.claude/skills/`.
- **Why it's escalated:** SP5 owns the pocket-pick implementation. SP1 is asked to "stub the local contract" but architect cannot define what that stub looks like without T1 reference.
- **Options:**
  1. Defer entirely to SP5 audit.
  2. Create a placeholder registration file documenting the interface.
  3. No action — the global registration per `feedback_library_global.md` is the correct state.
- **Recommended next step:** **Option 1** — defer to SP5 audit. Note in SP1 post-plan state.

---

### E8 — dashboard event streamer + /scout-plan-build composable wrapper (T2-only)

- **Scout finding:** `comprehensive_reference §Part 3 Principle 9` references a dashboard consumer for JSONL events. `comprehensive_reference §Part 5 Category 1` references a composable `/scout-plan-build` skill wrapper. Neither is present in any full-clone.
- **Why it's escalated:** Both are T2-only items. No T1 byte source. If D4 (hook revert) is approved, even the JSONL emitter stub disappears.
- **Options:**
  1. Defer both as T2-only gaps. Record in post-plan state.
  2. Build from T2 description only.
  3. If D4 is kept-as-exception (hooks stay), stub the dashboard consumer interface as a no-op file.
- **Recommended next step:** **Option 1** — defer both. The dashboard is likely SP9 scope; the composable wrapper may be SP3 scope. Surface in those SP audits.

---

## Cross-reference to scout findings

| Scout finding | Scout bucket | Plan item | Status |
|---|---|---|---|
| utils/tts/ (4 files) | MISSING[T1] | Commit 1 | AUTO-REVERT |
| utils/llm/ (4 files) | MISSING[T1] | Commit 2 | AUTO-REVERT |
| status_lines/ tree | MISSING[T1] | Commit 3 | AUTO-REVERT |
| statusLine settings.json (Python form) | DRIFT[T1] | Commit 4 | AUTO-REVERT |
| .claude/statusline.sh invention | DRIFT[T1] | Commit 5 | AUTO-REVERT |
| setup_init.py + setup_maintenance.py | MISSING[T1] | Commit 6 | AUTO-REVERT |
| settings.json Setup hook wiring | DRIFT[T1] | Commit 7 | AUTO-REVERT |
| setup.py consolidation | DRIFT[T1] | Commit 8 | AUTO-REVERT |
| install-hil.md | MISSING[T1] | Commit 9 | AUTO-REVERT |
| maintain.md → maintenance.md rename | DRIFT[T1] | Commit 10 | AUTO-REVERT |
| justfile maintenance references | DRIFT[T1] | Commit 11 | AUTO-REVERT |
| install.md forward-loads later SPs | DRIFT[T1] | Commit 12 | AUTO-REVERT |
| build.md structural delta | DRIFT[T1] | Commit 13 | AUTO-REVERT |
| REQUIRED_HOOKS future-SP validators | DRIFT[T2] | Commit 14 | AUTO-REVERT |
| settings.json extended Bash allow-list | DRIFT[T1] | D1 | DECISION-REQUIRED |
| SP2 damage-control wiring in settings.json | DRIFT[T1] | D2 | DECISION-REQUIRED |
| maintenance.md content delta | DRIFT[T1] | D3 | DECISION-REQUIRED |
| _base.py + 13 hook modifications | DRIFT[T1] | D4 | DECISION-REQUIRED (ARCHITECT RECOMMENDS ESCALATE) |
| permission_request.py ALLOWED_TOOLS | DRIFT[T1] | D5 | DECISION-REQUIRED (subsumed by D4) |
| pre_tool_use.py patterns.yaml loading | DRIFT[T1] | D6 | DECISION-REQUIRED (recommend keep-as-exception) |
| package.json invention | DRIFT[T1] | D7 | DECISION-REQUIRED |
| .tool-versions invention | DRIFT[T1] | D7 | DECISION-REQUIRED |
| 6 core subagent definitions | ESCALATE-T1 | E1 | ESCALATE |
| harness-review.md, architect.md, migrate.md | ESCALATE-T1 | E2 | ESCALATE |
| prime/SKILL.md, scout/SKILL.md | ESCALATE-T1 | E3 | ESCALATE |
| .env.example (scan blocked) | ESCALATE-T1 | E4 | ESCALATE |
| scripts/run-claude.py scope | ESCALATE-T1 | E5 | ESCALATE |
| fork-terminal skill | MISSING[T2-only] | E6 | ESCALATE |
| pocket-pick local registration | MISSING[T2-only] | E7 | ESCALATE |
| dashboard streamer + /scout-plan-build | DRIFT[T2] / MISSING[T2-only] | E8 | ESCALATE |
| CLAUDE.md comprehensive doc vs 0-byte stub | DRIFT[T1] | (deferred — see note) | DECISION-REQUIRED |
| justfile 40+ recipes vs minimal upstream | DRIFT[T1] | (deferred — see note) | DECISION-REQUIRED |

**Note on CLAUDE.md and justfile:** These two items appear in the scout DRIFT[T1] list but are not assigned a commit above. Both are load-bearing infrastructure with massive blast radius. CLAUDE.md is the project's operational bible; reverting to a 0-byte stub would break all implementation rules. The justfile's 40+ recipes represent months of SP1–SP14 accumulated workflow. These should be treated as user-decision items added to D4's decision gate: "Revert CLAUDE.md to 0-byte stub and justfile to 1.0k minimal form?" They are almost certainly intended as documented exceptions per the identicality audit, but the user must confirm.

---

## Post-plan state

After all 14 AUTO-REVERT commits execute (Commits 1–14):

- **Tier 1 parity:** approximately 45% of T1 findings closed (7 of 16 DRIFT[T1] modifications addressed + 6 of 11 MISSING[T1] files restored)
- **Tier 2 parity:** approximately 30% of T2 findings closed (1 of 9 DRIFT[T2] items + 0 of 5 MISSING[T2/T2-only])
- **Remaining gaps (AUTO-REVERT complete, DECISION-REQUIRED pending):**
  - `_base.py` + 13 hooks (D4) — largest remaining gap
  - settings.json allow-list (D1)
  - SP2 wiring in settings.json (D2)
  - maintenance.md content (D3)
  - permission_request.py (D5, subsumed by D4)
  - pre_tool_use.py (D6)
  - package.json + .tool-versions (D7)
  - CLAUDE.md + justfile (deferred, see note above)
  - 8 ESCALATE items (E1–E8)

**If all DECISION-REQUIRED items are approved as reverts (optimistic path):** Tier 1 parity rises to approximately 85%. Remaining 15% is the 8 ESCALATE items (no T1 source found yet).

**If all DECISION-REQUIRED items are kept as documented exceptions:** Tier 1 parity stays at approximately 45% by file count but the documented exceptions are intentional and auditable.

---

## Verify phase input (for phase 5)

Scout agent will re-audit using this plan's post-state. Expected new state after AUTO-REVERTs:

- **MATCH:** ~8 new MATCH items (tts/, llm/, status_lines/, setup_init.py, setup_maintenance.py, install-hil.md, maintenance.md rename, install.md)
- **Remaining DRIFT/MISSING:** ~21 items (7 from DECISION-REQUIRED pending, 8 ESCALATE, CLAUDE.md, justfile, .env.example)
- **Gate items for user decision before builder runs:** D1, D2, D3, D4, D5, D6, D7 + CLAUDE.md/justfile exception decision + 8 ESCALATE routing decisions (E1–E8)

---

## Appendix A — Deferred commits (blocked by SP2 fnmatch gap)

**Decision date:** 2026-04-13
**Decision:** User chose Option 2 — execute unblocked commits only; defer the rest to SP2 audit.

### Root cause

`.claude/hooks/patterns.yaml` has `".claude/hooks/*.py"` in `readOnlyPaths`. Python's `fnmatch.fnmatch()` does not treat `/` as a special character, so `*` matches directory separators. The pattern therefore matches both top-level hook files (intended) **and** any `.py` file in subdirectories (unintended over-reach). This is the same class of bug as the SP14 round-3 finding and is already documented in `project_sp2_architectural_gaps.md` as a P0 SP2 follow-up.

### Blocked commits (6 of 14)

| # | Action | Block reason |
|---|---|---|
| 1 | Restore `utils/tts/*.py` (4 files) | fnmatch over-reach (unintended) |
| 2 | Restore `utils/llm/*.py` (4 files) | fnmatch over-reach (unintended) |
| 6 | Create `setup_init.py` + `setup_maintenance.py` | readOnlyPaths (intended — new files in hooks/) |
| 7 | Edit settings.json Setup wiring | depends on 6 |
| 8 | Delete `setup.py` | depends on 7; possibly `noDeletePaths` |
| 14 | Edit `session_start.py` `REQUIRED_HOOKS` | readOnlyPaths (intended — edit of existing hook) |

### Resolution path

1. SP2 audit scout phase re-discovers this bug (already in memory `project_sp2_architectural_gaps.md`).
2. SP2 architect phase proposes `patterns.yaml` narrowing or `write_damage_control.py` path-matching fix.
3. SP2 build phase executes the fix.
4. After SP2 patterns fix lands, a **SP1 resume pass** re-runs these 6 deferred commits against the fixed rules.
5. SP1 audit remains **partially complete** (8/14 AUTO-REVERT + all DECISION-REQUIRED + all ESCALATE unresolved) until SP2 closes.

### Implications for SP1 state tracking

- SP1 verify phase (phase 5) after this AUTO-REVERT round will NOT see the blocked items close.
- Post-plan Tier 1 parity estimate revised: after 8 commits, approximately 25% of T1 findings closed (down from 45% in the original plan).
- The blocked items stay in `audits/SP1-scout.md` as open DRIFT/MISSING items until SP2 audit resolution.

---

## Appendix B — Unblocked commit subset (8 commits, executing now)

Commits **3, 4, 5, 9, 10, 11, 12, 13** execute as the "Option 2" subset.

### Dependencies within the subset

- Chain C: 3 → 4 → 5 (status_lines restore → settings.json statusLine revert → delete statusline.sh)
- Chain F: 10 → 11 (maintain→maintenance rename → justfile refs update)
- Standalone: 9 (install-hil.md), 12 (install.md revert), 13 (build.md revert)

### Execution order

3, 4, 5, 9, 10, 11, 12, 13 — unchanged from the original plan ordering. No re-sequencing needed; the dropped commits were either independent additions (1, 2) or their own self-contained dependency chain (6 → 7 → 8) + a standalone edit (14).
