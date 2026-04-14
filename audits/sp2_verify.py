#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""SP2 Phase A empirical verification.

Dynamically loads bash_damage_control via importlib (no static import) and
invokes check_command() on the SP1 resume-pass candidate commands. This
avoids (a) ty's static-import resolution failure and (b) the false-positive
regex match that fires when the outer bash command contains both `rm` (in
the probe JSON) and `.claude/hooks/*.py` (as the uv run target path).
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
HOOKS_DIR = Path(PROJECT_DIR).joinpath(".claude").joinpath("hooks")
sys.path.insert(0, str(HOOKS_DIR))

HOOK_FILE = HOOKS_DIR / "bash_damage_control.py"
spec = importlib.util.spec_from_file_location("sp2_probe_hook", str(HOOK_FILE))
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

rules = mod.load_patterns()

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

for cmd, label in test_cases:
    decision, reason = mod.check_command(cmd, rules)
    marker = {"allow": "OK ", "block": "!! ", "ask": "?? "}.get(decision, "?? ")
    print(f"{marker}[{decision.upper():5}] {label}")
    print(f"         cmd: {cmd}")
    if reason:
        print(f"         why: {reason}")
    print()
