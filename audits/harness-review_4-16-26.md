# Harness Review — audit/identicality-2026-04-13
**Date:** 2026-04-16
**Branch:** `audit/identicality-2026-04-13`
**Reviewers:** @validator + @security (parallel fan-out)
**Spec:** `~/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md`
**Prior review:** `audits/harness-review_4-14-26_ten-54-pm-mst.md`

---

## Summary

- **Commits ahead of main:** ~96 (SP1–SP16 r1 sweep + SP15-r2 obox deprecation + 2 post-sweep fixes)
- **Files changed:** 756 (+99,212 / -16,365)
- **Convention + spec violations (validator):** 0 P0, 1 P1, 1 P2, 4 P3
- **Security findings (security):** 2 HIGH (P0/P1), 2 MEDIUM (P1), 3 LOW (P2)
- **Missing requirements:** 0 (all 16 SPs structurally present)
- **Prior-review P0 resolved:** S-01 patterns.yaml self-lock — CONFIRMED FIXED

---

## Resolved Since 2026-04-14 Review

**S-01-OLD · patterns.yaml self-lock** — CONFIRMED RESOLVED
`.claude/skills/damage-control/patterns.yaml:767`
`readOnlyPaths` now includes `patterns.yaml` itself. The prior P0 (rulebook could be silently cleared by a single Edit) is closed.

---

## Priority Findings

### P0 / Critical — Security

**S-NEW-01 · Full tool I/O written to unprotected `./logs/` directory**
`.claude/hooks/post_tool_use.py:17-32`, `.claude/hooks/stop.py:173-211`

`post_tool_use.py` writes every tool's complete input/output blob to `Path.cwd() / 'logs' / 'post_tool_use.json'`. `stop.py` does the same to `./logs/stop.json`. The `zeroAccessPaths` entry in patterns.yaml (line 706) protects `.claude/logs/`, which is an entirely **different** directory than `./logs/`. Any agent can issue `Read("logs/post_tool_use.json")` and extract accumulated tool I/O including any API keys, passwords, or tokens that appeared in Bash outputs (`env`, `printenv`, `set`) or tool inputs during the session.

**Fix:** Change log path in both files to `.claude/logs/`, OR add `"logs/"` to `zeroAccessPaths` in patterns.yaml, AND add `"logs/chat.json"` to the same list (stop.py transcript).

---

### P1 — Security

**S-OLD-02 · `pre_tool_use.py` does not resolve symlinks** *(carried from 2026-04-14 review)*
`.claude/hooks/pre_tool_use.py:55-81`

`match_path()` calls `os.path.normpath()` but never `os.path.realpath()`. A symlink at any non-protected path pointing to `.env`, `~/.ssh/id_rsa`, or other zero-access targets passes the Read tool check. `edit_damage_control.py` and `write_damage_control.py` both call `Path().resolve()` correctly — `pre_tool_use.py` is the outlier.

**Fix:** Add `Path(expanded_normalized).resolve()` before `match_path()` in `check_read()`.

---

**S-OLD-03 · `ValueError` in `PurePath.match()` is fail-open** *(carried from 2026-04-14 review)*
`.claude/hooks/pre_tool_use.py:67-75`

On `ValueError`, `match_path()` does `pass` then `return False` ("no match" = allow). The inline comment says "fail closed" — the behavior is fail-open. An invalid pattern silently stops blocking for that rule.

**Fix:** Replace `pass` / `return False` with `return True` (block on invalid pattern = truly fail-closed).

---

**S-NEW-02 · `session_start.py` emits env values into model context**
`.claude/hooks/session_start.py:46, 232-233, 240`

`env_summary` is built as `f"{k}={v}"` for each injected var and emitted as `additionalContext` — visible to the model and all subagents. The `SECRET_PATTERNS` denylist (line 46) filters keys containing `KEY`, `TOKEN`, `SECRET`, `PASSWORD`, `CREDENTIAL`, `AUTH`. Common credential variable names not covered: `PGPASSWORD`, `DATABASE_URL` (may embed password in URI), `SMTP_PASS`, `MONGO_URI`.

**Fix:** Emit only key names, not values: `f"Injected env keys: {', '.join(safe_env.keys())}"`.

---

**S-OLD-04 · Damage-control hooks excluded from health check** *(carried from 2026-04-14 review)*
`.claude/hooks/session_start.py:81-94`

The three skill-located damage-control hooks (`bash_damage_control.py`, `edit_damage_control.py`, `write_damage_control.py`) are not in `REQUIRED_HOOKS`. A missing or crashed file is undetected until first use. Confirmed by inline comment at lines 87-93.

**Fix:** Add the three skill-path hooks by absolute path to `run_health_checks()`.

---

### P2 — Security (Defense-in-Depth)

