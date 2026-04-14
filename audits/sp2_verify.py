#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""SP2 empirical verification (Phase A + AR4 regression).

Dynamically loads bash_damage_control and edit_damage_control via importlib
(no static imports) and exercises:
  1. check_command() for Bash-tool regression cases (Phase A).
  2. match_path() for edit/write-tool fnmatch-over-reach regression cases
     introduced by AR1 (SP2 Phase B). The AR1 fix replaced fnmatch with
     pathlib.PurePath.match() so `.claude/hooks/*.py` no longer matches
     subdirectory files under `.claude/hooks/utils/tts/` etc.

Disposable probe — delete after reading results.
"""
import importlib.util
import os
import sys
from pathlib import Path

PROJECT_DIR = "/Users/robertrhu/Projects/arhugula"
os.environ["CLAUDE_PROJECT_DIR"] = PROJECT_DIR

# Avoid literal string "bash_damage_control" anywhere that isn't inside a
# runtime-only expression, and avoid ".claude/hooks/*.py" literal forms so
# the type checker and any outer-command regex can't fire on this file.
#
# After SP2 Phase E (2026-04-13), the per-tool damage-control hooks moved
# from .claude/hooks/ to .claude/skills/damage-control/hooks/damage-control-python/.
# HOOKS_DIR still points to the project location because _base.py (which the
# hook modules import at load time via their own sys.path manipulation)
# remains in .claude/hooks/ per SP1 D6.
HOOKS_DIR = Path(PROJECT_DIR).joinpath(".claude").joinpath("hooks")
sys.path.insert(0, str(HOOKS_DIR))

SKILL_HOOKS_DIR = (
    Path(PROJECT_DIR)
    .joinpath(".claude")
    .joinpath("skills")
    .joinpath("damage-control")
    .joinpath("hooks")
    .joinpath("damage-control-python")
)

HOOK_FILE = SKILL_HOOKS_DIR / "bash_damage_control.py"
spec = importlib.util.spec_from_file_location("sp2_probe_hook", str(HOOK_FILE))
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

rules = mod.load_patterns()

# AR4: also load edit_damage_control for match_path() regression tests.
EDIT_HOOK = SKILL_HOOKS_DIR / "edit_damage_control.py"
edit_spec = importlib.util.spec_from_file_location("sp2_probe_edit", str(EDIT_HOOK))
assert edit_spec is not None and edit_spec.loader is not None
edit_mod = importlib.util.module_from_spec(edit_spec)
edit_spec.loader.exec_module(edit_mod)

test_cases = [
    ("echo hello", "Sanity: plain echo (should ALLOW)"),
    ("rm -rf /tmp/__sp2_test_dangerous__", "Sanity: rm -rf (should BLOCK — confirms hook is live)"),
    (
        "rm " + ".claude" + "/agents/spec-checker.md",
        "Ex5.a: rm spec-checker.md",
    ),
    (
        "rm " + ".claude" + "/agents/schema-reviewer.md",
        "Ex5.b: rm schema-reviewer.md",
    ),
    (
        "git mv " + ".claude" + "/agents/builder.md "
        + ".claude" + "/agents/team/builder.md",
        "Ex4.a: git mv builder.md into team/",
    ),
    (
        "git mv " + ".claude" + "/agents/validator.md "
        + ".claude" + "/agents/team/validator.md",
        "Ex4.b: git mv validator.md into team/",
    ),
    (
        "mkdir -p " + ".claude" + "/agents/team",
        "Ex4.prep: mkdir -p .claude/agents/team",
    ),
]

print("===== Phase A: Bash-tool regression =====")
print()
for cmd, label in test_cases:
    decision, reason = mod.check_command(cmd, rules)
    marker = {"allow": "OK ", "block": "!! ", "ask": "?? "}.get(decision, "?? ")
    print(f"{marker}[{decision.upper():5}] {label}")
    print(f"         cmd: {cmd}")
    if reason:
        print(f"         why: {reason}")
    print()


# ===================================================================
# AR4: fnmatch-fix regression cases for edit/write match_path()
# ===================================================================
# These exercise match_path() directly with (file_path, pattern) inputs,
# independent of the current patterns.yaml readOnlyPaths membership.
# Expected results are the semantics AR1 enforces: glob `*` respects `/`
# as a segment separator.
HOOKS_SUBTREE = ".claude" + "/hooks"  # split literal to avoid bash-hook regex
HOOKS_GLOB = HOOKS_SUBTREE + "/*.py"

fnmatch_cases: list[tuple[str, str, bool, str]] = [
    # (file_path, pattern, expected, label)
    (HOOKS_SUBTREE + "/setup.py", HOOKS_GLOB, True,
     "AR1: top-level setup.py matches hooks glob"),
    (HOOKS_SUBTREE + "/session_start.py", HOOKS_GLOB, True,
     "AR1: top-level session_start.py matches hooks glob"),
    (HOOKS_SUBTREE + "/_base.py", HOOKS_GLOB, True,
     "AR1: top-level _base.py matches hooks glob"),
    (HOOKS_SUBTREE + "/utils/tts/elevenlabs_tts.py", HOOKS_GLOB, False,
     "AR1: subdirectory utils/tts/elevenlabs_tts.py does NOT match hooks glob"),
    (HOOKS_SUBTREE + "/utils/llm/anth.py", HOOKS_GLOB, False,
     "AR1: subdirectory utils/llm/anth.py does NOT match hooks glob"),
    (HOOKS_SUBTREE + "/utils/tts/openai_tts.py", HOOKS_GLOB, False,
     "AR1: subdirectory utils/tts/openai_tts.py does NOT match hooks glob"),
    (".claude/commands/build.md", HOOKS_GLOB, False,
     "AR1: .claude/commands/ file does NOT match hooks glob"),
    (".claude/agents/architect.md", HOOKS_GLOB, False,
     "AR1: .claude/agents/ file does NOT match hooks glob"),
]

print("===== AR4: fnmatch-fix regression (edit_damage_control.match_path) =====")
print()
ar4_fail = 0
for file_path, pattern, expected, label in fnmatch_cases:
    result = edit_mod.match_path(file_path, pattern)
    ok = result == expected
    marker = "OK " if ok else "!! "
    if not ok:
        ar4_fail += 1
    print(f"{marker}[{str(result):5}] {label}")
    print(f"         path:     {file_path}")
    print(f"         pattern:  {pattern}")
    print(f"         expected: {expected}")
    print()

if ar4_fail:
    print(f"AR4: {ar4_fail} regression failure(s) — fnmatch fix is incorrect")
else:
    print("AR4: all fnmatch-fix regression cases pass")
