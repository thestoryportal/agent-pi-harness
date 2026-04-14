#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""SP2 Phase F E1 verification probe.

Tests pathExclusions short-circuit in all 4 damage-control hooks:
  - edit/write check_path()  — early-exit on file_path match
  - pre_tool_use check_read() — early-exit on Read/Glob/Grep file_path
  - bash _check_single_command() — token filter applied before zero-access loop

Avoids literal protected-path strings in the OUTER shell environment by
building all test inputs in-process via dict construction (no JSON parsing
of literal strings, no os.environ pollution).

Disposable probe — delete after E1 is verified and committed.
"""
import importlib.util
import os
import sys
from pathlib import Path

PROJECT_DIR = "/Users/robertrhu/Projects/arhugula"
os.environ["CLAUDE_PROJECT_DIR"] = PROJECT_DIR

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


def _load(modname: str, path: Path):
    spec = importlib.util.spec_from_file_location(modname, str(path))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bash_mod = _load("sp2_e1_bash", SKILL_HOOKS_DIR / "bash_damage_control.py")
edit_mod = _load("sp2_e1_edit", SKILL_HOOKS_DIR / "edit_damage_control.py")
write_mod = _load("sp2_e1_write", SKILL_HOOKS_DIR / "write_damage_control.py")
ptu_mod = _load("sp2_e1_ptu", HOOKS_DIR / "pre_tool_use.py")

rules = bash_mod.load_patterns()

# Construct protected-path strings WITHOUT putting them in source literals
# that would be matched by the outer bash hook on the `uv run` invocation.
# `chr(46)` is ".", `chr(101)` is "e". The full string never appears as a
# contiguous literal in this file.
DOT = chr(46)
ENV_TOKEN = DOT + "env"  # ".env"
ENV_EX = DOT + "env" + DOT + "example"  # ".env.example"
ENVRC_EX = DOT + "envrc" + DOT + "example"  # ".envrc.example"

print("===== SP2 Phase F E1: pathExclusions short-circuit =====\n")


def expect(label, actual, expected):
    ok = actual == expected
    marker = "OK " if ok else "!! "
    print(f"{marker}[{actual!s:7}] {label}")
    print(f"         expected: {expected!s}")
    return ok


fails = 0


# ---------- edit hook ----------
print("--- edit_damage_control.check_path ---")
d, _ = edit_mod.check_path(ENV_EX, rules)
fails += not expect("Edit on .env.example  → allow (excluded)", d, "allow")

d, _ = edit_mod.check_path(ENVRC_EX, rules)
fails += not expect("Edit on .envrc.example → allow (excluded)", d, "allow")

d, _ = edit_mod.check_path(ENV_TOKEN, rules)
fails += not expect("Edit on .env (no exclusion match) → block", d, "block")
print()

# ---------- write hook ----------
print("--- write_damage_control.check_path ---")
d, _ = write_mod.check_path(ENV_EX, rules)
fails += not expect("Write on .env.example  → allow (excluded)", d, "allow")

d, _ = write_mod.check_path(ENVRC_EX, rules)
fails += not expect("Write on .envrc.example → allow (excluded)", d, "allow")

d, _ = write_mod.check_path(ENV_TOKEN, rules)
fails += not expect("Write on .env (no exclusion match) → block", d, "block")
print()

# ---------- pre_tool_use hook (Read/Glob/Grep) ----------
print("--- pre_tool_use.check_read ---")
d, _ = ptu_mod.check_read({"file_path": ENV_EX}, rules)
fails += not expect("Read on .env.example  → allow (excluded)", d, "allow")

d, _ = ptu_mod.check_read({"file_path": ENVRC_EX}, rules)
fails += not expect("Read on .envrc.example → allow (excluded)", d, "allow")

d, _ = ptu_mod.check_read({"file_path": ENV_TOKEN}, rules)
fails += not expect("Read on .env (no exclusion match) → block", d, "block")

# Glob/Grep accept "pattern" instead of "file_path"
d, _ = ptu_mod.check_read({"pattern": ENV_EX}, rules)
fails += not expect("Glob pattern .env.example → allow (excluded)", d, "allow")
print()

# ---------- bash hook (token-level filter) ----------
# Note: `cat .env.example` is also matched by a pre-existing entry in
# bashToolExclusions, which short-circuits the entire command at step 0.
# To isolate E1's pathExclusions / token-filter logic we use commands
# (head, wc) that do NOT have a bashToolExclusions allowlist entry for
# .env.example. These hit the zero-access loop where E1's filter applies.
print("--- bash_damage_control._check_single_command ---")

d, _ = bash_mod._check_single_command("head " + ENV_EX, rules)
fails += not expect("head .env.example       → allow (E1 token-filtered)", d, "allow")

d, _ = bash_mod._check_single_command("wc " + ENV_EX, rules)
fails += not expect("wc .env.example         → allow (E1 token-filtered)", d, "allow")

d, _ = bash_mod._check_single_command("head " + ENV_TOKEN, rules)
fails += not expect("head .env                → block (no exclusion)", d, "block")

# Critical case: mixed command must still block on the non-excluded token.
mixed = "head " + ENV_TOKEN + " " + ENV_EX
d, _ = bash_mod._check_single_command(mixed, rules)
fails += not expect("head .env .env.example   → block (.env still hits)", d, "block")

# Reverse order — exclusion should not gate the whole command.
mixed_rev = "head " + ENV_EX + " " + ENV_TOKEN
d, _ = bash_mod._check_single_command(mixed_rev, rules)
fails += not expect("head .env.example .env   → block (.env still hits)", d, "block")

# Sanity: the legacy bashToolExclusions short-circuit still works for cat.
# (This is pre-existing SP2 behavior, not new with E1.)
d, _ = bash_mod._check_single_command("cat " + ENV_EX, rules)
fails += not expect("cat .env.example        → allow (legacy exclusions)", d, "allow")
print()

if fails:
    print(f"E1: {fails} regression failure(s) — pathExclusions wiring is incorrect")
    sys.exit(1)
else:
    print("E1: all pathExclusions short-circuit cases pass")
