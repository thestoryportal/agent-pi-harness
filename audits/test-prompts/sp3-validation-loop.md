# Self-Correction Loop Test — SP3

## Purpose

Verify that the `ruff_validator` PostToolUse hook triggers self-correction
when invoked via `@builder` subagent dispatch:

1. Builder agent writes a Python file with a known ruff violation
2. PostToolUse hook fires and outputs `{"decision": "block", "reason": ...}`
3. Builder receives the block reason and re-writes the file
4. Ruff passes on the second write

## Scope (SP3 r1 finding)

The validator wiring lives in `agents/team/builder.md` frontmatter. It only
fires during `@builder` subagent invocations — **not** during regular
main-session edits. To verify the self-correction loop, the test must be
routed through `Use a @builder subagent to ...`.

## Fixture

The test fixture `audits/test-prompts/ruff_block_fixture.py` contains:

```python
import os, sys
print("hello")
```

This trips both `E401` (multiple imports on one line) and `F401` (unused
imports `os` and `sys`).

## Test (subagent route — fires the hook)

```
Use a @builder subagent: write the contents of
audits/test-prompts/ruff_block_fixture.py to /tmp/sp3_test.py, then if
ruff blocks, fix the imports and re-write.
```

Expected outcome: `ruff_validator.log` records one BLOCK followed by one
PASS for `/tmp/sp3_test.py`.

## Test (direct CLI — bypasses hook chain, exercises the validator alone)

```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"audits/test-prompts/ruff_block_fixture.py"},"tool_output":{}}' \
  | uv run .claude/hooks/validators/ruff_validator.py
```

Expected output:

```json
{"decision": "block", "reason": "Lint check failed:\n..."}
```

## Expected log entries

`.claude/hooks/validators/ruff_validator.log` should show:

- First invocation: `RESULT: BLOCK (exit code 1)`
- Second invocation (after fix): `RESULT: PASS - Lint check successful`

## Note on relocation

This file lived at `.claude/hooks/validators/test-prompts/validation-loop-v1.md`
through SP14 and was moved to `audits/test-prompts/sp3-validation-loop.md`
during SP3 r1 Phase D — the test prompt has no Tier 1 source (neither
`hooks-mastery` nor `agentic-finance-review` ships a `test-prompts/`
directory under `validators/`). The Tier 3 audit infrastructure carve-out
(`audits/`) is the correct home.
