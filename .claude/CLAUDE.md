# CLAUDE.md — ArhuGula

Claude Code agent development environment. Four-layer architecture for building AI applications with agents, hooks, and orchestrated workflows.

## What This Repo Does

This repo is the harness for building software projects with Claude Code. It provides:
- Agents, hooks, and slash commands pre-wired for agentic development
- Single-file agent templates for common data tasks (SQL, CSV, JSON, web)
- Browser automation, voice input, E2B sandboxes, and Pi terminal integration
- A validation pipeline for reviewing agent output against specs

Projects built with ArhuGula live in their own repos. This harness is the shared platform.

## Starting a New Project

1. Create a new repo for the project (not in ArhuGula)
2. Run `just prime` to load project context
3. Run `just scout` to decompose the spec into implementation units
4. Run `just architect` to produce a build plan
5. Run `just build` to implement each unit
6. Run `just harness-review` to validate against the spec

## Capabilities

| Category | Recipes |
|----------|---------|
| **Build pipeline** | `prime`, `scout`, `architect`, `build`, `harness-review` |
| **Session management** | `cldi`, `cldii`, `cldm`, `cldmm` |
| **Single-file agents** | `sfa-bash`, `sfa-duckdb`, `sfa-sqlite`, `sfa-polars`, `sfa-jq`, `sfa-metaprompt`, `sfa-context` |
| **Drive + Listen** | `listen`, `send`, `sendf`, `job`, `jobs`, `latest`, `stop`, `clear` |
| **Browser automation** | `hop`, `ui-review`, `automate-amazon`, `summarize-blog` |
| **Drop zones** | `dropzone` |
| **Prompt testing** | `eval-builder`, `eval-validator`, `eval-scout`, `eval-all`, `promptfoo-view` |
| **Pi integration** | `pi`, `pi-drive`, `pi-listen`, `pi-full`, `ext-*` (16 extensions) |
| **Steer (Swift GUI)** | `steer-build`, `steer-see`, `steer-apps`, `steer-ocr` |
| **E2B sandboxes** | `sbx`, `sbx-run`, `sbx-mcp` |
| **Voice** | `voice` |
| **Observe** | `db-prune` |

## Runtime Boundary

Orchestration is project-defined — Pi, n8n, OpenClaw, or other tools depending on project needs. This harness provides the Claude Code layer (agents, hooks, commands, recipes) regardless of which orchestrator a given project uses.

## Directory Navigation

| Task | Location |
|------|----------|
| Run a task | `justfile` — `just --list` |
| Understand hook architecture | `.claude/hooks/` |
| Read a slash command | `.claude/commands/` |
| Check subagent definitions | `.claude/agents/` |
| Review settings/permissions | `.claude/settings.json` |
| Check skill catalog | `~/Projects/agent-deployment-framework/skills/library/library.yaml` (role-skills catalog) |
| View environment config | `.env.example` |
| Review audit history | `audits/exceptions.md` |

## Naming Conventions

- Authored files: lowercase-with-hyphens
- Hook files: underscores (e.g., `session_start.py`)
- Reserved exceptions: `README.md`, `CLAUDE.md`, `SKILL.md`

## Four-Layer Architecture

| Layer | Purpose | Invocation |
|-------|---------|-----------|
| 1. Skill | Direct capability | `just prime`, `just scout` |
| 2. Subagent | Isolated agent sessions | `just build`, `just harness-review` |
| 3. Command | Saved workflows | `just cldi`, `just cldii` |
| 4. Justfile | Composable recipes | All `just` commands |

## Hook Security Model

- **Fail-open** (IndyDevDan default): non-security hook crash = pass through (exit 1)
- **Security hooks always fail-closed**: pre_tool_use, permission_request crash = block (exit 2)
- **Exit codes**: 0=allow, 1=log-only/pass-through, 2=block
- **Health check**: `session_start.py` validates all hooks at session start
- **Path protection**: `.env`, `~/.ssh/`, credentials blocked via `pre_tool_use.py`

## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.
The skill has specialized workflows that produce better results than ad-hoc answers.

Key routing rules:
- Product ideas, "is this worth building", brainstorming → invoke office-hours
- Bugs, errors, "why is this broken", 500 errors → invoke investigate
- Ship, deploy, push, create PR → invoke ship
- QA, test the site, find bugs → invoke qa
- Code review, check my diff → invoke review
- Update docs after shipping → invoke document-release
- Weekly retro → invoke retro
- Design system, brand → invoke design-consultation
- Visual audit, design polish → invoke design-review
- Architecture review → invoke plan-eng-review
- Save progress, checkpoint, resume → invoke checkpoint
- Code quality, health check → invoke health
