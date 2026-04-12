# Self-Correction Loop Test — V1

## Purpose

Verify that the ruff_validator PostToolUse hook triggers self-correction by:
1. Writing a Python file with a known ruff violation
2. Observing the block response
3. Confirming Claude auto-corrects

## Test Steps

1. Write `/tmp/sp3_test.py` containing:
   ```python
   import os,sys
   print("hello")
   ```
2. The ruff_validator.py hook should fire and output:
   `{"decision": "block", "reason": "Lint check failed: ..."}`
3. Claude receives the block reason and re-writes the file with:
   ```python
   import os
   import sys
   print("hello")
   ```
4. Ruff passes on the second write
5. Report: "Self-correction loop verified — ruff blocked, then auto-fixed"

## Expected Log Output

`.claude/hooks/validators/ruff_validator.log` shows two entries:
- First: `RESULT: BLOCK (exit code 1)`
- Second: `RESULT: PASS - Lint check successful`

## How to Run

```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/sp3_test.py"},"tool_output":{}}' | uv run .claude/hooks/validators/ruff_validator.py
```

Or interactively: ask Claude to write a Python file with `import os,sys` and observe
the PostToolUse hook block and self-correct.
