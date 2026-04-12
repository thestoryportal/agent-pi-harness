---
description: "Multi-model consensus code review"
allowed-tools:
  - Read
  - Glob
  - Grep
---

# /harness-review — Multi-Model Consensus Code Review

## Purpose

Read-only analysis of the current diff against a target spec. Identifies deviations, missing requirements, convention violations, and potential issues. Fans out to validator and spec-checker subagents.

## Variables

- `$ARGUMENTS` — **Required.** Spec identifier or path to review against.

## Workflow

### Step 1 — Gather the Diff

Determine what changed:

!`git diff --stat`
!`git diff --stat --staged`

Read the full diff content for all changed files.

### Step 2 — Load the Spec

Read the full specification document. Extract:
- All requirements (explicit "must", "shall", "required" statements)
- File artifacts listed in the spec
- Naming conventions referenced

### Step 3 — Fan Out to Analysis Agents

**Convention Compliance** (via @validator):
- File naming conventions (lowercase-with-hyphens, underscores for hooks)
- Code style and lint compliance
- Schema conventions (if SQL present)

**Spec Compliance** (via @spec-checker):
- Requirements coverage
- Missing artifacts
- Deviations from spec

### Step 4 — Aggregate Report

Produce a unified review report:

## Review: [Spec ID]

### Summary
- Files changed: N
- Convention violations: N
- Spec deviations: N
- Missing requirements: N

### Priority Findings
- **P0 (critical):** ...
- **P1 (important):** ...
- **P2 (minor):** ...
- **P3 (nit):** ...

### Detailed Findings
Per-dimension analysis from each subagent.

### Recommended Action Items
Ordered list of fixes.

## Error Handling

- If no changes are detected, report "No changes to review" and stop.
- If the spec file is not found, report searched paths and stop.
