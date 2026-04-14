# Phase 2 Fanout Bugfix Spec — CA-U23 through CA-U28

**Date:** 2026-04-14
**Branch:** audit/identicality-2026-04-13
**Source:** /investigate + /debug report — 6 bugs identified in `scripts/phase2_sp_fanout.sh`,
  `apps/sandbox_workflows/src/modules/constants.py`, and the sandbox prompt architecture.
**Next available CA-U:** CA-U23 (CA-U01..CA-U22 allocated in comprehensive-audit-scout.md)

---

## Summary

The Phase 2 SP fanout (`just phase2-sp-fanout`) completed with exit 1 and zero harvested
results despite all 16 obox processes reporting success. Root cause analysis identified
6 discrete bugs. This spec defines 6 implementation units that fix them in dependency order.

**Confirmed wasted spend:** ~$5.50 from the failed run. Fixes required before any re-run.

---

## Bug Inventory (confirmed, with evidence)

| # | Bug | File:Line | Severity |
|---|-----|-----------|---------- |
| B1 | Fork log filename collision — second-precision timestamp causes 14/16 parallel obox processes to overwrite each other's log files | `constants.py:120` | Critical |
| B2 | SP manifest bundles untracked — `audits/bundles/*.yaml` not in git; sandbox clone missing them; SFA exits 2 immediately | `git status: ?? audits/bundles/` | Critical |
| B3 | Harvest regex mismatch — patterns expect bare `PHASE2_RESULT: {json}`, agent outputs markdown `` **PHASE2_RESULT**: `{json}` `` | `phase2_sp_fanout.sh:375,403` | High |
| B4 | Ephemeral mailbox — SFA writes to `/tmp/phase2-mailbox.jsonl` inside E2B sandbox; no local persist path | `phase2_sp_fanout.sh:173` | High |
| B5 | Dead fallback harvest regex — `r'PHASE2_RESULT:\\s*...'` is literal `\s*` not whitespace | `phase2_sp_fanout.sh:415` | Medium |
| B6 | Stale mailbox — `audits/phase2-mailbox.jsonl` never cleared between runs; pre-existing SP15 entry causes exit 1 | `phase2_sp_fanout.sh:426+` | Medium |

---

## Implementation Units

### CA-U23 — Commit SP manifest bundles to git

**Type:** `script`
**Risk:** `low`
**Dependencies:** none

**Problem:** `audits/bundles/sp{1..16}.yaml` are generated at fanout runtime but are
untracked. When the E2B sandbox clones the repo, the bundles directory does not exist.
The SFA exits immediately: `setup error: SP manifest not found`. The obox haiku then
burns 30+ turns improvising — producing corrupt results.

The bundles also contain local machine paths (`/Users/robertrhu/...`) in `spec_refs`
(`sot_path` and `memory_file`). These fields are informational — printed in the coder
system prompt as strings — but must be stripped before committing. A sandboxed haiku
seeing a `/Users/robertrhu/...` path may attempt to open it; those paths don't exist
in the sandbox and the resulting errors consume turns. The SFA reads only `sp_scope`
and `exceptions_subset` as structured data.

**Fix:** Before committing, patch the bundle-building Python block in the fanout script
to emit `"N/A (local-only path, not available in sandbox)"` for `sot_path` and
`memory_file`. Regenerate all 16 bundles with the patched script, then commit. Add a
pre-flight check that verifies bundles are committed and up-to-date before launching
sandboxes.

**Artifacts to modify:**
- `scripts/phase2_sp_fanout.sh` — (1) patch `spec_refs` in bundle-building Python block,
  (2) add E-0 pre-flight block: verify `git ls-files audits/bundles/ | wc -l` equals 16;
  abort if not.
- `audits/bundles/sp1.yaml … sp16.yaml` — regenerate with patched script and commit.

**Validation:**
```bash
git ls-files audits/bundles/ | wc -l   # must output 16
git show HEAD:audits/bundles/sp2.yaml  # must show sp2 bundle content
```
After fix: sandbox clone contains `audits/bundles/sp2.yaml`; `uv run ... --sp-manifest
/home/user/repo/audits/bundles/sp2.yaml` resolves correctly.

