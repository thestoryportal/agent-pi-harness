---
description: "Create implementation plan from scout output via architect agent"
argument-hint: "[scout-output or spec-path]"
agent: architect
---

# /architect — Implementation Plan Creation

## Purpose

Create a detailed implementation plan by delegating to the Architect agent. This is the
second step in the Scout-Plan-Build pipeline: `/scout` → `/architect` → `/build`.

## Variables

- `$ARGUMENTS` — **Required.** Either:
  - Path to scout output (JSON from `/scout`)
  - Path to spec section to plan against (architect will read scout-style)

## Workflow

### Step 1 — Load Scout Output

If `$ARGUMENTS` points to scout JSON output, read it directly.
If it points to a spec or the source of truth, read the relevant section and
decompose it into units (architect handles this).

### Step 2 — Load Source References

Read the source of truth at `~/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md`
for the target sub-project's feature list.

Read the relevant IndyDevDan repo snapshot at
`~/Projects/indydevdan-harness-research/research/repo-snapshots/` for actual code patterns.

### Step 3 — Delegate to Architect

The Architect agent produces the implementation plan with:
- File map (exact paths)
- Code pattern references (repo snapshot files to follow)
- Test specs (what to test, expected behavior)
- Validation criteria (how to confirm correctness)
- Unit ordering (dependency-aware)

### Step 4 — Present Plan

Output the plan for user review. The plan is consumed by `/build` for execution.

## Pipeline Usage

```
# Full Scout-Plan-Build pipeline:
/scout ~/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md
# Review scout output, then:
/architect [scout output or spec path]
# Review plan, then for each unit:
/build [unit description from plan]
# After all units built:
/harness-review ~/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md
```

## Error Handling

- If no scout output or spec is provided, stop and ask.
- If the spec section has ambiguous requirements, list blockers and stop.
- Do not make architectural decisions — flag them for user input.
