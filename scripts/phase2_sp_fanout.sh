#!/usr/bin/env bash
# phase2_sp_fanout.sh — Phase 2 per-SP sandbox fan-out driver (Comprehensive Audit)
#
# Launches one E2B sandbox per sub-project via SP15 `just sbx-fork`, each
# running `sfa_coder_validator_loop.py` (CA-U06). Collects per-SP verdicts
# through the shared mailbox JSONL, then aggregates into a Phase 2 summary.
#
# This script is deliberately thin. The heavy lifting lives inside the
# per-sandbox SFA; everything here is fan-out plumbing, cost gating, and
# post-run aggregation.
#
# Usage:
#   scripts/phase2_sp_fanout.sh --dry-run            # no sandbox launches
#   scripts/phase2_sp_fanout.sh --sp SP15 --dry-run  # single SP, no launch
#   scripts/phase2_sp_fanout.sh --ack-exceptions 29,14,24,28 --confirm-cost
#
# Flags:
#   --sp SPn             Only fan out to this one SP (repeatable)
#   --dry-run            Print the invocations without launching any sandbox
#   --ack-exceptions L   Comma-separated list of exception IDs the user
#                        explicitly acknowledges (required unless --dry-run).
#                        Must exactly match 29,14,24,28 at time of writing
#                        (the four [S]-tagged runtime activation exceptions).
#   --confirm-cost       Required for live runs. Acts as a second trip on
#                        the Phase 2 cost gate (memory §10, $20 budget).
#   --help               Show this help.
#
# Exit codes:
#   0 = all fanned-out SPs emitted verdict=pass (or dry-run succeeded)
#   1 = at least one SP emitted verdict=fail or verdict=escalate
#   2 = setup error (missing CA-U06 SFA, missing credentials, gate failures)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

LOOP_SFA="agents/sfa/sfa_coder_validator_loop.py"
MAILBOX_DEFAULT="audits/phase2-mailbox.jsonl"
# CA-U25: local temp dir for per-SP result exfiltration (obox agent Write tool
# target; inside ALLOWED_DIRECTORIES of sandbox_workflows agent)
TEMP_DIR="apps/sandbox_agent_working_dir/temp"
SP_IDS=(SP1 SP2 SP3 SP4 SP5 SP6 SP7 SP8 SP9 SP10 SP11 SP12 SP13 SP14 SP15 SP16)
REQUIRED_ACK="29,14,24,28"

# Bug D fix — concurrency batching for Anthropic org quota.
# Tier 1 Anthropic quota is 450K input tokens/min. Each SFA run bursts
# ~30-50K input tokens per message across 3-5 turns. 16 concurrent runs
# exceed the quota and trigger 429s (observed in CA-U28 Step G: SP1/SP8/SP16
# all hit rate limits). Default batch size 6 keeps the 1-min burst under
# ~300K input tokens which has headroom under 450K.
# Override with --batch-size N. Pass 0 or 16 to disable batching.
DEFAULT_BATCH_SIZE=6
BATCH_SIZE="$DEFAULT_BATCH_SIZE"

DRY_RUN=false
CONFIRM_COST=false
ACK_EXCEPTIONS=""
FILTER_SPS=()
MAILBOX="$MAILBOX_DEFAULT"

usage() {
    sed -n '2,31p' "${BASH_SOURCE[0]}"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --sp)
            FILTER_SPS+=("$2")
            shift 2
            ;;
        --ack-exceptions)
            ACK_EXCEPTIONS="$2"
            shift 2
            ;;
        --confirm-cost)
            CONFIRM_COST=true
            shift
            ;;
        --mailbox)
            MAILBOX="$2"
            shift 2
            ;;
        --batch-size)
            BATCH_SIZE="$2"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo "unknown flag: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

if [[ ! -f "$LOOP_SFA" ]]; then
    echo "setup error: CA-U06 SFA not found at $LOOP_SFA" >&2
    exit 2
fi

