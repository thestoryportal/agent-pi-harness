# Maintenance Results — 2026-04-14

**Status**: FAILED

## What worked

- Hook fired correctly on `claude --maintenance` (30 sessions logged since 2026-04-13)
- Log header written successfully each run

## What failed

- **`uv sync --upgrade`** — crashes immediately: `apps/backend/` does not exist in ArhuGula
- **`npm update`** — never reached: `apps/frontend/` does not exist in ArhuGula
- **SQLite VACUUM** — never reached: `apps/backend/starter.db` does not exist
- **DB integrity** — never reached: same reason above
- Result: hook exits on exception after "Running: uv sync --upgrade", no completion output logged

## Root Cause

`setup_maintenance.py` is a generic project template targeting a `apps/backend` + `apps/frontend` + SQLite monorepo. ArhuGula has neither — its apps directory contains `drive/`, `listen/`, `direct/`, `dropzone/`, `sandbox_fundamentals/`, `sandbox_mcp/`, `observe/`, `steer/`, and `voice/` — all separate uv projects with their own `pyproject.toml`.

When `subprocess.run(["uv", "sync", "--upgrade"], cwd=backend_dir)` is called with a non-existent `cwd`, Python raises an uncaught exception that crashes the hook.

## Next Steps

The maintenance hook needs to be updated for ArhuGula's actual structure:

1. Replace the single `apps/backend` uv sync with per-app syncs across all apps that have a `pyproject.toml`
2. Remove the `apps/frontend` npm update (no frontend app exists)
3. Remove the SQLite VACUUM (no `starter.db` — ArhuGula uses JSONL log files, not SQLite)
4. Add ArhuGula-appropriate maintenance: verify hook health, check JSONL log retention, validate damage-control patterns.yaml

**Note:** This requires an SP r2 round or harness-review follow-up, as the fix would diverge from the upstream `setup_maintenance.py` byte-identical clone (Tier 3 audit carve-out needed). Check audits/exceptions.md before proceeding.