**S-NEW-03 · Bash exclusion allowlist could pass symlink through hooks dir**
`.claude/skills/damage-control/patterns.yaml:932-937`

`bashToolExclusions` permits `cat .*\.claude/hooks/` with `.*` wildcard. A symlink at `.claude/hooks/mylink -> ../../.env` would produce `cat .claude/hooks/mylink` which matches the exclusion and allows the cat while the OS resolves the symlink to `.env`. The `ln` check in `bash_damage_control.py` validates argument paths are within the project but does not verify the symlink *target* is not a zero-access path.

**Fix:** Tighten exclusion pattern to specific filenames (`\bcat\s+\.claude/hooks/[a-z_]+\.py\b`), and add a zero-access target check to the `ln` path validation.

---

**S-LOW-01 · `permission_request.py` fragile on null `tool_input`**
`.claude/hooks/permission_request.py:38-45`

Minor code path fragility — resolves to deny (correct behavior) on edge cases. No immediate impact; flagged for future-edit robustness.

**Fix:** Add explicit `if not d: sys.exit(2)` guard at start of `main()`.

---

### P1 — Convention/Spec

**V-01 · Exception 18 (env sample damage-control hard stop) eligible for revert**

Exception 18 is documented as UNRESOLVED with user direction to revert post-audit-complete. SP1-SP16 r1 sweep closed 2026-04-14. The revert gate is open. Requires explicit user authorization per `feedback_damage_control_self_unlock.md`.

**Action:** User-authorized revert only. Do not self-unlock.

---

### P2 — Convention

**V-02 · Command naming inconsistency: hyphens vs underscores**
`.claude/commands/prime_cli_sandbox.md`, `prime_tts.md`, `load_ai_docs.md`

CLAUDE.md convention: authored files use `lowercase-with-hyphens`. Three commands use underscores. These are Tier 1 byte-identical upstream imports (Exception 21/23 class) — not a regression, but a documented convention deviation.

---

### P3 — Nit

**V-03 · SP1-SP9 rows in `CLAUDE.md` missing "+ AUDIT R1" suffix**
`.claude/CLAUDE.md` (SP table)
SP10-SP16 rows show `BUILT + AUDIT R1 (2026-04-14)`. SP1-SP9 show `BUILT` only, even though all were audited. Cosmetic inconsistency for readers cross-referencing the SoT.

**V-04 · Large log files tracked in git**
`.claude/hooks/setup.init.log` (29.2K), `.claude/hooks/setup.maintenance.log` (13.9K),
`.claude/hooks/utils/validators/ruff_validator.log` (341K), `.claude/hooks/utils/validators/ty_validator.log` (328.9K)
Four log files are checked into version control. Add patterns to `.gitignore`.

**V-05 · `settings.json` stray blank line**
`.claude/settings.json:38` — cosmetic.

---

## Confirmed Safe

- **patterns.yaml self-lock:** `readOnlyPaths` line 767 — CONFIRMED (prior P0 CLOSED)
- **Listen app bind address:** `127.0.0.1` in `apps/listen/main.py:123` — Exception 31 satisfied
- **TTS in stop.py:** completion message from LLM scripts, not hook event data — no secret leak through TTS argv
- **MCP gate:** token-sequence matching, 512-char cap, ASCII check present in `pre_tool_use.py:153-234`
- **Fail-closed import guard:** `pre_tool_use.py:31-35` exits 2 on import failure
- **curl short-flag bundling:** all patterns use `\s-[A-Za-z]*<flag>` form
- **run_hook security_critical path:** correctly exits 2 in `_base.py:133-137`
- **All 16 SPs structurally present:** hooks, commands, agents, skills, justfile recipes verified

---

## Recommended Action Items (Ordered by Priority)

| # | Priority | Finding | Action |
|---|----------|---------|--------|
| 1 | P0 | S-NEW-01 `./logs/` unprotected | Change log path to `.claude/logs/` in post_tool_use.py + stop.py, or add `logs/` to zeroAccessPaths |
| 2 | P1 | S-OLD-02 symlink bypass | Add `os.path.realpath()` to `check_read()` in pre_tool_use.py |
| 3 | P1 | S-OLD-03 ValueError fail-open | `return True` on ValueError in `match_path()` |
| 4 | P1 | S-NEW-02 env value leak | Emit only key names in session_start.py env_summary |
| 5 | P1 | S-OLD-04 health check gap | Add skill-path hooks to REQUIRED_HOOKS |
| 6 | P1 | V-01 Exception 18 revert | User-authorized action when ready |
| 7 | P2 | S-NEW-03 hooks exclusion symlink | Tighten exclusion pattern + add target check to ln validation |
| 8 | P3 | V-03 CLAUDE.md SP table | Add "+ AUDIT R1" suffix to SP1-SP9 rows |
| 9 | P3 | V-04 log files in git | Add log patterns to .gitignore |