---

### CA-U24 — Fix fork log filename collision

**Type:** `script`
**Risk:** `low`
**Dependencies:** none

**Problem:** `LOG_TIMESTAMP_FORMAT = "%Y%m%d-%H%M%S"` (`constants.py:120`) has
second-level precision. The fanout bash loop launches 16 `obox --forks 1` processes
in ~1–2 seconds. `ForkLogger.__init__` (`logs.py:34`) calls `open(log_path, 'w')`
immediately at process start. Multiple processes share the same path string and each
truncates the file in write mode. Only the last writer per second survives.

**Fix:** Add microsecond precision to the timestamp format. This makes collision
effectively impossible even at 1000 parallel launches.

**Artifacts to modify:**
- `apps/sandbox_workflows/src/modules/constants.py:120`

```python
# Before
LOG_TIMESTAMP_FORMAT: Final[str] = "%Y%m%d-%H%M%S"

# After
LOG_TIMESTAMP_FORMAT: Final[str] = "%Y%m%d-%H%M%S-%f"
```

**Validation:**
```bash
# Launch 4 obox --forks 1 processes concurrently and count distinct log files
ls apps/sandbox_agent_working_dir/logs/audit-*.log | wc -l  # must equal 4
```
After fix: 16 parallel processes produce 16 distinct log files.

---

### CA-U25 — Add local temp-file result exfiltration to sandbox prompt

**Type:** `script`
**Risk:** `medium`
**Dependencies:** none (independent of CA-U24, can run in parallel)

**Problem:** The SFA writes its result to `/tmp/phase2-mailbox.jsonl` inside the
ephemeral E2B sandbox. The only exfiltration path is the step-5 echo, which lands in
the obox agent's conversation text (the fork log). With log collision (B1) and regex
mismatch (B3), no results survive to the harvest step. The architecture has no
out-of-band local persist.

**Fix:** Add step 5b to `make_sp_prompt` in the fanout script. Instruct the obox agent
to write the PHASE2_RESULT JSON to a LOCAL file using the `Write` tool. The target path
is `apps/sandbox_agent_working_dir/temp/phase2-result-${sp}.json` — inside `TEMP_DIR`,
which is in `ALLOWED_DIRECTORIES` and is not restricted by the obox hook.

Step 5b must happen BEFORE the sandbox terminates (the E2B sandbox auto-kills on
`SANDBOX_LIFETIME_IN_SECONDS = 1800` timeout).

**Artifacts to modify:**
- `scripts/phase2_sp_fanout.sh` — update `make_sp_prompt()` function

Replace step 5 in the heredoc:
```
=== REPORT ===
5. After the SFA exits, read the result from the sandbox mailbox:
     sandbox_result=$(mcp__e2b-sandbox__execute_command sandbox_id=<id> \
         command='tail -1 /tmp/phase2-mailbox.jsonl')

5b. Write the result to a LOCAL file (outside the sandbox, so it persists):
     Use the Write tool to write the JSON content to:
     apps/sandbox_agent_working_dir/temp/phase2-result-${sp}.json
     Content: the single JSON line from step 5.
     Do NOT use Bash for this — use the Write tool directly.
```

Also: create `apps/sandbox_agent_working_dir/temp/` directory at fanout start if absent.

**Validation:**
After a single-SP live run (`--sp SP1`):
```bash
ls apps/sandbox_agent_working_dir/temp/phase2-result-SP1.json  # must exist
python3 -c "import json; d=json.load(open('apps/sandbox_agent_working_dir/temp/phase2-result-SP1.json')); print(d['verdict'])"
```

---

### CA-U26 — Fix harvest to read from temp files + fix regex dead code

**Type:** `script`
**Risk:** `medium`
**Dependencies:** CA-U25 (harvest primary source is the temp files from CA-U25)

