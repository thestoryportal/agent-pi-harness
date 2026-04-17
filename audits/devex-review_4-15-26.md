# DX Live Audit — ArhuGula

**Date:** 2026-04-15  
**Branch:** audit/identicality-2026-04-13  
**Commit:** d7e9cbe  
**Skill:** /devex-review  
**Product type:** Internal developer harness (personal/small-team)  
**Audit method:** File inspection (INFERRED) — no web presence to browse

---

## DX Scorecard

```
+====================================================================+
|              DX LIVE AUDIT — arhugula                               |
+====================================================================+
| Dimension            | Score  | Evidence        | Method   |
|----------------------|--------|-----------------|----------|
| Getting Started      |  3/10  | setup_init.py   | INFERRED |
| API/CLI/SDK          |  7/10  | justfile, CLI   | INFERRED |
| Error Messages       |  4/10  | hook log, code  | INFERRED |
| Documentation        |  6/10  | CLAUDE.md, cmds | INFERRED |
| Upgrade Path         |  3/10  | no CHANGELOG    | INFERRED |
| Dev Environment      |  5/10  | .env.ex, hooks  | INFERRED |
| Community            |  2/10  | private repo    | INFERRED |
| DX Measurement       |  3/10  | events.jsonl    | INFERRED |
+--------------------------------------------------------------------+
| TTHW (measured)      | BROKEN | install crashes | INFERRED |
| Overall DX           |  4.1/10|                 |          |
+====================================================================+
```

---

## Getting Started Audit — 3/10

```
GETTING STARTED AUDIT
=====================
Step 1: Clone repo                         Time: 1 min   Friction: low    Evidence: git remote shows thestoryportal/agent-pi-harness
Step 2: cp .env.example .env, fill keys    Time: 5-10m   Friction: HIGH   Evidence: 13 keys in .env.example; 8 are secrets; not marked mandatory/optional
Step 3: just cldii (claude --init /install) Time: 2 min  Friction: HIGH   Evidence: setup_init.py:119 runs uv sync in apps/backend/ — DOES NOT EXIST → exits 2
Step 4: /prime (if install survived)       Time: 2 min   Friction: low    Evidence: 731 files, clean prime report

TOTAL: broken — install hook crashes on first run
```

**Critical finding:** `setup_init.py:119` calls `run(["uv", "sync"], cwd=backend_dir)` where `backend_dir = "apps/backend/"`. That directory does not exist in ArhuGula. The hook exits 2 silently. The `setup.init.log` confirms this: 15+ consecutive runs all end at "Running: uv sync" with no success output. Every `just cldii` session starts with a silent install failure.

Gap to 10: Fix `setup_init.py` to match ArhuGula's actual structure (no `apps/backend/`, no SQLite, no Vue frontend). Running `uv sync` in the project root is likely the correct behavior. TTHW < 5 minutes is achievable after this fix.

---

## API/CLI/SDK Ergonomics — 7/10

`just --list` returns 60+ recipes. Every recipe has a comment. The 4-layer grouping (Skill → Subagent → Command → Justfile) is explicit in the file but invisible at runtime — `just --list` shows them alphabetically, not grouped.

`run-claude.py --help` is clean: all params documented, `--preset` saves 4 lines per call.

The `ext-*` namespace for Pi extensions (16 recipes) has no discovery path — a new developer running `just --list` sees `ext-agent-chain`, `ext-damage-control`, etc., with no context that these are Pi status-line extensions.

Naming is consistent within each SP. Cross-SP consistency is good: `sfa-bash`, `sfa-duckdb`, `sfa-sqlite`, `sfa-polars`, `sfa-jq`, `sfa-metaprompt` all follow the pattern.

Gap to 10: Group `just --list` output by layer (justfile supports `[group]` recipe attributes since `just 1.9`). Add a one-line comment explaining the `ext-*` namespace.

---

## Error Messages — 4/10

**Damage-control blocks:**
```json
{"error": "Blocked: zero-access path .env (no operations allowed)"}
```
Functional. Reason string is specific and actionable. Missing: which rule triggered it, where to find `patterns.yaml`.

**Init hook failure:**
```
>>> Setting up Python backend...
  Running: uv sync
[process exits 2, log stops]
```
No "ERROR: apps/backend does not exist". No exit message. No suggested fix. A developer sees nothing in the Claude Code session — the error disappears into init hook stderr.

**Hook health check failures** (`session_start.py`): logs `Hook health check failed: [filename]` but no "how to fix it" guidance.

Gap to 10: Init hook failures need human-readable errors: "ERROR: apps/backend not found. If this is a fresh ArhuGula setup, update setup_init.py to match your directory structure." Damage-control errors could include a doc pointer.

