---
description: Load full project context for orientation
---

# /prime — Project Context Loader

## Purpose

Load the complete ArhuGula project state so you understand the codebase before doing any work.

## Workflow

1. Run `git ls-files` to get the full file manifest
2. Read `README.md` for project overview
3. Read `justfile` for available recipes and architecture layers
4. Read `.claude/settings.json` to understand hook wiring and permissions
5. Read all files in `.claude/hooks/` to understand the hook architecture
6. Read all files in `.claude/commands/` to understand available slash commands
7. Read all files in `.claude/agents/` to understand subagent definitions
8. Read `skills/library.yaml` for the skill catalog
9. Read `.env.example` for environment variable schema

## Report

Present a structured summary:

| Section | Contents |
|---------|----------|
| **Files** | Total count from git ls-files |
| **Hooks** | List all 13 with health status |
| **Commands** | List all 7 with descriptions |
| **Agents** | List all 4 with roles |
| **Skills** | List from library.yaml |
| **Environment** | List INJECT-marked variables |
