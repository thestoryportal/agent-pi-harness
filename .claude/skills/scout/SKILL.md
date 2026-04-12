---
name: scout
description: Read a spec, identify implementation units, produce structured task list with dependency graph. First step in Scout-Plan-Build pipeline. Keywords - spec, decompose, tasks, dependencies, analysis.
allowed-tools: Read, Glob, Grep
---

# Scout — Spec Analysis and Task Decomposition

## Purpose

Read a specification document, identify implementation units, create an ordered task list, and output structured JSON. This is the first step in the Scout-Plan-Build pipeline.

## Variables

- `$ARGUMENTS` — **Required.** Path to the spec or source of truth section to analyze.

## Workflow

### Step 1 — Locate and Read the Spec

Find and read the full specification document identified by `$ARGUMENTS`.
If the spec references source repos, read the relevant repo snapshot in
`~/Projects/indydevdan-harness-research/research/repo-snapshots/` for actual code patterns.

### Step 2 — Read Project Conventions

Read `CLAUDE.md` for:
- Implementation rules (mandatory checks)
- Naming conventions
- Source of truth reference
- Current sub-project status

### Step 3 — Identify Implementation Units

Decompose the spec into discrete implementation units. Each unit is:
- **Atomic:** completable in a single Claude Code session
- **Testable:** has a clear validation condition
- **Ordered:** dependencies between units are explicit

For each unit, determine:
1. **id:** Sequential (e.g., `SP2-U01`)
2. **title:** Concise description
3. **type:** One of `hook`, `skill`, `agent`, `command`, `config`, `test`, `script`
4. **artifacts:** Files to create or modify (exact paths)
5. **source_repo:** IndyDevDan repo to reference for patterns
6. **dependencies:** Other unit IDs that must complete first
7. **validation:** How to confirm the unit is correct
8. **risk:** `low` (additive), `medium` (modifies existing), `high` (destructive or security)

### Step 4 — Build Dependency Graph

Order units topologically. Identify:
- Critical path (longest dependency chain)
- Parallelizable groups (independent units at same depth)
- External dependencies (tools that must be available)

### Step 5 — Output Structured JSON

Produce the task list as JSON for downstream consumption by `/plan` and `/build`:

```json
{
  "spec": "path/to/spec",
  "sub_project": "SP2",
  "total_units": 6,
  "critical_path_length": 3,
  "units": [
    {
      "id": "SP2-U01",
      "title": "Create patterns.yaml rule engine",
      "type": "config",
      "artifacts": [".claude/hooks/patterns.yaml"],
      "source_repo": "claude-code-damage-control",
      "dependencies": [],
      "validation": "patterns.yaml loads without error, rules match damage-control format",
      "risk": "medium"
    }
  ],
  "blockers": [],
  "recommended_order": ["SP2-U01", "SP2-U02", "SP2-U03"]
}
```

Also produce a human-readable summary:
- Total units and critical path length
- Unit list with IDs, titles, types, and risk levels
- Identified blockers or ambiguities
- Recommended execution order

## Error Handling

- If the spec file is not found, report the searched paths and stop.
- If the spec contains ambiguous requirements, list them as blockers. Do not make architectural decisions.
