---
description: "Read a spec, identify implementation units, produce structured task list"
allowed-tools:
  - Read
  - Glob
  - Grep
---

# /scout — Spec Analysis and Task Decomposition

## Purpose

Read a specification document, identify implementation units, create an ordered task list, and output structured JSON. This is the first step in the Scout-Plan-Build pipeline.

## Variables

- `$ARGUMENTS` — **Required.** Path or identifier of the spec to analyze (e.g., `docs/specs/SPEC-H03.md` or `SPEC-H03`).
- If `$ARGUMENTS` is a short identifier, search for the full path.

## Workflow

### Step 1 — Locate and Read the Spec

Find and read the full specification document identified by `$ARGUMENTS`.
If the spec references other specs, read those as well to understand dependencies.

### Step 2 — Read Project Conventions

Read `CLAUDE.md` for non-negotiable conventions:
- Naming: lowercase-with-hyphens for files, underscores for hooks, snake_case for SQL
- Project-specific constraints

### Step 3 — Identify Implementation Units

Decompose the spec into discrete implementation units. Each unit is:
- **Atomic:** completable in a single Claude Code session
- **Testable:** has a clear validation condition
- **Ordered:** dependencies between units are explicit

For each unit, determine:
1. **ID:** Sequential within this spec (e.g., `SPEC-H03-U01`)
2. **Title:** Concise description
3. **Type:** One of `hook`, `skill`, `agent`, `command`, `config`, `test`, `script`
4. **Artifacts:** Files to create or modify (exact paths)
5. **Dependencies:** Other unit IDs that must complete first
6. **Validation:** How to confirm the unit is correct
7. **Risk:** `low` (read-only or additive), `medium` (modifies existing), `high` (destructive)

### Step 4 — Build Dependency Graph

Order units topologically. Identify:
- Critical path (longest dependency chain)
- Parallelizable groups (independent units at same dependency depth)
- External dependencies (tools that must be available)

### Step 5 — Output

Produce the task list as a structured report with:
- Total units and critical path length
- Unit list with IDs, titles, types, and risk levels
- Identified blockers or ambiguities in the spec
- Recommended execution order

## Error Handling

- If the spec file is not found, report the searched paths and stop.
- If the spec contains ambiguous requirements, list them as blockers. Do not make architectural decisions.
