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
SP_IDS=(SP1 SP2 SP3 SP4 SP5 SP6 SP7 SP8 SP9 SP10 SP11 SP12 SP13 SP14 SP15 SP16)
REQUIRED_ACK="29,14,24,28"

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

DATE="$(date -u +%Y-%m-%d)"
SUMMARY_OUT="audits/phase2-summary-${DATE}.md"

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
You are running inside an isolated E2B sandbox with the ArhuGula working
tree mounted read-only at /repo. Your job is to execute the sub-project
${sp} coder↔validator loop via the CA-U06 single-file agent.

Steps:
  1. cd /repo
  2. Load the ${sp} context bundle from audits/bundles/${sp,,}.yaml
  3. Run:
       uv run ${LOOP_SFA} \\
           --sp ${sp} \\
           --sp-manifest audits/bundles/${sp,,}.yaml \\
           --mailbox /tmp/phase2-mailbox.jsonl \\
           --max-iter 3
  4. On completion, print the mailbox contents so the host session can
     harvest it.

Do not modify any file in /repo. The sandbox mount is read-only; the
coder agent writes diffs under /tmp/coder_diffs/ only.
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
    mem_file="$HOME/.claude/projects/-Users-$(id -un)-Projects-arhugula/memory/project_${sp_lower}_r1_resume.md"
    exc_ids="$(_sp_exceptions "$sp")"

    # Build YAML scope list and exceptions list via Python for correct quoting
    python3 - <<PYEOF
import yaml, pathlib

scope_globs = "$scope".split()
exc_list   = [int(x) for x in "$exc_ids".split() if x.strip()]

bundle = {
    "sp_id":    "$sp",
    "sp_scope": scope_globs,
    "spec_refs": {
        "sot_section":  "$sot",
        "sot_path":     "$HOME/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md",
        "memory_file":  "$mem_file",
        "exceptions_md":"audits/exceptions.md",
    },
    "memory_file_excerpt": "(load memory_file for full context)",
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

declare -a PIDS=()
declare -A PID_TO_SP=()

echo "Launching ${#TARGET_SPS[@]} sandbox(es) (parallel)..."
for sp in "${TARGET_SPS[@]}"; do
    sp_lower="${sp,,}"
    PROMPT="$(make_sp_prompt "$sp")"
    CAPTURE="$FANOUT_MARKER_DIR/${sp}.log"
    (
        cd "$REPO_ROOT/apps/sandbox_workflows"
        uv run obox sandbox-fork "$REPO_URL" \
            --prompt  "$PROMPT" \
            --forks   1 \
            --branch  "$BRANCH" \
            --model   sonnet \
        >"$CAPTURE" 2>&1
    ) &
    pid=$!
    PIDS+=("$pid")
    PID_TO_SP[$pid]="$sp"
    echo "  [$sp] pid=$pid  capture=$CAPTURE"
done
echo

# E-6: wait for all sandbox pids
echo "Waiting for ${#PIDS[@]} sandbox(es) to complete..."
FAILED_PIDS=()
for pid in "${PIDS[@]}"; do
    sp="${PID_TO_SP[$pid]}"
    if wait "$pid"; then
        echo "  [$sp] pid=$pid — done (exit 0)"
    else
        rc=$?
        echo "  [$sp] pid=$pid — exit $rc" >&2
        FAILED_PIDS+=("$pid")
    fi
done
echo

# E-7: harvest mailbox lines
# Sources checked (in order):
#   a) per-SP stdout captures — agent may echo JSONL via cat or rich output
#   b) obox ForkLogger log files in apps/sandbox_agent_working_dir/logs/
#      pattern: "[TIMESTAMP] [INFO   ] [Agent] TextBlock | content={...}"
FORK_LOG_DIR="$REPO_ROOT/apps/sandbox_agent_working_dir/logs"
HARVEST_TMP="$FANOUT_MARKER_DIR/harvested.jsonl"

echo "Harvesting mailbox lines..."

for sp in "${TARGET_SPS[@]}"; do
    capture="$FANOUT_MARKER_DIR/${sp}.log"
    [[ -f "$capture" ]] || continue
    # Extract full JSON objects containing "sp":"<sp>" with a "verdict" key
    python3 - <<PYEOF >> "$HARVEST_TMP" 2>/dev/null || true
import re, json
text = open("$capture", errors="replace").read()
for m in re.finditer(r'(\{"sp"\s*:\s*"$sp"[^\n]{10,}\})', text):
    line = m.group(1).strip()
    try:
        obj = json.loads(line)
        if "verdict" in obj:
            print(json.dumps(obj))
    except Exception:
        pass
PYEOF
done

# Also scan fork log files created since we started (belt-and-suspenders)
if [[ -d "$FORK_LOG_DIR" ]]; then
    python3 - <<PYEOF >> "$HARVEST_TMP" 2>/dev/null || true
import re, json, os, pathlib
log_dir = pathlib.Path("$FORK_LOG_DIR")
marker_mtime = os.path.getmtime("$FANOUT_MARKER_DIR")
for logfile in log_dir.glob("*.log"):
    if logfile.stat().st_mtime < marker_mtime:
        continue
    text = logfile.read_text(errors="replace")
    for m in re.finditer(r'TextBlock.*?content=(\{"sp":[^\n]+\})', text, re.DOTALL):
        line = m.group(1).split("\n")[0].strip()
        try:
            obj = json.loads(line)
            if "verdict" in obj and "sp" in obj:
                print(json.dumps(obj))
        except Exception:
            pass
PYEOF
fi

# Deduplicate (last entry per SP) and append to shared mailbox
python3 - <<PYEOF
import json, pathlib, sys

harvest = pathlib.Path("$HARVEST_TMP")
if not harvest.exists():
    print("  no mailbox lines found in any capture or fork log")
    sys.exit(0)

seen: dict = {}
for line in harvest.open(errors="replace"):
    line = line.strip()
    if not line:
        continue
    try:
        obj = json.loads(line)
        sp = obj.get("sp", "")
        if sp:
            seen[sp] = obj   # last entry per SP wins
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
if [[ -f "$MAILBOX" ]]; then
    ESCALATED="$(python3 -c "
import json
rows=[json.loads(l) for l in open('$MAILBOX') if l.strip()]
print(sum(1 for r in rows if r.get('verdict') in ('fail','escalate')))
" 2>/dev/null || echo 0)"
fi

if [[ "$ESCALATED" -gt 0 ]]; then
    echo "exit 1: $ESCALATED SP(s) emitted verdict=fail or verdict=escalate"
    exit 1
fi
echo "Phase 2 fanout complete — all harvested verdicts = pass."
exit 0