if ! $DRY_RUN; then
    if [[ "$ACK_EXCEPTIONS" != "$REQUIRED_ACK" ]]; then
        echo "setup error: --ack-exceptions must equal $REQUIRED_ACK (got: ${ACK_EXCEPTIONS:-<empty>})" >&2
        echo "  These are the four [S]-tagged runtime activation exceptions from the ledger." >&2
        echo "  Re-read audits/exceptions.md entries 14/24/28/29 before proceeding." >&2
        exit 2
    fi
    if ! $CONFIRM_COST; then
        echo "setup error: --confirm-cost required for live runs (Phase 2 cost gate, memory §10)" >&2
        echo "  Expected spend: 16 sandboxes × ~15 min × ~\$0.05/min ≈ \$12-\$20." >&2
        exit 2
    fi
fi

# Apply --sp filter if any; otherwise fan out to all 16.
if [[ ${#FILTER_SPS[@]} -gt 0 ]]; then
    TARGET_SPS=("${FILTER_SPS[@]}")
else
    TARGET_SPS=("${SP_IDS[@]}")
fi

# Validate each requested SP is in the canonical set.
for sp in "${TARGET_SPS[@]}"; do
    found=false
    for canonical in "${SP_IDS[@]}"; do
        if [[ "$sp" == "$canonical" ]]; then
            found=true
            break
        fi
    done
    if ! $found; then
        echo "setup error: unknown sub-project '$sp' (expected SP1..SP16)" >&2
        exit 2
    fi
done

# CA-U23 / E-0: pre-flight — verify 16 SP manifest bundles are committed to git.
# The sandbox clones the repo fresh, so the bundles must exist in the tree for
# the SFA to find them at --sp-manifest. If this check fails, the fanout would
# spend money only for each SFA to exit 2 with "setup error: SP manifest not
# found". Bootstrap: regenerate bundles and commit them before re-running.
_committed_bundles=$(git ls-files audits/bundles/ 2>/dev/null | wc -l | tr -d ' ')
if [[ "$_committed_bundles" != "16" ]]; then
    echo "setup error: expected 16 committed SP bundles in audits/bundles/, found $_committed_bundles" >&2
    echo "  First-time bootstrap:" >&2
    echo "    1. Regenerate bundles (run this script live once, or invoke the" >&2
    echo "       bundle-building Python block manually)" >&2
    echo "    2. git add audits/bundles/ && git commit" >&2
    exit 2
fi

DATE="$(date -u +%Y-%m-%d)"
SUMMARY_OUT="audits/phase2-summary-${DATE}.md"

# Detect branch early so make_sp_prompt can reference it in both dry-run and live modes.
BRANCH="$(git branch --show-current 2>/dev/null)" || BRANCH="main"

echo "=== Phase 2 SP fan-out ==="
echo "  mode:         $([ $DRY_RUN = true ] && echo 'DRY RUN' || echo 'LIVE')"
echo "  sps:          ${TARGET_SPS[*]}"
echo "  mailbox:      $MAILBOX"
echo "  summary out:  $SUMMARY_OUT"
echo "  loop SFA:     $LOOP_SFA"
echo

# Construct per-SP prompts. Each prompt instructs the sandboxed Claude Code
# session to run the loop SFA for its SP and append the verdict to the
# mailbox. The mailbox path is sandbox-local; CA-U10 will add a post-run
# step that copies it back out.
make_sp_prompt() {
    local sp="$1"
    cat <<EOF
=== OBOX AGENT DIRECTIVE — Phase 2 Comprehensive Audit for ${sp} ===

You are running ONE sub-project audit inside an E2B cloud sandbox.
This is a CONSTRAINT-FIRST directive. Deviation is not permitted.

=== HARD CONSTRAINTS (read these twice before acting) ===

C1. TOOL USE — You MUST ONLY use these tool families:
    - mcp__e2b-sandbox__* for ALL operations inside the sandbox.
    - Write / Read / Edit for the ONE local file exfiltration step (step 5).
    - Glob / Grep / TodoWrite for read-only helpers if needed.
    You are NOT allowed to use: Bash, Skill, SlashCommand, Task, WebFetch,
    WebSearch. The obox hook enforces this at the tool-call layer; attempts
    will return an error.

C2. NO IMPROVISATION — If anything fails (rate limit, missing env, clone
    failure, SFA non-zero exit), you MUST:
      (a) Write an error result to the exfil path (step 5) with
          verdict="escalate" and escalate_reason=<what failed>
      (b) Stop. Do not retry with different models, CLI flags, or env vars.
      (c) Do not read any host files outside ALLOWED_DIRECTORIES.
      (d) Do not extract or set ANTHROPIC_API_KEY, E2B_API_KEY, or any other
          credential from the host environment. The sandbox inherits these
          via auto-injection.

C3. NO HOST FILE WRITES — You MUST NOT write, append, rm, mv, or otherwise
    modify any file on the host filesystem EXCEPT the one exfil file in
    step 5. The Write tool is the only path permitted for host writes.

C4. EXACT FILENAMES — The exfil file MUST be named exactly
    phase2-result-${sp}.json. Wrong filenames are dropped by the host
    harvest. No variations, no abbreviations.

C5. NO CLI FLAG CHANGES — The SFA invocation in step 4 is frozen. You MUST
    NOT add --coder-model, --validator-model, --max-iter, or any other flag
    beyond those listed below.

=== STEP 1 — Create the sandbox (MCP tool, with warmup retry) ===

Call: mcp__e2b-sandbox__create_sandbox(template='base', timeout=1800)

Pass timeout as an INTEGER (1800), not a string ('1800'). The result
contains a sandbox_id (look for it in the output text). Remember it for
all subsequent steps.

MCP WARMUP RETRY — KNOWN STARTUP RACE:
  If you get "Error: No such tool available: mcp__e2b-sandbox__create_sandbox"
  on the FIRST call, that is a known MCP server startup race (the MCP
  subprocess is still registering its tools when you made the call). You
  are EXPLICITLY PERMITTED to retry the create_sandbox call up to TWO more
  times. This is the only exception to C2 (no improvisation) — the retry
  target MUST be the same create_sandbox tool with the same arguments.
  Do NOT use init_sandbox (it is not exposed to the agent tool registry).
  Do NOT fall back to Bash, Skill, or any other path.

  If create_sandbox still returns "No such tool available" after 3 total
  attempts, go directly to STEP 6 and write an error exfil.

You MUST NOT call the 'agent-sandboxes' Skill or run 'sbx init' via Bash.
The MCP server layer auto-injects ANTHROPIC_API_KEY and OPENAI_API_KEY
from its own process environment regardless of which sandbox-creation
tool is called (verified at server.py:160).

=== STEP 2 — Clone the repo and install uv (MCP execute_command) ===

Call: mcp__e2b-sandbox__execute_command(sandbox_id=<id>, command='<cmd>')
where <cmd> is:

  git clone https://github.com/thestoryportal/agent-pi-harness.git \\
      --branch ${BRANCH} /home/user/repo 2>&1 | tail -5 && \\
  curl -LsSf https://astral.sh/uv/install.sh | sh 2>&1 | tail -3

Verify:
  mcp__e2b-sandbox__execute_command(sandbox_id=<id>, command='which /home/user/.local/bin/uv && ls /home/user/repo/audits/bundles/${sp,,}.yaml')

If either of these verification calls fails, go to step 6 (error exfil).

=== STEP 3 — Run the SFA (MCP execute_command, frozen flags) ===

Call: mcp__e2b-sandbox__execute_command(sandbox_id=<id>, command='<cmd>')
where <cmd> is EXACTLY this (no added flags, no model overrides):

  export PATH="/home/user/.local/bin:\$PATH" && \\
  cd /home/user/repo && \\
  uv run ${LOOP_SFA} \\
      --sp ${sp} \\
      --sp-manifest /home/user/repo/audits/bundles/${sp,,}.yaml \\
      --mailbox /tmp/phase2-mailbox.jsonl \\
      --max-iter 3

This is a LIVE audit. Do NOT add --dry-run.

=== STEP 4 — Capture the verdict (MCP execute_command, read mailbox) ===

Call: mcp__e2b-sandbox__execute_command(sandbox_id=<id>,
                                         command='cat /tmp/phase2-mailbox.jsonl')
The output is one line of JSON. Call this JSON "VERDICT".

=== STEP 5 — Exfil VERDICT to the host via Write tool ===

You MUST use the Write tool. You MUST NOT use Bash. You MUST NOT use any
mcp__e2b-sandbox__ tool for this step (that target path is OUTSIDE the
sandbox, on the host filesystem).

Call: Write(file_path='temp/phase2-result-${sp}.json',
            content='<VERDICT from step 4, verbatim, no wrapping>')

If the Write call fails (path validation error, etc.), DO NOT improvise
with Bash. Report the failure in your final text response and stop.

=== STEP 6 — Error exfil (only if an earlier step failed) ===

If ANY earlier step failed irrecoverably (sandbox init fail, clone fail,
SFA non-zero exit, rate limit exhaustion), write an error result to the
same exfil path:

Call: Write(file_path='temp/phase2-result-${sp}.json',
            content='{"sp":"${sp}","verdict":"escalate","iterations":0,"coder_model":"unknown","validator_model":"unknown","findings":[],"escalate_reason":"<short reason>","timestamp":"<iso8601>","dry_run":false}')

Then stop. Do not retry. Do not improvise.

=== VERIFICATION ===

After step 5 (or step 6), your work is DONE. You may call kill_sandbox to
free the resource but this is optional (the sandbox auto-terminates at
1800s timeout). Report completion in a final text response.

The host fanout script harvests from exactly one place:
  temp/phase2-result-${sp}.json
If that file does not exist or contains wrong JSON, the host counts this
SP as "no verdict" and reports it as a harvest miss.
EOF
}

if $DRY_RUN; then
    echo "--- DRY RUN: would invoke for each SP ---"
    for sp in "${TARGET_SPS[@]}"; do
        echo
        echo "[${sp}] just sbx-fork <repo-url> <per-sp-prompt> 1"
        echo "  prompt preview (first line): $(make_sp_prompt "$sp" | head -1)"
    done
    echo
    echo "dry run complete — no sandboxes launched, no mailbox writes"
    exit 0
fi

# === Live fanout (CA-U10) ============================================================

# E-1: auto-detect repo URL and branch
REPO_URL="$(git remote get-url origin 2>/dev/null)" || {
    echo "setup error: could not determine remote origin URL (is this a git repo?)" >&2
    exit 2
}
BRANCH="$(git branch --show-current 2>/dev/null)" || {
    echo "setup error: not on a named branch (detached HEAD?)" >&2
    exit 2
}
echo "  repo:    $REPO_URL"
echo "  branch:  $BRANCH"
echo

# E-2: confirm branch is pushed to origin (sbx-fork clones from remote)
echo "Verifying branch is pushed to origin..."
git fetch origin --quiet 2>/dev/null || {
    echo "setup error: cannot reach origin — check network / credentials" >&2
    exit 2
}
if ! git merge-base --is-ancestor HEAD "origin/$BRANCH" 2>/dev/null; then
    LOCAL="$(git rev-parse --short HEAD)"
    REMOTE="$(git rev-parse --short "origin/$BRANCH" 2>/dev/null || echo '<not found>')"
    echo "setup error: HEAD ($LOCAL) is not yet pushed to origin/$BRANCH ($REMOTE)" >&2
    echo "  Push before launching sandboxes: git push -u origin $BRANCH" >&2
    exit 2
fi
echo "  origin/$BRANCH is up-to-date — OK"
echo

# CA-U27 / E-2.5: archive any stale mailbox entries from prior runs so the
# final exit-code check only sees verdicts from this run. Truncate (not
# delete) to keep git tracking stable.
if [[ -s "$MAILBOX" ]]; then
    ARCHIVE="audits/phase2-mailbox-archived-$(date -u +%Y-%m-%d-%H%M%S).jsonl"
    cp "$MAILBOX" "$ARCHIVE"
    : > "$MAILBOX"
    echo "Archived prior mailbox → $ARCHIVE"
    echo
fi

# CA-U25 / E-2.6: ensure the local temp dir exists for per-SP result
# exfiltration. The obox agent writes phase2-result-<sp>.json here via the
# Write tool (path is inside ALLOWED_DIRECTORIES of the sandbox_workflows
# agent). Harvest reads from here as the primary source.
mkdir -p "$TEMP_DIR"

# CA-U28-StageG-pass3: clean stale phase2-result-SP*.json files from prior
# runs. The mtime-sentinel harvest filter handles staleness at read time,
# but an agent that fails to Write a new file can accidentally "update"
# (via Read+Edit) a stale file and confuse the harvest. Truncate to keep
# the same inode if possible, otherwise remove.
for _stale in "$TEMP_DIR"/phase2-result-SP*.json; do
    [[ -f "$_stale" ]] || continue
    : > "$_stale"
done

# E-3: create per-SP context bundles at audits/bundles/<sp>.yaml
mkdir -p audits/bundles

_sp_scope() {
    case "$1" in
        SP1)  echo ".claude/**";;
        SP2)  echo ".claude/skills/damage-control/**";;
        SP3)  echo ".claude/hooks/validators/**";;
        SP4)  echo "mcp/just-prompt/**";;
        SP5)  echo "mcp/pocket-pick/**";;
        SP6)  echo "~/.claude/skills/library/**";;
        SP7)  echo "agents/sfa/**";;
        SP8)  echo "apps/drive/** apps/listen/**";;
        SP9)  echo ".claude/commands/infinite.md .claude/commands/harness-review.md .claude/agents/meta-agent.md";;
        SP10) echo "apps/dropzone/**";;
        SP11) echo "apps/prompt-testing/**";;
        SP12) echo "apps/direct/** apps/drive/** apps/listen/**";;
        SP13) echo "apps/steer/** .claude/skills/steer/**";;
        SP14) echo ".claude/skills/claude-bowser/** .claude/commands/bowser/**";;
        SP15) echo "apps/sandbox_workflows/** apps/sandbox_cli/** apps/sandbox_mcp/**";;
        SP16) echo "apps/voice/**";;
        *)    echo ".";;
    esac
}

