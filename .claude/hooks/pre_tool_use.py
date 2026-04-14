#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""PreToolUse hook: Read/Glob/Grep zero-access protection + MCP gates (catch-all).

Bash, Edit, and Write tools are handled by their own per-tool hooks
(bash_damage_control.py, edit_damage_control.py, write_damage_control.py).
This hook catches:
  - Read, Glob, Grep — blocks access to zeroAccessPaths
  - mcp__* (ALL namespaces) — blocks arbitrary-JS primitives (execute_script,
    eval, run_code, run_script, evaluate) regardless of MCP server namespace.
    SP14 round-3 extended the gate from only mcp__claude_in_chrome__* to all
    mcp__* tools after a security review found that a second Chrome MCP
    server under a different namespace could bypass the original gate.
    All segments of the tool name are checked, not just the last, to defeat
    depth-3 bypasses like mcp__claude_in_chrome__execute_script__v2.

Exit codes: 0=allow, 2=block. This is a security-critical hook — never exit 1.
"""

import json
import os
import sys
import time
from pathlib import Path, PurePath

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
sys.path.insert(0, str(Path(PROJECT_DIR) / ".claude" / "hooks"))
try:
    import yaml
    from _base import Logger, emit_event, handle_health_check, read_stdin, run_hook
except Exception:
    sys.exit(2)

HOOK_NAME = "pre_tool_use.py"
handle_health_check(HOOK_NAME)

PROJECT_ROOT = str(Path(PROJECT_DIR).resolve())


def is_glob_pattern(pattern: str) -> bool:
    return "*" in pattern or "?" in pattern or "[" in pattern


def match_path(file_path: str, pattern: str) -> bool:
    """Match file path against pattern using path-segment-aware matching.

    SP2 AR1 (2026-04-13): uses pathlib.PurePath.match() instead of
    fnmatch.fnmatch() for glob patterns. PurePath.match() treats `/` as
    a path separator, so `.claude/hooks/*.py` does NOT match
    `.claude/hooks/utils/tts/foo.py`.
    """
    expanded_pattern = os.path.expanduser(pattern)
    normalized = os.path.normpath(file_path)
    expanded_normalized = os.path.expanduser(normalized)

    # Resolve relative patterns against project root
    if not os.path.isabs(expanded_pattern):
        abs_pattern = os.path.normpath(os.path.join(PROJECT_ROOT, expanded_pattern))
    else:
        abs_pattern = os.path.normpath(expanded_pattern)

    if is_glob_pattern(pattern):
        # Path-segment-aware glob matching via PurePath.match().
        try:
            if PurePath(expanded_normalized).match(expanded_pattern, case_sensitive=False):
                return True
            if PurePath(expanded_normalized).match(abs_pattern, case_sensitive=False):
                return True
        except ValueError:
            # Invalid pattern — fail closed
            pass
        return False
    else:
        if expanded_normalized.startswith(expanded_pattern) or expanded_normalized == expanded_pattern.rstrip("/"):
            return True
        if expanded_normalized.startswith(abs_pattern) or expanded_normalized == abs_pattern.rstrip("/"):
            return True
        return False


def check_read(tool_input: dict, rules: dict) -> tuple[str, str | None]:
    """Check Read/Glob/Grep tool inputs against zeroAccessPaths."""
    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
    pattern = tool_input.get("pattern", "")
    check_str = file_path or pattern
    if not check_str:
        return "allow", None

    for zero_path in rules.get("zeroAccessPaths", []):
        if match_path(check_str, zero_path):
            return "block", f"Read/search of protected path: {zero_path}"

    return "allow", None


# ============================================================================
# MCP TOOL GATES (SP14 rounds 4–8 hardening)
# Token-sequence matching introduced in r4. r5 added the first batch of
# single-token concatenated-name entries (executescript, runscript, runcode).
# r6 added the `*js` family (evaljs, runjs, execjs, executejs). r7 added
# the `javascript` single-token entry. r8 adds the `("java","script")`
# two-token sequence for `mcp__srv__java__script` style double-underscore
# names — low exploitability (requires hostile MCP server registration)
# but closes the last enumerated token-sequence gap.
# ============================================================================
# Any MCP tool (regardless of server namespace) whose name contains an
# arbitrary-JS execution primitive as a token sequence is blocked.
#
# Evolution:
#   r1: gated only mcp__claude_in_chrome__* by prefix; only final segment
#       suffix-checked against a set of primitives (execute_script, etc.).
#   r2: r1 review found that a depth-3 tool name like
#       mcp__claude_in_chrome__execute_script__v2 has a final segment of
#       "v2" and bypassed the suffix check. r2 switched to any-segment
#       exact-match across all __-split segments, still scoped to the
#       claude_in_chrome namespace.
#   r3: r2 review found that any other MCP server namespace evaded the
#       claude_in_chrome prefix gate, and that a single-underscore suffix
#       like execute_script_v2 still bypassed segment exact-match. r3
#       extended the gate to all mcp__* namespaces.
#   r4: r3 review found that r3's per-segment exact match still failed
#       on execute_script_v2 (suffix) and execute-script (hyphen). r4
#       introduced token-sequence matching: normalize hyphens, split on
#       underscore, look for primitive tuples as contiguous subsequences.
#       Also added single-token entries for concatenated-name variants.
#   r5: r4 review found four new delimiter-form bypasses in the round-4
#       upload patterns (curl --data-binary=@, wget --post-file <space>,
#       etc.). r5 is primarily a patterns.yaml sweep to cover both `=`
#       and ` ` delimiter forms, plus single-token MCP entries below
#       to close the concatenated-name variant (S-26).
#
# False-positive avoidance: "retrieval" contains "eval" as a substring
# but is one atomic token, so ("eval",) != ("retrieval",). "medieval"
# same logic. A legitimate MCP tool named mcp__db__retrieval is allowed.

# Each entry is a tuple of lowercase atomic tokens representing an
# arbitrary-JS primitive. A tool name matches if any of these tuples
# appears as a contiguous subsequence in the tool name's tokenization.
# Single-token entries cover concatenated-name variants (e.g.
# "executescript" with no internal separator — an unusual MCP naming
# choice that round-4 missed).
MCP_JS_EXEC_TOKEN_SEQS: frozenset[tuple[str, ...]] = frozenset({
    ("execute", "script"),
    ("run", "script"),
    ("run", "code"),
    ("java", "script"),
    ("eval",),
    ("evaluate",),
    # Concatenated-name variants (r5 + r6 + r7): MCP tool names that
    # combine the primitive into a single token with no separator.
    # Covers the `-script`, `-code`, `-js`, and `javascript` families.
    ("executescript",),
    ("runscript",),
    ("runcode",),
    ("evaljs",),
    ("runjs",),
    ("execjs",),
    ("executejs",),
    ("javascript",),
})


def _atomize(tool_name: str) -> list[str]:
    """Tokenize an MCP tool name into lowercase atomic tokens.

    Normalizes by splitting on __, then replacing - with _ within each
    segment, then splitting on _. Empty tokens are dropped. Used by
    check_mcp_tool() for token-sequence matching.
    """
    tokens: list[str] = []
    for seg in tool_name.lower().split("__"):
        for atom in seg.replace("-", "_").split("_"):
            if atom:
                tokens.append(atom)
    return tokens


def check_mcp_tool(tool_name: str) -> tuple[str, str | None]:
    """Gate mcp__* tool invocations (all namespaces).

    Blocks any tool whose atomic-token sequence contains an arbitrary-JS
    execution primitive as a contiguous subsequence. Passive MCP tools
    (navigate, click, screenshot, snapshot, etc.) pass through and are
    logged via the ALLOW emit at main()'s fallthrough.

    Round-10 hardening (V-3 + S-06): defensive length cap and non-ASCII
    rejection before atomization. A hostile MCP server could register a
    tool name with unicode homoglyphs (e.g., Cyrillic `е` U+0435 in place
    of Latin `e`) to slip past the token-sequence frozenset check, or
    with a pathological-length name to drive the inner contiguous-
    subsequence loop. Both vectors are closed here.
    """
    # Round-10 V-3: defensive length cap for pathological tool names.
    # Normal MCP tool names are short identifiers (tens of chars). A
    # 512-char cap is generous for legitimate traffic and closes the
    # pathological-input loop amplification.
    if len(tool_name) > 512:
        return (
            "block",
            f"MCP tool name exceeds 512-char cap ({len(tool_name)} chars): "
            f"{tool_name[:64]}...",
        )
    # Round-10 S-06: non-ASCII MCP tool names are either homoglyph
    # primitive-bypass attempts (e.g. `mcp__srv__еval` with Cyrillic `е`)
    # or protocol violations. JSON-RPC MCP tool names are ASCII
    # identifiers by convention. Fail closed.
    if not tool_name.isascii():
        return (
            "block",
            f"MCP tool name contains non-ASCII characters (possible "
            f"homoglyph primitive bypass): {tool_name!r}",
        )
    tokens = _atomize(tool_name)
    for seq in MCP_JS_EXEC_TOKEN_SEQS:
        n = len(seq)
        for i in range(len(tokens) - n + 1):
            if tuple(tokens[i:i + n]) == seq:
                return (
                    "block",
                    f"MCP arbitrary-JS primitive blocked: {tool_name}. "
                    f"execute_script / eval against a live browser session "
                    f"is an identity-exfiltration vector and has no allowlist.",
                )
    return "allow", None


def load_patterns() -> dict:
    patterns_path = Path(PROJECT_DIR) / ".claude" / "hooks" / "patterns.yaml"
    with open(patterns_path) as f:
        return yaml.safe_load(f)


def main():
    logger = Logger("pre_tool_use")
    start_time = time.monotonic()

    input_data = read_stdin()
    if not input_data or "tool_name" not in input_data:
        logger.log("BLOCKED: malformed or empty stdin (fail-closed)")
        emit_event("PreToolUse", HOOK_NAME, 2, {"error": "malformed stdin"})
        sys.exit(2)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # MCP tools (all namespaces): gate arbitrary-JS primitives BEFORE the
    # catch-all early exit. BLOCK emits an event and exits 2. ALLOW emits
    # an explicit PreToolUse allow event (so the pre-execution audit trail
    # is consistent even if post_tool_use later fails) and then exits 0.
    if tool_name.startswith("mcp__"):
        decision, reason = check_mcp_tool(tool_name)
        elapsed = int((time.monotonic() - start_time) * 1000)
        if decision == "block":
            payload = {"tool": tool_name, "decision": decision, "reason": reason}
            emit_event("PreToolUse", HOOK_NAME, 2, payload, elapsed)
            logger.log(f"BLOCKED: {tool_name} — {reason}")
            print(json.dumps({"error": reason}), file=sys.stderr)
            sys.exit(2)
        # ALLOW path — emit an explicit audit event so passive MCP
        # invocations always appear in the PreToolUse event stream.
        emit_event("PreToolUse", HOOK_NAME, 0, {"tool": tool_name, "decision": "allow"}, elapsed)
        logger.log(f"ALLOW: {tool_name}")
        sys.exit(0)

    # Only handle Read, Glob, Grep — other tools have their own hooks
    if tool_name not in ("Read", "Glob", "Grep"):
        sys.exit(0)

    try:
        rules = load_patterns()
    except Exception as e:
        logger.log(f"BLOCKED: patterns.yaml load failed — {e} (fail-closed)")
        emit_event("PreToolUse", HOOK_NAME, 2, {"error": f"patterns.yaml: {e}"})
        print(json.dumps({"error": f"patterns.yaml load failed: {e}"}), file=sys.stderr)
        sys.exit(2)

    decision, reason = check_read(tool_input, rules)
    elapsed = int((time.monotonic() - start_time) * 1000)

    payload = {"tool": tool_name, "decision": decision}
    if reason:
        payload["reason"] = reason

    if decision == "block":
        emit_event("PreToolUse", HOOK_NAME, 2, payload, elapsed)
        logger.log(f"BLOCKED: {tool_name} — {reason}")
        print(json.dumps({"error": reason}), file=sys.stderr)
        sys.exit(2)
    else:
        emit_event("PreToolUse", HOOK_NAME, 0, payload, elapsed)
        logger.log(f"ALLOW: {tool_name}")
        sys.exit(0)


if __name__ == "__main__":
    run_hook(main, HOOK_NAME, security_critical=True, event_type="PreToolUse")
