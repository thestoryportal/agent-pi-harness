---
description: "Multi-model consensus code review"
allowed-tools:
  - Read
  - Glob
  - Grep
---

# /harness-review — Multi-Model Consensus Code Review

## Purpose

Read-only analysis of the current diff against a target spec. Identifies deviations, missing requirements, convention violations, and potential issues. Fans out to validator and security subagents.

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

Dispatch two specialist agents in parallel:

**Convention + Spec Compliance** (via @validator):
- File naming conventions (lowercase-with-hyphens, underscores for hooks)
- Code style and lint compliance
- Schema conventions (if SQL present)
- Error handling patterns and edge cases
- Requirements coverage against the spec / source of truth
- Missing artifacts listed in the spec
- Deviations from IndyDevDan patterns
- Source attribution verification (code matches full-clone)

**Security Review** (via @security):
- Command injection vectors (regex bypass, script escape, TOCTOU)
- Path traversal and symlink attacks
- Data exposure (secrets in logs, hook output, events)
- Hook bypass scenarios (crash behavior, role confusion)

### Step 4 — Aggregate Report

Collect findings from both agents and produce a unified review report:

## Review: [Spec ID]

### Summary
- Files changed: N
- Convention + spec violations: N (from @validator)
- Security findings: N (from @security)
- Missing requirements: N

### Priority Findings
- **P0 (critical):** ...
- **P1 (important):** ...
- **P2 (minor):** ...
- **P3 (nit):** ...

### Detailed Findings
Per-agent analysis with file paths and line references.

### Recommended Action Items
Ordered list of fixes by priority.

## Error Handling

- If no changes are detected, report "No changes to review" and stop.
- If the spec file is not found, report searched paths and stop.