---

## Documentation — 6/10

CLAUDE.md is genuinely good. Navigation table, 4-layer architecture with invocation examples, naming conventions, SP status table, hook security model, and skill routing — all in one file.

The `.env.example` inline comments are excellent — `# INJECT` vs `# Secrets — NEVER injected`, TTS priority order documented, SP16 prerequisites called out inline.

Weak spots:
- README.md is 8 lines — useless for cold-start orientation
- No architecture diagram
- `setup_init.py` docstring says "Install dependencies and initialize the database" — not true since `apps/backend/` was dropped

Gap to 10: Update `setup_init.py` docstring. Add a one-paragraph architecture overview to README. The CLAUDE.md quality is impressive — most projects don't get this right.

---

## Upgrade Path — 3/10

No CHANGELOG. No MIGRATION guide. No `DEPRECATED` comments in authored code.

The source of truth document functions as an upgrade log for the audits — SP completion dates are tracked there. But it is a research artifact, not a developer-facing changelog.

The exception ledger (30 exceptions) is the closest thing to a migration guide. It is stored in memory files, not in the repo itself.

`git log` is the actual changelog. Commits are well-written (audit phases, exception numbers, specific file operations). Better than most projects. But it requires reading git history to understand what changed and why.

Gap to 10: Add `CHANGELOG.md`. Given the SP1-SP16 audit sweep just completed, one entry summarizing the identicality audit, the 30 exceptions, and any breaking changes to hook interfaces would close most of this gap.

---

## Developer Environment — 5/10

Strong:
- `.tool-versions` pins `nodejs 22` + `python 3.12` — exact version pinning, works with asdf/mise
- `uv` for Python deps — fast, deterministic
- `package.json` pins exact Claude Code version
- `.env.example` comments explain which vars are optional

Weak:
- `setup_init.py` is broken — targets `apps/backend/`, `apps/frontend/` that don't exist
- `setup_maintenance.py` also crashes (targets non-existent `apps/backend/` + SQLite)
- 13 API keys in `.env.example`; only `ANTHROPIC_API_KEY` is strictly required for basic use, but this is not stated anywhere
- No "minimum viable .env" guidance

Gap to 10: (1) Fix `setup_init.py` — highest-leverage fix in the whole audit. (2) Add a "Required vs optional" key comment block to `.env.example`. (3) Fix `setup_maintenance.py` similarly.

---

## Community & Ecosystem — 2/10

Private repo. No CONTRIBUTING.md. No GitHub issue templates. No Discord/Slack.

Personal harness derived from IndyDevDan's public work. "Community" does not apply in the traditional sense. The CLAUDE.md has a Source Precedence table and explicit feature rules — this is effectively a contributor guide for AI agents working in the repo.

Score of 2 is calibrated for a personal harness where community expectations are different.

---

## DX Measurement — 3/10

JSONL event logs at `.claude/logs/events.jsonl` capture every hook invocation with timing, session ID, and payload preview — good for internal debugging.

No NPS widget, no docs analytics, no usage tracking for `just` recipes. The gstack learnings system adds learning capture.

---

## TTHW Assessment

| Tier | Target | Current | Status |
|------|--------|---------|--------|
| Champion | < 2 min | BROKEN | install crashes |
| Competitive | 2-5 min | — | unreachable until install fixed |

With fix #1 applied, TTHW would be approximately 8-12 minutes (key setup is the bottleneck). With a "minimum viable .env" comment, it drops to 5-7 min.

---

## Top 3 Fixes (Ranked by Impact)

### Fix 1 — `setup_init.py` and `setup_maintenance.py` (P0)

Both hooks target `apps/backend/` + `apps/frontend/` + SQLite. None exist. Every `claude --init` and `claude --maintenance` session silently fails.

```python
# Current (broken) — setup_init.py:109-135
backend_dir = os.path.join(project_dir, "apps", "backend")
run(["uv", "sync"], cwd=backend_dir)

# Should be (ArhuGula root has pyproject.toml)
run(["uv", "sync"], cwd=project_dir)
```

Impact: Getting Started 3→7, Dev Environment 5→7.

### Fix 2 — `.env.example` minimum viable comment block

```bash
# === Minimum required for basic operation ===
# ANTHROPIC_API_KEY — required for all Claude Code sessions
# All other keys are optional; features that need them will fail gracefully
```

Impact: Getting Started +1, Dev Environment +1.

### Fix 3 — Add `CHANGELOG.md`

One entry summarizing the SP1-SP16 identicality audit sweep, the 30 exceptions, and any breaking changes to hook interfaces.

Impact: Upgrade Path 3→6.
