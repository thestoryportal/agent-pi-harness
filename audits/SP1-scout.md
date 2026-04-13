# SP1 Audit — Scout Artifact

**Date:** 2026-04-13
**SP:** 1 — CC Harness
**Phase:** Scout (audit mode, v2 two-tier methodology)
**Audit branch:** `audit/identicality-2026-04-13`
**Classification rule:** `feedback_disler_authoritative.md` — MATCH / DRIFT / MISSING only, tier-tagged

---

## Sources

**Tier 1 — byte-level authoritative**
- `~/Projects/indydevdan-harness-research/research/full-clones/claude-code-hooks-mastery/` @ `052ad1c`
- `~/Projects/indydevdan-harness-research/research/full-clones/install-and-maintain/` @ `558b5c8`

**Tier 2 — intent-level authoritative (universal docs, all SPs)**
- `research/IndyDevDan Comprehensive/indydevdan_method_comprehensive_reference.md` (746 lines)
- `research/IndyDevDan Comprehensive/indydevdan_claude_imac_agent_blueprint.md` (585 lines)
- `research/IndyDevDan Comprehensive/indydevdan_method_claude_imac_agent_reference.md` (445 lines)

**Tier 2 — topical:** (none — SP1 has no topical mapping)

## Scope

40 SP1 features: scaffolding (10), hook system (18), core commands (7), core subagents (4), library catalog (1), programmatic wrapper (3).

**Explicitly out of scope** (handled by other SPs, excluded from findings):
- Damage-control hooks `bash_damage_control.py`, `edit_damage_control.py`, `write_damage_control.py` → SP2
- `patterns.yaml` → SP2
- Agents `meta-agent.md`, `security.md`, `bowser-qa-agent.md`, `playwright-bowser-agent.md`, `claude-bowser-agent.md` → SP3/SP13/SP14
- Skills `damage-control/`, `steer/`, `playwright-bowser/`, `claude-bowser/` → other SPs
- `apps/` directory → SP7/SP8/SP10/SP13
- `agents/sfa/` → SP7
- Commands `bowser/*`, `ui-review.md`, `device-control.md` → SP13/SP14

---

## Tier 1 — Byte-level diff vs full-clones

### Hooks (`.claude/hooks/`)

**MATCH:** none — every SP1 hook diverges structurally from upstream.

**DRIFT[T1] — hook modifications** (13 items):
- `.claude/hooks/session_start.py` vs upstream: imports `_base.py`, adds `ARHUGULA_SESSION_ID` env var, adds `.env` whitelist with INJECT marker + secret denylist, structured JSONL event logging. Upstream is minimal.
- `.claude/hooks/session_end.py` vs upstream: `_base.py` imports, uuid/timezone handling, structured event logging
- `.claude/hooks/setup.py` vs upstream: consolidated from upstream's two separate files (see MISSING below); `_base.py`-coupled
- `.claude/hooks/user_prompt_submit.py` vs upstream: `_base.py`, detailed event logging
- `.claude/hooks/pre_tool_use.py` vs upstream: loads `patterns.yaml` for `zeroAccessPaths` + all `mcp__*` namespace gates; upstream only detects `rm -rf`
- `.claude/hooks/post_tool_use.py` vs upstream: `_base.py`-based event emission
- `.claude/hooks/post_tool_use_failure.py` vs upstream: `_base.py`, error tracking
- `.claude/hooks/subagent_start.py` vs upstream: `_base.py`, event emission
- `.claude/hooks/subagent_stop.py` vs upstream: `_base.py`, state capture
- `.claude/hooks/stop.py` vs upstream: `_base.py`, session cleanup; upstream has random completion messages
- `.claude/hooks/notification.py` vs upstream: `_base.py`, structured event
- `.claude/hooks/permission_request.py` vs upstream: `_base.py`, adds `ALLOWED_TOOLS` + `ALLOWED_BASH_PREFIXES` stricter allowlist
- `.claude/hooks/pre_compact.py` vs upstream: `_base.py`, state capture before compaction

**DRIFT[T1] — invention** (file exists in ArhuGula with no upstream equivalent):
- `.claude/hooks/_base.py` — ArhuGula-invented shared helper library (`Logger`, `emit_event`, `handle_health_check`, `read_stdin`, `run_hook`). Not in either upstream. Imported by all 13 hooks above.