_sp_sot_section() {
    local n="${1#SP}"
    printf "§4.%d" "$n"
}

_sp_exceptions() {
    case "$1" in
        SP1)  echo "1 2 3 4 5 6 7 8 9 10";;
        SP2)  echo "14 15 16";;
        SP3)  echo "17";;
        SP4)  echo "18";;
        SP5)  echo "19";;
        SP6)  echo "19";;
        SP7)  echo "5 18";;
        SP8)  echo "20";;
        SP9)  echo "1 9";;
        SP10) echo "";;
        SP11) echo "21";;
        SP12) echo "22 23";;
        SP13) echo "24";;
        SP14) echo "25";;
        SP15) echo "26 28 29";;
        SP16) echo "27 28";;
        *)    echo "";;
    esac
}

echo "Building SP context bundles..."
for sp in "${TARGET_SPS[@]}"; do
    sp_lower="${sp,,}"
    bundle="audits/bundles/${sp_lower}.yaml"
    scope="$(_sp_scope "$sp")"
    sot="$(_sp_sot_section "$sp")"
    exc_ids="$(_sp_exceptions "$sp")"

    # CA-U23: spec_refs.sot_path / memory_file stripped to an explicit sentinel.
    # These used to be local machine paths ($HOME/...) which the sandboxed SFA
    # would attempt to open (and fail). The SFA only consumes sp_scope and
    # exceptions_subset as structured data; spec_refs is informational.
    python3 - <<PYEOF
