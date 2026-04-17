# Harness Review — audit/identicality-2026-04-13
**Date:** 2026-04-14, 10:54 PM MST
**Branch:** `audit/identicality-2026-04-13`
**Reviewers:** @validator + @security (parallel fan-out)

---

## Summary

- **Commits ahead of main:** ~94 (SP1–SP16 r1 identicality audit sweep + SP15-r2 obox deprecation)
- **Files changed:** 754 (+98,542 / -16,361)
- **Convention + spec violations (validator):** 2 P1, 4 P2, 3 P3
- **Security findings:** 1 critical, 3 high, 4 medium, 1 low
- **Missing requirements:** 0 (all 16 SPs structurally present; byte-identicality spot-checks pass)

---

## Priority Findings

### P0 / Critical — Security

**S-01 · patterns.yaml is unprotected — self-modification disables all blocking**
`audits/exceptions.md` (known SP2 follow-up, not yet closed)

`patterns.yaml` is the rulebook for every blocking decision in all 4 hooks. It loads on every hook call. It is **not** in `readOnlyPaths`. An agent can emit one Edit call to this file, clear all rules, and the next Bash/Write/Read call passes with zero resistance. This is the "patterns.yaml isn't locked (round-9)" finding noted in your SP2 architectural follow-ups memory — still open.

**Fix:** Add `.claude/skills/damage-control/patterns.yaml` to `readOnlyPaths` in patterns.yaml itself.

---

### P1 — Security

**S-02 · `pre_tool_use.py` does not resolve symlinks**
`.claude/hooks/pre_tool_use.py:53-57`

`edit_damage_control.py` and `write_damage_control.py` both call `Path().resolve()` before checking zero-access paths. `pre_tool_use.py`'s `match_path()` only calls `os.path.normpath()` — it never follows symlinks. A committed symlink `safe.txt → ~/.ssh/id_rsa` passes the Read tool zero-access check.

**Fix:** Add `Path(expanded_normalized).resolve()` to the path normalization in `match_path()`, mirroring the edit/write hooks.

---

**S-03 · `ValueError` in `PurePath.match()` is fail-open, not fail-closed**
`.claude/hooks/pre_tool_use.py:67-75`
`.claude/skills/damage-control/hooks/damage-control-python/edit_damage_control.py:79-82`

When a zeroAccessPaths pattern raises `ValueError`, the `except` block does `pass` then `return False`. For a block-list, `False` = no match = **allow**. The comment says "fail closed" — it is not. An invalid pattern (e.g. bare `[`) silently stops blocking for that rule.

**Fix:** On `ValueError`, return `True` (treat as matched = block) for security-critical callers, or validate all patterns at load-time and exit 2 if invalid.

---

**S-04 · Damage-control hooks removed from health check — missing file = silent fail-open**
`.claude/hooks/session_start.py:81-94`

The three damage-control hooks were moved to `.claude/skills/damage-control/hooks/damage-control-python/` and were explicitly removed from `REQUIRED_HOOKS`. If these files are absent (fresh clone, partial setup, or deliberate deletion), `uv run` on a missing file exits 1, which Claude Code treats as pass-through — the Bash/Edit/Write protection layers are silently disabled for the session. CLAUDE.md promises "Health check: `session_start.py` validates all hooks at session start."

**Fix:** Add the skill-path hook files to `REQUIRED_HOOKS` by absolute path. Also known from SP2 architectural follow-ups memory.

---

### P1 — Convention/Spec

**V-01 · Global library catalog is stale for 6 entries**
`~/.claude/skills/library/library.yaml`

1. `builder` → points to `.claude/agents/builder.md` (deleted; moved to `team/`)
2. `validator` → points to `.claude/agents/validator.md` (deleted; moved to `team/`)
3. `schema-reviewer` → points to `.claude/agents/schema-reviewer.md` (deleted, Exception 5)
4. `spec-checker` → points to `.claude/agents/spec-checker.md` (deleted, Exception 5)
5. `harness-review` prompt description says "validator + spec-checker" but spec-checker was dropped in SP9 r1
6. Skills missing from catalog: `agent-sandboxes`, `claude-bowser`, `drive`, `playwright-bowser`, `steer` (all added during SP7–SP16 sweeps)

Exception 19 covers catalog *population*, not staleness. This is new drift.

---

**V-02 · `session_start.py` health check only validates 3 of 14 required hooks**
`.claude/hooks/session_start.py:97-127`

The health check runs `uv run <hook> --health-check` on all REQUIRED_HOOKS. Only 3 hooks (`session_start.py`, `pre_tool_use.py`, `permission_request.py`) actually implement `handle_health_check()`. The other 11 get invoked with an empty stdin and return 0 by accident — the probe doesn't actually validate anything hook-specific.

---

### P2 — Medium

**S-05 · Pipe splitter doesn't handle process substitution `<(...)` or heredoc bodies**
`.claude/skills/damage-control/hooks/damage-control-python/bash_damage_control.py:166-221`

`cat <(cat .env)` runs the nested `cat .env` in a subshell that the splitter never tokenizes. The zero-access `.env` check doesn't fire.

**Fix:** Add a pattern to `bashToolPatterns` blocking `<(` and `>(` as process substitution syntax.

---

**S-07 · `python-settings.json` references non-existent hook paths**
`.claude/skills/damage-control/hooks/damage-control-python/python-settings.json:9,24,33`

The sample config references the old `damage-control/bash-tool-damage-control.py` path (wrong directory, wrong filename). Any new project created from this template deploys with silently missing damage-control protection.

**Fix:** Update paths to `skills/damage-control/hooks/damage-control-python/bash_damage_control.py`.

---