**MISSING[T1]** (11 items — files present upstream, absent in ArhuGula):
- `full-clones/install-and-maintain/.claude/hooks/setup_init.py` (183 lines) — upstream bootstrap hook for initial setup phase
- `full-clones/install-and-maintain/.claude/hooks/setup_maintenance.py` (117 lines) — upstream maintenance-phase setup hook
- `full-clones/claude-code-hooks-mastery/.claude/hooks/utils/tts/elevenlabs_tts.py`
- `full-clones/claude-code-hooks-mastery/.claude/hooks/utils/tts/openai_tts.py`
- `full-clones/claude-code-hooks-mastery/.claude/hooks/utils/tts/pyttsx3_tts.py`
- `full-clones/claude-code-hooks-mastery/.claude/hooks/utils/tts/tts_queue.py`
- `full-clones/claude-code-hooks-mastery/.claude/hooks/utils/llm/anth.py`
- `full-clones/claude-code-hooks-mastery/.claude/hooks/utils/llm/oai.py`
- `full-clones/claude-code-hooks-mastery/.claude/hooks/utils/llm/ollama.py`
- `full-clones/claude-code-hooks-mastery/.claude/hooks/utils/llm/task_summarizer.py`
- `full-clones/claude-code-hooks-mastery/.claude/status_lines/status_line_v6.py` (upstream Python status line replaced by ArhuGula's `statusline.sh`)

### Scaffolding

**MATCH:** none — every SP1 scaffolding file diverges.

**DRIFT[T1] — modifications**:
- `.claude/settings.json` vs `full-clones/claude-code-hooks-mastery/.claude/settings.json`: extended Bash permission allow-list (adds `brew`, `tmux`, `just`, `yq`, `node`, `xcode-select`, `test`, `cat`); `statusLine` wiring uses `.sh` command instead of upstream's `status_line_v6.py`
- `.claude/CLAUDE.md` vs `full-clones/claude-code-hooks-mastery/CLAUDE.md`: ArhuGula has 6.9k comprehensive project documentation (SP status table, source-precedence rules, four-layer architecture); upstream is a 0-byte stub
- `justfile` vs `full-clones/install-and-maintain/justfile`: ArhuGula has 40+ recipes spanning SP1–SP14; upstream is a 1.0k minimal justfile

**DRIFT[T1] — invention** (file exists in ArhuGula, neither upstream has it):
- `.claude/statusline.sh` — ArhuGula bash wrapper; upstream form is Python at `.claude/status_lines/status_line_v6.py`
- `package.json` — exists in ArhuGula; neither upstream ships one
- `.tool-versions` — exists in ArhuGula; `install-and-maintain` doesn't ship it

**ESCALATE-T1 — incomplete scan**:
- `.env.example` — byte-level comparison blocked by damage-control hook during scout. Needs manual diff before architect phase.

### Commands (`.claude/commands/`)

**MATCH:** none.

**DRIFT[T1] — modifications**:
- `.claude/commands/install.md` vs `full-clones/install-and-maintain/.claude/commands/install.md`: ArhuGula forward-loads Playwright / Pi-agent / Swift checks (SP4/SP8/SP13 content) into the SP1 install command
- `.claude/commands/maintain.md` vs `full-clones/install-and-maintain/.claude/commands/maintenance.md`: filename renamed `maintenance` → `maintain` + structural content delta
- `.claude/commands/build.md` vs `full-clones/claude-code-hooks-mastery/.claude/commands/build.md`: structural delta

**DRIFT[T1] — invention / ESCALATE-T1** (ArhuGula files with no upstream reference in the two SP1 source repos; may trace to another Disler repo):
- `.claude/commands/harness-review.md` — absent from both SP1 upstreams
- `.claude/commands/architect.md` — absent from both SP1 upstreams
- `.claude/commands/migrate.md` — absent from both SP1 upstreams
- `.claude/skills/prime/SKILL.md` — absent from both SP1 upstreams
- `.claude/skills/scout/SKILL.md` — absent from both SP1 upstreams

**MISSING[T1]**:
- `full-clones/install-and-maintain/.claude/commands/install-hil.md` — hardware-in-the-loop install variant

### Core Subagents (`.claude/agents/`)

**ESCALATE-T1** — all 6 core subagent definitions are absent from both SP1 upstream repos. Candidate source repos: `agentic-finance-review` (SP3), `indydevtools`, `single-file-agents`. Architect phase must locate source before SP1 can close, OR classify as inventions:
- `.claude/agents/builder.md`
- `.claude/agents/validator.md`
- `.claude/agents/spec-checker.md`
- `.claude/agents/schema-reviewer.md`
- `.claude/agents/architect.md`
- `.claude/agents/scout-agent.md`

### Library + Programmatic

**MATCH (out-of-scope note)**:
- `~/.claude/skills/library/library.yaml` — lives at user-global path per memory `feedback_library_global.md`. No SP1 T1 reference (the-library is SP6 scope).

**ESCALATE-T1**:
- `scripts/run-claude.py` — exists in ArhuGula; MANIFEST row 2 (`claude-code-is-programmable`) classifies programmatic wrapper as SP12 source. Either (a) route this finding out of SP1 scope into SP12, or (b) source-of-truth SP1 attribution is wrong and must be corrected.

### Tier 1 Summary

| Bucket | Count |
|---|---:|
| MATCH | 0 |
| DRIFT[T1] — hook/file modifications | 16 |
| DRIFT[T1] — inventions (no upstream equivalent) | 4 (`_base.py`, `statusline.sh`, `package.json`, `.tool-versions`) |
| MISSING[T1] — present upstream, absent locally | 11 |
| ESCALATE-T1 — no SP1 upstream reference | 10 (5 commands/skills + 6 subagents — `architect.md` double-counted; 10 unique paths) |
| ESCALATE-T1 — incomplete scan | 1 (`.env.example` blocked) |

### Top Tier-1 findings

1. **Hook architecture divergence — all 13 core hooks reworked via `_base.py` coupling and extended event logging.** Blast radius: hooks-wide. Atomic revert touches 14 files in one commit set. Paths: `.claude/hooks/*.py` vs `full-clones/claude-code-hooks-mastery/.claude/hooks/*.py`.
2. **6 core subagents and 3 commands (harness-review/architect/migrate) have no SP1 upstream reference.** Must locate source repo (likely `agentic-finance-review` per SP3 mapping) before byte-diff is possible. Architect phase routes to SP3.
3. **`setup.py` consolidation dropped ~205 lines of upstream logic.** Upstream ships `setup_init.py` (183L) + `setup_maintenance.py` (117L) = 300L; ArhuGula has single `setup.py` at 95L. Unverified feature parity. Split back in atomic revert.
4. **`.claude/hooks/utils/` tree — 8 files entirely missing.** TTS (4) + LLM (4) utility modules present in upstream `claude-code-hooks-mastery`, absent in ArhuGula. No documented intent to omit.
5. **`/install.md` forward-loads later-SP bootstrap.** ArhuGula adds Playwright, Pi-agent, Swift checks (SP4/SP8/SP13 content) to the SP1 install command. User decision: drop content or move to correct SP's install-extensions.

---

## Tier 2 — Intent diff vs Comprehensive docs

### Principles / philosophy alignment

**MATCH**:
- "Minimal, observable, secure" philosophy embedded in hook event emission (`comprehensive_reference §Part 1`)
- UV single-file script pattern used consistently across all hooks (`comprehensive_reference §Part 4 Coding Standards`)
- `session_start.py` health check matches "Install & Maintain pattern" (`comprehensive_reference §Part 11 Deterministic Bootstrap`)
- Proof-of-work principle: PostToolUse validators run after every Write/Edit and block on violation

**DRIFT[T2]**:
- Events emitted to JSONL but not streamed to a dashboard (`comprehensive_reference §Part 3 Principle 9 "Observability Over Trust"`). SP9 concern, but SP1 should stub the dashboard consumer interface.
- Hook events are log-only; they do not act as decision gates for downstream agents per "agents know what they are doing" principle.

### Architecture blueprint conformance (four-layer architecture)

**MATCH**:
- Four-layer architecture (Skill / Subagent / Command / Justfile) realized exactly per `blueprint §Four-Layer Architecture`. All four layers populated and wired.

**DRIFT[T2]**:
- Docs reference "**2 skills + 4 CLIs**" as the minimal stack (`comprehensive_reference §Part 1 Key Metric`). The canonical 2 skills are `steer` (GUI) and `drive` (terminal). ArhuGula ships 6 skills (`prime`, `scout`, `damage-control` + later-SP additions). The expansion is undocumented.
- Docs name 5 subagent specializations: `scout`, `planner`, `builder`, `validator`, `reviewer` (`comprehensive_reference §Part 3 Principle 4`). ArhuGula has 11 agents including `spec-checker`, `schema-reviewer`, `security`, `meta-agent` as additional roles not in the reference.
- Justfile scope: docs show minimal example; ArhuGula's has 40+ recipes pre-wiring SP7–SP14 capabilities into Layer 4 at SP1 scaffolding time.

**MISSING[T2]**:
- YAML job system contract: docs describe it as core architecture (`blueprint §Security-First Design`). SP1 does not document where/how SP8 (Drive/Listen) will plug this in.

### Pattern coverage (observation loop, proof of work, health check, event emission)

**MATCH**:
- Event emission framework: all 13 hooks call `emit_event()` writing JSONL with `session_id`, `timestamp`, `hook_name`, `exit_code`, `payload`, `duration_ms`
- Exit code spec: 0=allow, 1=pass-through (fail-open), 2=block (fail-closed) — matches "Observability Over Trust" principle
- Session health check via `session_start.py --health-check`, logs to `.claude/logs/session-start-{session_id}.json`

**DRIFT[T2]**:
- "Stream all agent events to a dashboard" (`comprehensive_reference §Part 3 Principle 9`) — ArhuGula writes JSONL files, no dashboard streamer. SP9 concern but SP1 should stub the contract.
- Health check `REQUIRED_HOOKS` list in `session_start.py` includes SP3/SP14 validators already (ruff, ty). These cause false negatives on fresh clone before SP3 ships. **ESCALATE-T2** — purge or make conditional.

**MISSING[T2]**:
- Docs describe "R&D: Reduce & Delegate" as a `scout → planner → builder` pipeline (`comprehensive_reference §Part 3 Principle 5`). ArhuGula has `/scout` → `/architect` → `/build`. Name mismatch: "planner" vs "architect". Either docs lag the rename or ArhuGula drifted the name.

### Named components in docs

**MATCH**:
- Slash commands `/install`, `/prime`, `/scout`, `/build`, `/harness-review`, `/maintain`, `/architect`, `/migrate` all exist
- `settings.json` hook wiring covers PreToolUse, PostToolUse, SessionStart, Stop, SubagentStart, SubagentStop, Notification

**DRIFT[T2]**:
- Docs reference `/scout-plan-build` as a composable skill wrapper (`comprehensive_reference §Part 5 Category 1`). ArhuGula offers three separate commands; no composable wrapper.
- "Planner" vs "architect" naming mismatch per R&D principle above.

**MISSING[T2-only]** — features described in comprehensive docs with no Tier-1 implementation reference in any Disler repo:
- `fork-terminal` skill — referenced in `comprehensive_reference §Part 5 Category 1` for spawning parallel agents. Not present in any full-clone. No byte source to revert against.
- `pocket-pick` local skill registration — docs explicitly reference pocket-pick MCP (`comprehensive_reference §Part 1, Part 8 Phase 4`). Pocket-pick exists as user-global skill per memory but is not registered locally in ArhuGula's `.claude/skills/`. SP5 owns implementation; SP1 should stub the local contract.

### Tier 2 Summary

| Bucket | Count |
|---|---:|
| MATCH | ~14 (scout-agent reported 32; ~18 referenced SP2/SP13/SP14 content, removed from this scope) |
| DRIFT[T2] | 9 |
| MISSING[T2] | 3 (YAML job contract stub, `/plan` naming, dashboard streamer stub) |
| MISSING[T2-only] | 2 (`fork-terminal` skill, `pocket-pick` local registration) |

### Top Tier-2 findings

1. **Four-layer architecture fully realized** — all four layers populated, matches blueprint. (`blueprint §Four-Layer Architecture`)
2. **Subagent set expanded from 5 to 11 archetypes** — undocumented expansion; `spec-checker`, `schema-reviewer`, `security`, `meta-agent` not in reference docs. (`comprehensive_reference §Part 3 Principle 4`)
3. **`scout-plan-build` composable skill wrapper missing** — pipeline exists as three commands, not as wrapper. (`comprehensive_reference §Part 5 Category 1`)
4. **`fork-terminal` skill absent — T2-only gap** — no Disler repo ships it; architect phase ESCALATE.
5. **Health check `REQUIRED_HOOKS` references future-SP validators** — creates false negatives before SP3 ships. Purge or gate on SP presence.

---

## Cross-tier reconciliation

### Items flagged by both tiers (T1 revert first, then T2 fix)

1. **`_base.py` + 13 hook modifications** — DRIFT[T1] byte divergence AND DRIFT[T2] "events are log-only, not dashboarded". Reverting T1 inlines helpers AND drops the event emission infrastructure. T2 dashboard streamer then has no T1 reference to rebuild against. **Order:** revert hooks → escalate event-infra rebuild as T2-only gap.
2. **`settings.json` permissions + `REQUIRED_HOOKS` list** — DRIFT[T1] extended Bash allow-list AND DRIFT[T2] health check references future-SP validators. Single atomic revert addresses both.
3. **Subagent inventions + subagent count expansion** — ESCALATE-T1 (no upstream) AND DRIFT[T2] (expansion beyond 5-archetype model). Both findings converge: shrink subagent set to canonical 5 once T1 reference is located.

### T2-only gaps (no T1 byte reference — cannot revert-against)

1. `fork-terminal` skill — build from `comprehensive_reference §Part 5 Category 1` description or defer as known gap
2. `pocket-pick` local skill registration — SP5 owns implementation; SP1 stubs the contract
3. Dashboard event streamer — T2 describes intent only; no Disler repo ships this
4. `/scout-plan-build` composable skill wrapper — T2 describes it; no T1 reference
5. YAML job system contract stub — SP8 owns implementation; SP1 references it

All five get `ESCALATE` classification in architect phase.

### Routing recommendations for architect

**SP1-owned AUTO-REVERTs (high confidence, no memory conflict)**:
- Restore `.claude/hooks/utils/tts/` and `utils/llm/` trees (8 files)
- Split `setup.py` back into `setup_init.py` + `setup_maintenance.py`
- Revert `/install.md` to upstream (drop SP4/SP8/SP13 scope creep)
- Rename `maintain.md` → `maintenance.md`
- Replace `.claude/statusline.sh` with upstream `status_lines/status_line_v6.py`
- Add `install-hil.md` from upstream
- Purge future-SP validators from `session_start.py` `REQUIRED_HOOKS`

**SP1-owned DECISION-REQUIRED (conflicts with hardening memory)**:
- Inline or remove `_base.py` → revert all 13 hooks to upstream form (blast radius: every hook; conflicts with observability infra)
- Revert `permission_request.py` `ALLOWED_TOOLS` / `ALLOWED_BASH_PREFIXES` stricter allowlist
- Revert `session_start.py` `.env` whitelist/denylist with INJECT marker
- Revert `settings.json` extended Bash permission allow-list
- Revert `pre_tool_use.py` `patterns.yaml` loading (touches SP2 patterns.yaml itself)
- Drop `package.json` and `.tool-versions` (inventions with no upstream reference)

**Route to other SPs**:
- `scripts/run-claude.py` → SP12 (`claude-code-is-programmable`)
- 6 core subagent definitions → SP3 (`agentic-finance-review`) for attribution search
- `harness-review.md`, `architect.md`, `migrate.md` commands → SP3/SP4 attribution search

**ESCALATE to user at decision gate**:
- `package.json`, `.tool-versions`: keep or drop?
- `fork-terminal` skill: build from T2 description or defer?
- `pocket-pick` local registration: stub now or defer to SP5?
- Subagent-count expansion (5 → 11): shrink to canonical 5 or document 11 as deliberate?
- Dashboard event streamer (T2-only): build from description or defer?
- `.env.example` byte comparison (scan blocked): manual diff needed before build phase

---

## Artifact metadata

- **Prior state:** first SP audit on `audit/identicality-2026-04-13` branch (main at `aa9dbd2`)
- **Expected architect input:** this file (`audits/SP1-scout.md`)
- **Expected architect output:** `audits/SP1-plan.md`
- **Estimated atomic commit count (lower bound):** 15–20
- **Items requiring user decision at gate:** ≥6 (see ESCALATE list)
- **Scout agent confidence:** high for Tier 1 byte findings, medium for Tier 2 intent mapping (docs reference conceptual features that may have been renamed/realized under different terminology)
