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

# Live path: stubbed until CA-U10. Re-confirms the hard stop documented in
# memory §10 rather than launching sandboxes. CA-U10 replaces this block
# with the actual `just sbx-fork ... &` + `wait` fanout + mailbox harvest.
echo "LIVE MODE BLOCKED — CA-U10 (Phase 2 execution) has not landed." >&2
echo "  This script intentionally does NOT launch sandboxes yet." >&2
echo "  The ack-exceptions + confirm-cost gates are verified; CA-U10 will" >&2
echo "  replace this block with the real fanout." >&2
exit 2
