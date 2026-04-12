---
description: "Execute an implementation task with validation hooks active via builder agent"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash
agent: builder
---

# /build — Implementation Execution

## Purpose

Execute an implementation task with all validation hooks active. Delegates to the builder subagent for actual implementation. PostToolUse hooks (ruff for Python, schema validator for SQL) fire on all tool calls, providing automated quality gates.

## Variables

- `$ARGUMENTS` — **Required.** Task description or unit ID to execute.

## Workflow

### Step 1 — Understand the Task

Read the task description or spec unit carefully. If a scout output exists, load the relevant unit definition.

### Step 2 — Load Context

Read project conventions from CLAUDE.md. Read any referenced spec files.

### Step 3 — Execute Implementation

The builder agent handles execution with these constraints:
- **Python files** are linted by ruff after every write. Fix lint errors immediately.
- **SQL files** are checked for schema namespace, TIMESTAMPTZ, CHECK-not-ENUM conventions.
- File naming: lowercase-with-hyphens (hook files use underscores)

### Step 4 — Self-Validation

After creating artifacts:
1. Verify naming conventions
2. Confirm all expected files exist
3. If validation hooks blocked anything, confirm it was resolved

### Step 5 — Report

Report:
- Artifacts created/modified (exact paths)
- Validation results (pass/fail per check)
- Any warnings or deviations from spec

## Error Handling

- If validation fails after 3 self-correction attempts, report the failure and stop
- If the task is ambiguous, stop and ask. Do not make architectural decisions.