import yaml, pathlib

scope_globs = "$scope".split()
exc_list   = [int(x) for x in "$exc_ids".split() if x.strip()]

bundle = {
    "sp_id":    "$sp",
    "sp_scope": scope_globs,
    "spec_refs": {
        "sot_section":  "$sot",
        "sot_path":     "N/A (local-only path, not available in sandbox)",
        "memory_file":  "N/A (local-only path, not available in sandbox)",
        "exceptions_md":"audits/exceptions.md",
    },
    "memory_file_excerpt": "(memory file is local-only; load memory via host)",
    "exceptions_subset":   exc_list,
}
pathlib.Path("$bundle").write_text(yaml.safe_dump(bundle, default_flow_style=False, sort_keys=False))
print(f"  wrote $bundle")
PYEOF
done
echo

# E-4 / E-5: background-launch one obox sandbox per SP, capture per-SP stdout
FANOUT_MARKER_DIR="/tmp/phase2-fanout-$$"
mkdir -p "$FANOUT_MARKER_DIR"
# CA-U26 fix: capture a stable "run start" timestamp via a sentinel file whose
# mtime never changes after creation. Using the FANOUT_MARKER_DIR's own mtime
# is racy — the dir's mtime updates each time a file is added to it (e.g.,
# harvested.jsonl during harvest), so any filter comparing file mtimes against
# the dir mtime at harvest time would incorrectly drop files that were written
# earlier inside the same run.
touch "$FANOUT_MARKER_DIR/.start-marker"
RUN_START_MARKER="$FANOUT_MARKER_DIR/.start-marker"

