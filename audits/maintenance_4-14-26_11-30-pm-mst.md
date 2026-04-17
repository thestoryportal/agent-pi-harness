# Maintenance Hook Audit — 2026-04-14 11:30 PM MST

**Status**: FAILED (hook crashes on every run)

## What worked

- Hook fired correctly on `claude --maintenance` (30 sessions logged since 2026-04-13)
- Log header written successfully each run

## What failed

- **`uv sync --upgrade`** — crashes immediately: `apps/backend/` does not exist in ArhuGula
- **`npm update`** — never reached: `apps/frontend/` does not exist in ArhuGula
- **SQLite VACUUM** — never reached: `apps/backend/starter.db` does not exist
- **DB integrity check** — never reached: same reason
- Result: hook exits on unhandled exception after "Running: uv sync --upgrade"; no completion output ever logged

## Root Cause

`setup_maintenance.py` is a generic project template targeting a `apps/backend` + `apps/frontend` + SQLite monorepo. ArhuGula has none of those. Its apps directory contains separate uv projects: `drive/`, `listen/`, `direct/`, `dropzone/`, `sandbox_fundamentals/`, `sandbox_mcp/`, `observe/`, `steer/`, `voice/` — each with its own `pyproject.toml`.

`subprocess.run(["uv", "sync", "--upgrade"], cwd=backend_dir)` raises an uncaught exception when `cwd` doesn't exist, crashing the hook before any subsequent steps execute.

Relevant code: `.claude/hooks/setup_maintenance.py` lines 64–65.

## Fix Required (Tier 3 carve-out needed)

The maintenance hook needs to be updated for ArhuGula's actual structure:

1. **Replace** the single `apps/backend` uv sync with per-app `uv sync --upgrade` across all apps that contain a `pyproject.toml` (drive, listen, direct, dropzone, sandbox_fundamentals, sandbox_mcp, observe, voice)
2. **Remove** the `apps/frontend` npm update — no frontend app exists
3. **Remove** the SQLite VACUUM + integrity check — no `starter.db`; ArhuGula uses JSONL log files
4. **Add** ArhuGula-appropriate checks:
   - Verify all 13 hooks are healthy (analogous to `session_start.py` health check)
   - Check JSONL log retention (prune old logs per `OBSERVE_RETENTION_DAYS`)
   - Validate damage-control `patterns.yaml` is syntactically valid

This fix diverges from the upstream `setup_maintenance.py` byte-identical clone and requires a **Tier 3 audit carve-out** (analogous to Exceptions 22/24/27). Add to `audits/exceptions.md` before implementing.

## Files

- Log file: `.claude/hooks/setup.maintenance.log`
- Hook source: `.claude/hooks/setup_maintenance.py`
- Exceptions registry: `audits/exceptions.md`