**S-08 · `bashToolExclusions` rm patterns are over-broad**
`.claude/skills/damage-control/patterns.yaml` (rm exclusion patterns)

`\brm\s+.*__pycache__` matches `rm -rf apps/safe/__pycache__/../../hooks/pre_tool_use.py` because `.*` consumes the traversal. The exclusion fires before the destructive-rm block.

**Fix:** Anchor the pattern to require `__pycache__` at the terminal path component.

---

**V-03 · Source-of-truth text stale in §1, §3.3, §4.7 after SP1-SP16 sweep**
`~/Projects/indydevdan-harness-research/.../arhugula-source-of-truth.md`

Three stale claims:
- §1 SP1 block says "/maintain" (renamed to "/maintenance")
- §3.3 "all 7 agents have `memory: scope: session`" — false for 6 Tier 1 byte-identical reverts
- §4.7 O08 repeats same stale agent frontmatter claim

Doc-only fixes, no code changes needed.

---

**V-04 · `install.md` SP2 D12=A merge not in `audits/exceptions.md`**
`.claude/commands/install.md:39-56`

Local `install.md` is a documented inline merge of two upstream files, self-documented inside the file but not in the exceptions ledger, which by its own preamble must capture every deliberate deviation.

**Fix:** Add Exception 31 entry or fold into Exception 7.

---

### P3 — Minor / Nits

**S-06 · pathExclusion traversal protection works correctly but by accident (undocumented)**
`.claude/skills/damage-control/hooks/damage-control-python/bash_damage_control.py:282-293`

`normpath()` eliminates traversal components before exclusion matching, making `cat .env.example/../.env` bypass impossible by construction — but the comment doesn't say so. Add a 1-line comment to document this invariant.

---

**S-09 · `patterns.yaml` header comment says wrong location**
`.claude/skills/damage-control/patterns.yaml:2`

`# Location: .claude/hooks/patterns.yaml` is stale (moved to `.claude/skills/damage-control/`).

---

**V-05 · Underscore command filenames missing from naming convention exception doc**
`.claude/commands/load_ai_docs.md`, `prime_cli_sandbox.md`, `prime_tts.md`

CLAUDE.md §Naming Conventions says "Authored files: lowercase-with-hyphens." These three are Tier 1 byte-identical imports with underscores. The Disler-authoritative rule resolves the tension but it's undocumented.

**Fix:** Extend CLAUDE.md naming rule with "Tier 1 imports preserve upstream filenames" or add an Exception entry.

---

**V-06 · Runtime log files co-located with hook source**
`.claude/hooks/setup.init.log`, `setup.maintenance.log`

Runtime artifacts sitting next to source. Consider redirecting to `.claude/logs/` or adding `.claude/hooks/*.log` to `.gitignore`.

---

## Recommended Action Items (ordered by priority)

| # | Priority | Action | File |
|---|----------|--------|------|
| 1 | P0 | Add `patterns.yaml` to `readOnlyPaths` | `patterns.yaml` |
| 2 | P1 | Add `Path().resolve()` to `pre_tool_use.py match_path()` | `pre_tool_use.py` |
| 3 | P1 | Change `except ValueError: pass; return False` → `return True` | `pre_tool_use.py`, `edit_damage_control.py` |
| 4 | P1 | Add damage-control skill hooks to REQUIRED_HOOKS by absolute path | `session_start.py` |
| 5 | P1 | Sync library.yaml catalog (4 deletions, 2 path updates, 5 new skills) | `library.yaml` |
| 6 | P2 | Fix `python-settings.json` hook paths to actual file locations | `python-settings.json` |
| 7 | P2 | Anchor rm exclusion patterns to terminal path component | `patterns.yaml` |
| 8 | P2 | Block `<(` / `>(` process substitution in bashToolPatterns | `patterns.yaml` |
| 9 | P2 | Add Exception 31 for `install.md` SP2 D12=A merge | `audits/exceptions.md` |
| 10 | P2 | Update SoT §1/§3.3/§4.7 stale text (doc-only) | `arhugula-source-of-truth.md` |
| 11 | P3 | Add traversal-protection comment to `_matches_exclusion` and `check_read` | both hooks |
| 12 | P3 | Update `patterns.yaml` location comment in header | `patterns.yaml` |
| 13 | P3 | Document Tier 1 underscore filenames in CLAUDE.md or exceptions.md | `CLAUDE.md` |
| 14 | P3 | Add `.claude/hooks/*.log` to `.gitignore`, redirect to `.claude/logs/` | `.gitignore` |

---

## Files Inspected by Validator

- `.claude/settings.json`
- `.claude/hooks/session_start.py`
- `.claude/hooks/_base.py`
- `.claude/hooks/pre_tool_use.py`
- `.claude/agents/` (all 10 files + team/)
- `.claude/commands/build.md`, `install.md`, `maintenance.md`, `harness-review.md`, `architect.md`
- `audits/exceptions.md` (index + Ex 4, 5, 6, 7, 15, 19, 23)
- `~/Projects/indydevdan-harness-research/.../arhugula-source-of-truth.md` (§1, §3, §4, §7, §8, §11)
- `~/.claude/skills/library/library.yaml`

## Files Inspected by Security

- `.claude/hooks/pre_tool_use.py`
- `.claude/skills/damage-control/hooks/damage-control-python/bash_damage_control.py`
- `.claude/skills/damage-control/hooks/damage-control-python/edit_damage_control.py`
- `.claude/skills/damage-control/hooks/damage-control-python/write_damage_control.py`
- `.claude/skills/damage-control/hooks/damage-control-python/python-settings.json`
- `.claude/settings.json`
- `.claude/hooks/session_start.py`
- `.claude/hooks/_base.py`
- `.claude/skills/damage-control/patterns.yaml`
