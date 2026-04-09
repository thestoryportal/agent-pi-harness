# CLAUDE.md — ArhuGula

Portable Pi-orchestrated agent development environment.

## What This Repo Does

This repo implements IndyDevDan's four-layer architecture (Skill -> Subagent -> Command -> Justfile)
as a standalone, portable agent development environment. It provides the harness for building
projects with Claude Code agents, hooks, and orchestrated workflows.

## What This Repo Does NOT Do

- No production application code lives here (projects built with ArhuGula live in their own repos)
- No direct API calls to external services from the harness itself

## Runtime Boundary

n8n remains the sole runtime orchestrator for production data flows. This harness augments
Claude Code development sessions only.

## Source Precedence

| Rank | Source | Role |
|------|--------|------|
| 1 | Official Anthropic docs | Ground truth for Claude Code capabilities |
| 2 | IndyDevDan method reference | Patterns and conventions |
| 3 | IndyDevDan public repos | Evidence for implementation |
| 4 | Project-specific constraints | Product requirements |

## Directory Navigation

| Task | Location |
|------|----------|
| Run a task | `justfile` — `just --list` |
| Understand hook architecture | `.claude/hooks/` |
| Read a slash command | `.claude/commands/` |
| Check subagent definitions | `.claude/agents/` |
| Review settings/permissions | `.claude/settings.json` |
| Check skill catalog | `skills/library.yaml` |
| View environment config | `.env.example` |

## Naming Conventions

- Authored files: lowercase-with-hyphens
- Hook files: underscores (e.g., `session_start.py`)
- Reserved exceptions: `README.md`, `CLAUDE.md`, `SKILL.md`

## Four-Layer Architecture

| Layer | Purpose | Invocation |
|-------|---------|-----------|
| 1. Skill | Direct capability | `just prime`, `just scout` |
| 2. Subagent | Isolated agent sessions | `just build`, `just review` |
| 3. Command | Saved workflows | `just cldi`, `just cldii` |
| 4. Justfile | Composable recipes | All `just` commands |

## Hook Security Model

- **Fail-open** (IndyDevDan default): non-security hook crash = pass through (exit 1)
- **Security hooks always fail-closed**: pre_tool_use, permission_request crash = block (exit 2)
- **Exit codes**: 0=allow, 1=log-only/pass-through, 2=block
- **Health check**: `session_start.py` validates all hooks at session start
- **Path protection**: `.env`, `~/.ssh/`, credentials blocked via `pre_tool_use.py`
