---
name: prime
description: Load full project context for orientation. Use at session start to understand the codebase before doing any work. Keywords - context, orientation, status, overview.
allowed-tools: Read, Glob, Grep, Bash
---

# Prime — Project Context Loader

## Purpose

Load the complete ArhuGula project state so you understand the codebase before doing any work.

## Workflow

1. Run `git ls-files` to get the full file manifest
2. Read `CLAUDE.md` for project conventions and implementation rules
3. Read `justfile` for available recipes and architecture layers
4. Read `.claude/settings.json` to understand hook wiring and permissions
5. Scan `.claude/hooks/` for the hook architecture
6. Scan `.claude/commands/` for available slash commands
7. Scan `.claude/agents/` for subagent definitions
8. Scan `.claude/skills/` for available skills
9. Read `skills/library.yaml` for the skill catalog
10. Read the source of truth at `~/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md` Section 1 for current build status
11. Scan the auto-loaded MEMORY.md for the most recent entries (last 5-8 lines of the index — these are the active work threads). Read the memory files they point to for active context. Also check `~/.claude/roles/` git status for any uncommitted cross-repo state.

## Report

Present a structured summary:

| Section | Contents |
|---------|----------|
| **Files** | Total count from git ls-files |
| **Hooks** | List all 13 with health status |
| **Commands** | List all with descriptions |
| **Agents** | List all with roles and tool access |
| **Skills** | List from library.yaml + .claude/skills/ |
| **Environment** | Key env vars from session start |
| **Build Status** | SP completion status from source of truth |