**Problem (B3):** Harvest searches fork logs for `r'PHASE2_RESULT:\s*(\{[^\n]+\})'`
but the obox agent formats its TextBlock output as markdown:
`` **PHASE2_RESULT**: `{"sp":"SP16",...}` ``. No match.

**Problem (B5):** Second fallback regex `r'PHASE2_RESULT:\\s*(\{[^\n]+\})'` — in a
Python raw string, `\\s` is a literal backslash + `s`, not the `\s` whitespace class.
This is dead code that never matches anything.

**Fix (primary):** Read result files from
`apps/sandbox_agent_working_dir/temp/phase2-result-SP*.json` as the primary harvest
source. This is reliable, format-independent, and does not depend on fork log survival.

**Fix (secondary — belt-and-suspenders for fork logs):** Update the fork log regex to
handle the markdown backtick form:
```python
# Primary: bare form
re.finditer(r'PHASE2_RESULT:\s*(\{[^\n]+\})', text)
# Secondary: markdown backtick form  **PHASE2_RESULT**: `{json}`
re.finditer(r'\*\*PHASE2_RESULT\*\*[:\s]+`(\{[^`]+\})`', text)
```

**Fix (B5):** Remove the dead second fallback regex entirely (it was trying to handle
an escaped form that doesn't appear in practice).

**Fix (dedup ordering):** Change the deduplication logic from last-wins to first-wins:
```python
# Before (last-wins — primary source gets overwritten by fallback sources)
seen[sp] = obj

# After (first-wins — primary source set first, fallback sources fill gaps only)
if sp not in seen:
    seen[sp] = obj
```

The harvest pipeline must write temp files to `HARVEST_TMP` FIRST so they are the
first-seen entry per SP. Fork log and capture file results only fill gaps where no
temp file exists.

**Artifacts to modify:**
- `scripts/phase2_sp_fanout.sh` — replace harvest section (lines ~355–424)

New harvest order:
1. Read `apps/sandbox_agent_working_dir/temp/phase2-result-SP*.json` (primary, from CA-U25) — written to HARVEST_TMP first
2. Scan fork logs with updated regex (secondary) — fills gaps
3. Scan capture files (tertiary, unchanged) — fills remaining gaps

Dedup block uses first-wins (`if sp not in seen`).

**Validation:**
```bash
# Place a test JSON file in temp and verify harvest picks it up
echo '{"sp":"SP99","verdict":"pass","iterations":1,"coder_model":"test","validator_model":"test","findings":[]}' \
    > apps/sandbox_agent_working_dir/temp/phase2-result-SP99.json
# Run harvest section manually and check HARVEST_TMP
```

---

### CA-U27 — Archive stale mailbox at live run start

**Type:** `script`
**Risk:** `low`
**Dependencies:** none

**Problem (B6):** `audits/phase2-mailbox.jsonl` retains entries from prior runs. On
the failed fanout, a pre-existing SP15 `escalate` entry from the smoke run was counted
by the exit-code check, causing exit 1 even though zero new entries were harvested.

**Fix:** At the start of each live run (after cost gate, before bundle build), if the
mailbox file exists and is non-empty, archive it to
`audits/phase2-mailbox-archived-<DATE>.jsonl` and start fresh.

**Artifacts to modify:**
- `scripts/phase2_sp_fanout.sh` — add E-0.5 block before `Building SP context bundles...`

```bash
# Archive existing mailbox if non-empty
if [[ -s "$MAILBOX" ]]; then
    ARCHIVE="audits/phase2-mailbox-archived-$(date -u +%Y-%m-%d-%H%M%S).jsonl"
    cp "$MAILBOX" "$ARCHIVE"
    : > "$MAILBOX"   # truncate (don't remove — keeps git tracking)
    echo "  archived prior mailbox → $ARCHIVE"
fi
```

**Validation:**
```bash
echo '{"sp":"old","verdict":"fail"}' > audits/phase2-mailbox.jsonl
# Run fanout --dry-run; verify mailbox is archived and empty
ls audits/phase2-mailbox-archived-*.jsonl
wc -l audits/phase2-mailbox.jsonl  # must be 0
```

---

### CA-U28 — Integration smoke test for all fixes

**Type:** `test`
**Risk:** `low`
**Dependencies:** CA-U23, CA-U24, CA-U25, CA-U26, CA-U27

**Problem:** No single test verifies all six fixes work together end-to-end before
spending money on a live re-run.

**Fix:** Extend the existing `--dry-run` path in `phase2_sp_fanout.sh` to exercise
the new pre-flight (CA-U23), temp dir creation (CA-U25), and mailbox archival (CA-U27).
Also add a single-SP live smoke with `--sp SP15` (cheapest SP to run; pre-existing
SP15 context is well-understood).

The smoke test protocol:
1. `just phase2-sp-fanout --dry-run` — confirm no errors, bundle pre-flight passes,
   temp dir would be created, mailbox archival would fire
2. Verify `git ls-files audits/bundles/ | wc -l` = 16 (CA-U23)
3. Verify `LOG_TIMESTAMP_FORMAT` contains `%f` (CA-U24)
4. Verify harvest section reads `temp/phase2-result-*.json` (CA-U26)
5. Single live SP: `just phase2-sp-fanout --sp SP15 --ack-exceptions 29,14,24,28 --confirm-cost`
6. Confirm: `apps/sandbox_agent_working_dir/temp/phase2-result-SP15.json` exists with valid JSON
7. Confirm: `audits/phase2-mailbox.jsonl` has exactly 1 entry with `"sp":"SP15"`
8. Confirm: exit code matches verdict (0=pass, 1=escalate/fail)

**Artifacts to modify:**
- `audits/ca-current-gate.txt` — update gate status after smoke passes

**Validation:** All 8 steps above pass. No API errors. Cost < $0.50 for single SP smoke.

---

## Dependency Graph

```
CA-U23 (bundles)     ──────────────────────────────────────────┐
CA-U24 (log collision) ────────────────────────────────────────┤
CA-U25 (temp exfil)  ──── CA-U26 (harvest) ───────────────────┤──── CA-U28 (smoke test)
CA-U27 (mailbox)     ──────────────────────────────────────────┘
```

- **Parallelizable group (no deps):** CA-U23, CA-U24, CA-U25, CA-U27
- **Sequential:** CA-U26 after CA-U25 (harvest reads from temp files CA-U25 creates)
- **Gate:** CA-U28 after all five

**Critical path:** CA-U25 → CA-U26 → CA-U28 (length 3)

---

## Structured JSON

```json
{
  "spec": "audits/phase2-fanout-bugfix-spec.md",
  "sub_project": "CA-Phase2-BugFix",
  "total_units": 6,
  "critical_path_length": 3,
  "units": [
    {
      "id": "CA-U23",
      "title": "Commit SP manifest bundles to git",
      "type": "script",
      "artifacts": [
        "scripts/phase2_sp_fanout.sh",
        "audits/bundles/sp1.yaml",
        "audits/bundles/sp2.yaml",
        "audits/bundles/sp3.yaml",
        "audits/bundles/sp4.yaml",
        "audits/bundles/sp5.yaml",
        "audits/bundles/sp6.yaml",
        "audits/bundles/sp7.yaml",
        "audits/bundles/sp8.yaml",
        "audits/bundles/sp9.yaml",
        "audits/bundles/sp10.yaml",
        "audits/bundles/sp11.yaml",
        "audits/bundles/sp12.yaml",
        "audits/bundles/sp13.yaml",
        "audits/bundles/sp14.yaml",
        "audits/bundles/sp15.yaml",
        "audits/bundles/sp16.yaml"
      ],
      "source_repo": "arhugula (audit infra, no upstream)",
      "dependencies": [],
      "validation": "git ls-files audits/bundles/ | wc -l outputs 16; cat audits/bundles/sp2.yaml shows sot_path: 'N/A (local-only path, not available in sandbox)'",
      "risk": "low"
    },
    {
      "id": "CA-U24",
      "title": "Fix fork log filename collision (microsecond timestamp)",
      "type": "script",
      "artifacts": [
        "apps/sandbox_workflows/src/modules/constants.py"
      ],
      "source_repo": "arhugula (audit infra, no upstream)",
      "dependencies": [],
      "validation": "LOG_TIMESTAMP_FORMAT contains %f; 4 parallel obox launches produce 4 distinct log files",
      "risk": "low"
    },
    {
      "id": "CA-U25",
      "title": "Add local temp-file result exfiltration to sandbox prompt",
      "type": "script",
      "artifacts": [
        "scripts/phase2_sp_fanout.sh"
      ],
      "source_repo": "arhugula (audit infra, no upstream)",
      "dependencies": [],
      "validation": "After single-SP live run, apps/sandbox_agent_working_dir/temp/phase2-result-SP*.json exists with valid JSON",
      "risk": "medium"
    },
    {
      "id": "CA-U26",
      "title": "Fix harvest: read temp files + fix regex dead code",
      "type": "script",
      "artifacts": [
        "scripts/phase2_sp_fanout.sh"
      ],
      "source_repo": "arhugula (audit infra, no upstream)",
      "dependencies": ["CA-U25"],
      "validation": "Placing test JSON in temp dir causes harvest to pick it up; dead regex removed; markdown regex added",
      "risk": "medium"
    },
    {
      "id": "CA-U27",
      "title": "Archive stale mailbox at live run start",
      "type": "script",
      "artifacts": [
        "scripts/phase2_sp_fanout.sh"
      ],
      "source_repo": "arhugula (audit infra, no upstream)",
      "dependencies": [],
      "validation": "Pre-populated mailbox is archived and truncated before bundle build step; dry-run exercises the path",
      "risk": "low"
    },
    {
      "id": "CA-U28",
      "title": "Integration smoke test — single SP live run validation",
      "type": "test",
      "artifacts": [
        "audits/ca-current-gate.txt"
      ],
      "source_repo": "arhugula (audit infra, no upstream)",
      "dependencies": ["CA-U23", "CA-U24", "CA-U25", "CA-U26", "CA-U27"],
      "validation": "just phase2-sp-fanout --sp SP15 --ack-exceptions 29,14,24,28 --confirm-cost exits 0 or 1; temp result file exists; mailbox has exactly 1 entry",
      "risk": "low"
    }
  ],
  "blockers": [
    {
      "id": "BLOCKER-1",
      "description": "RESOLVED. The bundle sot_path and memory_file fields contain local machine paths (/Users/robertrhu/...). These are stripped to 'N/A (local-only path, not available in sandbox)' in the patched bundle-building Python block before committing. Sandboxed agents will not attempt to open them.",
      "decision_required": "NONE — strip local paths (decided in plan-eng-review 2026-04-14)"
    }
  ],
  "recommended_order": ["CA-U23", "CA-U24", "CA-U27", "CA-U25", "CA-U26", "CA-U28"]
}
```

---

## Recommended Execution Order

```
Phase A (parallel, no deps):
  CA-U23  Commit bundles
  CA-U24  Fix log collision
  CA-U27  Archive mailbox

Phase B (after CA-U25 is unblocked):
  CA-U25  Temp exfil

Phase C (after CA-U25):
  CA-U26  Fix harvest

Phase D (gate — after all):
  CA-U28  Smoke test → re-run full 16-SP fanout if smoke passes
```

**Estimated total implementation:** ~45 min (human: ~4 hours)
**Estimated smoke test cost:** < $0.50 (single SP15 run)
**Full 16-SP re-run budget:** $5–8 (within remaining ~$9.77 balance)

---

## Notes

- Results from the failed run (SP2 escalate, SP9 pass, SP11 escalate, SP15 escalate, SP16 escalate) are **suspect** — they came from a haiku agent improvising around the missing manifest, not a clean SFA run. Treat them as invalidated. All 16 SPs need a clean re-run.
- The `smoke_run: true` field in the existing SP15 mailbox entry indicates it was from a pre-CA-U10 run (sonnet model, different schema). The archived copy will preserve it for reference.
- After CA-U28 passes, update `audits/ca-current-gate.txt` to reflect Step G status.
