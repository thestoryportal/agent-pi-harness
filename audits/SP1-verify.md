# SP1 Audit — Verify Artifact (Round 1)

**Date:** 2026-04-13
**SP:** 1 — CC Harness
**Phase:** Verify (Phase 5, v2 methodology)
**Branch:** `audit/identicality-2026-04-13`
**Scope:** 6 of 14 SP1 AUTO-REVERT commits landed; 8 deferred to SP2 audit per `audits/exceptions.md` Exception 3

---

## Verify results per commit

### Commit 3 — `status_lines/` tree (SHA `9f74fc3`)

| File | Classification | Note |
|---|---|---|
| `status_line.py` | MATCH | 152 lines, byte-identical to upstream |
| `status_line_v2.py` | INTENTIONAL DRIFT (Exception 2) | Unused `import os` removed by ruff validator; ArhuGula version has 1 line fewer than upstream |
| `status_line_v3.py` | MATCH | 188 lines, byte-identical to upstream |
| `status_line_v4.py` | MATCH | 200 lines, byte-identical to upstream |
| `status_line_v5.py` | MATCH | 128 lines, byte-identical to upstream |
| `status_line_v6.py` | MATCH | 142 lines, byte-identical to upstream |
| `status_line_v7.py` | MATCH | 176 lines, byte-identical to upstream |
| `status_line_v8.py` | MATCH | 121 lines, byte-identical to upstream |
| `status_line_v9.py` | MATCH | 189 lines, byte-identical to upstream |

**DEL check:** no missing files in either direction. All 9 ArhuGula `status_lines/` files accounted for.

### Commit 9 — `install-hil.md` (SHA `a43c8e1`)

| File | Classification | Note |
|---|---|---|
| `.claude/commands/install-hil.md` | MATCH | Byte-identical to upstream `install-and-maintain/.claude/commands/install-hil.md` |

### Commit 10 — `maintenance.md` rename (SHA `a3033b3`)

| Check | Result | Note |
|---|---|---|
| `maintain.md` absent | YES | No file found in `.claude/commands/` |
| `maintenance.md` present | YES | File exists at `.claude/commands/maintenance.md` |
| Content preserved (rename only, no content change) | YES | Matches pre-rename content; content revert to upstream is pending D3 decision |

### Commit 11 — `justfile` reference updates (SHA `0e3cb73`)

| Check | Result | Note |
|---|---|---|
| No remaining `maintain.md` path references | YES | Grep returned zero matches |
| Reference updated to `/maintenance` | YES | `cldmm` recipe body now references `"/maintenance"` |
| Recipe names preserved | YES | `cldm`, `cldmm` preserved (ArhuGula convention per plan) |

### Commit 12 — `install.md` revert (SHA `b47306f`)

| File | Classification | Note |
|---|---|---|
| `.claude/commands/install.md` | MATCH | Byte-identical to upstream `install-and-maintain/.claude/commands/install.md` (38 lines) |
| No Playwright content | YES | Zero grep matches |
| No Pi-agent content | YES | Zero grep matches |
| No Swift content | YES | Zero grep matches |

### Commit 13 — `build.md` revert (SHA `1facd9e`)

| File | Classification | Note |
|---|---|---|
| `.claude/commands/build.md` | MATCH | Byte-identical to upstream `claude-code-hooks-mastery/.claude/commands/build.md` (21 lines) |
| No inline PostToolUse hooks | YES | Zero grep matches |
| No `allowed-tools` block | YES | Zero grep matches |
| No `agent: builder` directive | YES | Zero grep matches |
| No ruff/ty validator references | YES | Zero grep matches |

---

## New drift introduced

**(none)** — all 6 commits verified successfully. No unexpected deviations beyond Exception 2 (documented validator-forced drift on `status_line_v2.py`).

---

## Remaining SP1 gaps after this round

- **8 commits deferred to SP2 audit** (Exception 3): Commits 1, 2, 4, 5, 6, 7, 8, 14
- **7 DECISION-REQUIRED items pending user gate** (D1–D7 from `audits/SP1-plan.md`)
- **5 active exceptions**: 1 (Tier-3 audit infra), 2 (validator-forced drift), 3 (SP2-blocked reverts), 4 (builder/validator move), 5 (invention deletions — new)
- **Remaining ESCALATE items**: E4 (`env-example` scan blocked), E5 (`run-claude.py` → SP12), E6 (`fork-terminal` T2-only), E7 (`pocket-pick` local reg → SP5), E8 (dashboard streamer + composable wrapper → SP9/SP3)

---

## Post-verify SP1 parity

- **Tier 1 findings closed:** 6 of 14 AUTO-REVERT items (43%)
- **Tier 2 findings closed:** 0 of deferred items (0% — future-SP validator purge on `session_start.py` is in Commit 14, blocked)
- **Exceptions documented:** 5 active
- **Inventions classified:** 9 confirmed (7 Tier-3 audit infra + 2 deletion candidates)

## SP1 round-1 status: **PARTIAL — VERIFIED**

The 6 landed commits are byte-verified clean. SP1 round 1 cannot fully close until SP2 unblocks the remaining 8 commits, at which point an SP1 resume pass re-runs them and a second verify round confirms.

---

## Next-step options

1. **Proceed to SP2 audit scout** — kick off SP2 scout-plan-build-verify cycle, which will fix the fnmatch bug + `readOnlyPaths` over-reach and allow the SP1 resume pass
2. **Decision gate on D1–D7** — resolve the 7 remaining SP1 decision-required items now, even though builds against them are blocked; this produces a complete plan for the SP1 resume pass when SP2 finishes
3. **Route remaining ESCALATE items** — E4 (one-shot `env-example` unlock for scout), E5 (SP12 routing), E6–E8 (defer to later SPs); these are cheap to resolve in this session

**Recommended order:** (2) → (3) → (1). Resolve all SP1 paperwork, then move to SP2 with SP1 fully specified.