declare -a ALL_PIDS=()
declare -A PID_TO_SP=()
FAILED_PIDS=()

# Resolve effective batch size. 0 or >= target count means "launch all at once".
_target_count=${#TARGET_SPS[@]}
if [[ "$BATCH_SIZE" -le 0 ]] || [[ "$BATCH_SIZE" -ge "$_target_count" ]]; then
    _effective_batch=$_target_count
else
    _effective_batch=$BATCH_SIZE
fi

echo "Launching ${_target_count} sandbox(es) in batches of ${_effective_batch}..."
echo "  (Bug D: Anthropic org quota ~450K input tokens/min — batching"
echo "   prevents 16-way burst from hitting 429 rate limits)"
echo

_batch_num=0
_idx=0
while [[ $_idx -lt $_target_count ]]; do
    _batch_num=$((_batch_num + 1))
    _batch_end=$((_idx + _effective_batch))
    if [[ $_batch_end -gt $_target_count ]]; then
        _batch_end=$_target_count
    fi
    echo "─── Batch ${_batch_num}: SPs ${_idx}..$((_batch_end - 1)) (of $((_target_count - 1))) ───"

    declare -a _batch_pids=()
    while [[ $_idx -lt $_batch_end ]]; do
        sp="${TARGET_SPS[$_idx]}"
        sp_lower="${sp,,}"
        PROMPT="$(make_sp_prompt "$sp")"
        CAPTURE="$FANOUT_MARKER_DIR/${sp}.log"
        (
            cd "$REPO_ROOT/apps/sandbox_workflows"
            uv run obox "$REPO_URL" \
                --prompt  "$PROMPT" \
                --forks   1 \
                --branch  "$BRANCH" \
                --model   haiku \
            >"$CAPTURE" 2>&1
        ) &
        pid=$!
        _batch_pids+=("$pid")
        ALL_PIDS+=("$pid")
        PID_TO_SP[$pid]="$sp"
        echo "  [${sp}] pid=${pid}  capture=${CAPTURE}"
        _idx=$((_idx + 1))
    done

    # Wait for the batch to finish before launching the next one.
    echo "  (waiting for batch ${_batch_num} to complete...)"
    for pid in "${_batch_pids[@]}"; do
        sp="${PID_TO_SP[$pid]}"
        if wait "$pid"; then
            echo "  [${sp}] pid=${pid} — done (exit 0)"
        else
            rc=$?
            echo "  [${sp}] pid=${pid} — exit ${rc}" >&2
            FAILED_PIDS+=("$pid")
        fi
    done
    unset _batch_pids
    echo
done

# Keep PIDS alias for downstream harvest block
PIDS=("${ALL_PIDS[@]}")

# E-7: harvest mailbox lines (CA-U26).
# Sources checked (in this order — FIRST-wins dedup so the primary source
# takes precedence over the fallbacks):
#   1) LOCAL temp result files written by the obox agent via Write tool:
#      $TEMP_DIR/phase2-result-SP*.json (CA-U25 exfiltration path, primary).
#      Filtered by mtime > $FANOUT_MARKER_DIR to ignore stale files.
#   2) Fork log files in apps/sandbox_agent_working_dir/logs/ — sentinel line
#      "PHASE2_RESULT: {...}" in TextBlock content. Matches both bare and
#      markdown backtick forms (agent TextBlock may use **PHASE2_RESULT**: `...`).
#   3) Per-SP stdout captures in $FANOUT_MARKER_DIR — same sentinel patterns.
FORK_LOG_DIR="$REPO_ROOT/apps/sandbox_agent_working_dir/logs"
HARVEST_TMP="$FANOUT_MARKER_DIR/harvested.jsonl"

echo "Harvesting mailbox lines..."

# Source 1: LOCAL temp files (primary — CA-U25 exfiltration).
python3 - <<PYEOF >> "$HARVEST_TMP" 2>/dev/null || true
import json, os, pathlib
temp_dir = pathlib.Path("$TEMP_DIR")
# Use the stable sentinel mtime, not the marker dir mtime (dir mtime updates
# whenever files are added, e.g. harvested.jsonl during harvest).
marker_mtime = os.path.getmtime("$RUN_START_MARKER")
if temp_dir.exists():
    for result_file in sorted(temp_dir.glob("phase2-result-SP*.json")):
        if result_file.stat().st_mtime < marker_mtime:
            continue
        try:
            obj = json.loads(result_file.read_text(errors="replace").strip())
            if "verdict" in obj and "sp" in obj:
                print(json.dumps(obj))
        except Exception:
            pass
PYEOF

# Source 2: fork log files created since we started (secondary).
if [[ -d "$FORK_LOG_DIR" ]]; then
    python3 - <<PYEOF >> "$HARVEST_TMP" 2>/dev/null || true
import re, json, os, pathlib
log_dir = pathlib.Path("$FORK_LOG_DIR")
# Stable sentinel mtime (see Source 1 comment above).
marker_mtime = os.path.getmtime("$RUN_START_MARKER")
for logfile in log_dir.glob("*.log"):
    if logfile.stat().st_mtime < marker_mtime:
        continue
    text = logfile.read_text(errors="replace")

    # Bare form: PHASE2_RESULT: {"sp":"SPx", ...}
    for m in re.finditer(r'PHASE2_RESULT:\s*(\{[^\n]+\})', text):
        raw = m.group(1).strip()
        try:
            obj = json.loads(raw)
            if "verdict" in obj and "sp" in obj:
                print(json.dumps(obj))
        except Exception:
            pass

    # Markdown backtick form: **PHASE2_RESULT**: \`{"sp":"SPx", ...}\`
    for m in re.finditer(r'\*\*PHASE2_RESULT\*\*[:\s]+\`(\{[^\`]+\})\`', text):
        raw = m.group(1).strip()
        try:
            obj = json.loads(raw)
            if "verdict" in obj and "sp" in obj:
                print(json.dumps(obj))
        except Exception:
            pass
PYEOF
fi

# Source 3: per-SP stdout captures (tertiary).
for sp in "${TARGET_SPS[@]}"; do
    capture="$FANOUT_MARKER_DIR/${sp}.log"
    [[ -f "$capture" ]] || continue
    python3 - <<PYEOF >> "$HARVEST_TMP" 2>/dev/null || true
import re, json
text = open("$capture", errors="replace").read()

# Bare form
for m in re.finditer(r'PHASE2_RESULT:\s*(\{[^\n]+\})', text):
    line = m.group(1).strip()
    try:
        obj = json.loads(line)
        if "verdict" in obj and "sp" in obj:
            print(json.dumps(obj))
    except Exception:
        pass

# Markdown backtick form
for m in re.finditer(r'\*\*PHASE2_RESULT\*\*[:\s]+\`(\{[^\`]+\})\`', text):
    line = m.group(1).strip()
    try:
        obj = json.loads(line)
        if "verdict" in obj and "sp" in obj:
            print(json.dumps(obj))
    except Exception:
        pass
PYEOF
done

# Deduplicate (FIRST entry per SP wins — primary source from temp files is
# written to HARVEST_TMP first, so it takes precedence over fork log and
# capture fallbacks).
python3 - <<PYEOF
import json, pathlib, sys

harvest = pathlib.Path("$HARVEST_TMP")
if not harvest.exists():
    print("  no mailbox lines found in temp files, fork logs, or captures")
    sys.exit(0)

seen: dict = {}
for line in harvest.open(errors="replace"):
    line = line.strip()
    if not line:
        continue
    try:
        obj = json.loads(line)
        sp = obj.get("sp", "")
        if sp and sp not in seen:
            seen[sp] = obj   # first entry per SP wins (primary = temp files)
    except Exception:
        pass

if not seen:
    print("  no parseable mailbox entries found")
    sys.exit(0)

mailbox = pathlib.Path("$MAILBOX")
mailbox.parent.mkdir(parents=True, exist_ok=True)
with mailbox.open("a") as fh:
    for obj in seen.values():
        fh.write(json.dumps(obj, separators=(",", ":")) + "\n")
print(f"  harvested {len(seen)} line(s) → $MAILBOX")
PYEOF
echo

# E-8: generate phase2 summary markdown
echo "Generating $SUMMARY_OUT..."
python3 - <<PYEOF
import json, pathlib, sys
from collections import defaultdict

target_sps = "$( IFS=' '; echo "${TARGET_SPS[*]}" )".split()
mailbox = pathlib.Path("$MAILBOX")

rows = []
if mailbox.exists():
    for line in mailbox.open(errors="replace"):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            pass

harvested_sps = {r["sp"] for r in rows}
by_verdict = defaultdict(list)
for r in rows:
    by_verdict[r.get("verdict", "unknown")].append(r["sp"])

out = [
    "# Phase 2 SP Fan-out Summary",
    "",
    f"**Date:** $DATE",
    f"**Branch:** $BRANCH",
    f"**SPs targeted:** {len(target_sps)}",
    f"**Mailbox entries:** {len(rows)}",
    "",
    "## Results by verdict", "",
]
for verdict in ("pass", "fail", "escalate"):
    sps = sorted(by_verdict.get(verdict, []))
    out.append(f"### {verdict.upper()} ({len(sps)})")
    if sps:
        for sp in sps:
            r = next((x for x in rows if x["sp"] == sp), {})
            nf = len(r.get("findings", []))
            ni = r.get("iterations", 0)
            out.append(f"- **{sp}** — {ni} iter(s), {nf} finding(s)")
    else:
        out.append("- (none)")
    out.append("")

missing = [sp for sp in target_sps if sp not in harvested_sps]
if missing:
    out += ["## No verdict (sandbox may have failed or mailbox not harvested)", ""]
    for sp in missing:
        out.append(f"- **{sp}** — check /tmp/phase2-fanout-*/{ sp }.log")
    out.append("")

out += ["## Per-SP details", ""]
for r in sorted(rows, key=lambda x: x["sp"]):
    sp = r["sp"]
    verdict = r.get("verdict", "?").upper()
    findings = r.get("findings", [])
    out += [
        f"### {sp} — {verdict}",
        f"- Iterations: {r.get('iterations', 0)}",
        f"- Coder model: {r.get('coder_model', '?')}",
        f"- Validator model: {r.get('validator_model', '?')}",
    ]
    if r.get("escalate_reason"):
        out.append(f"- Escalate reason: {r['escalate_reason']}")
    if findings:
        out.append(f"- Findings ({len(findings)}):")
        for f in findings[:10]:
            sev = f.get("severity", "?")
            loc = f"{f.get('file','?')}:{f.get('line', 0)}"
            ev  = str(f.get("evidence", ""))[:80]
            out.append(f"  - [{sev}] {loc} — {ev}")
    out.append("")

pathlib.Path("$SUMMARY_OUT").write_text("\n".join(out))
print(f"  wrote {len(rows)}-SP summary → $SUMMARY_OUT")
PYEOF
echo

# E-9: final exit code
if [[ ${#FAILED_PIDS[@]} -gt 0 ]]; then
    echo "⚠  ${#FAILED_PIDS[@]} sandbox process(es) exited nonzero — check per-SP capture logs"
fi

ESCALATED=0
TOTAL_MAILBOX=0
if [[ -f "$MAILBOX" ]]; then
    read TOTAL_MAILBOX ESCALATED < <(python3 -c "
import json
rows=[json.loads(l) for l in open('$MAILBOX') if l.strip()]
print(len(rows), sum(1 for r in rows if r.get('verdict') in ('fail','escalate')))
" 2>/dev/null || echo "0 0")
fi

# CA-U28 fix: an empty harvest is a setup/harvest error, not "all pass".
# If we targeted N SPs and harvested 0 entries, something broke between the
# sandbox and the mailbox — do not lie about success.
if [[ "$TOTAL_MAILBOX" -eq 0 ]]; then
    echo "exit 2: harvested 0 mailbox entries from ${#TARGET_SPS[@]} targeted SP(s) — harvest failure" >&2
    echo "  Check: apps/sandbox_agent_working_dir/temp/phase2-result-SP*.json and fork logs" >&2
    exit 2
fi

if [[ "$TOTAL_MAILBOX" -lt "${#TARGET_SPS[@]}" ]]; then
    MISSING=$(( ${#TARGET_SPS[@]} - TOTAL_MAILBOX ))
    echo "⚠  harvested $TOTAL_MAILBOX mailbox entries from ${#TARGET_SPS[@]} targeted SP(s) — $MISSING missing"
fi

if [[ "$ESCALATED" -gt 0 ]]; then
    echo "exit 1: $ESCALATED SP(s) emitted verdict=fail or verdict=escalate"
    exit 1
fi
echo "Phase 2 fanout complete — all $TOTAL_MAILBOX harvested verdict(s) = pass."
exit 0
