# CLAUDE.md — ArhuGula

Portable Pi-orchestrated agent development environment. Identical clone of IndyDevDan's
complete agent harness development environment.

## What This Repo Does

This repo implements IndyDevDan's four-layer architecture (Skill -> Subagent -> Command -> Justfile)
as a standalone, portable agent development environment. It provides the harness for building
projects with Claude Code agents, hooks, and orchestrated workflows.

## What This Repo Does NOT Do

- No production application code lives here (projects built with ArhuGula live in their own repos)
- No direct API calls to external services from the harness itself
- No invented features — only features documented in IndyDevDan's repos

## Runtime Boundary

n8n remains the sole runtime orchestrator for production data flows. This harness augments
Claude Code development sessions only.

## Canonical Source Documents

The following documents in the research repo are the source of truth for all implementation:

| Document | Path | Role |
|----------|------|------|
| **v2 Design Spec** | `~/Projects/indydevdan-harness-research/docs/superpowers/specs/2026-04-09-arhugula-design-v2.md` | Master architecture, sub-project definitions, dependency graph |
| **Feature Inventory** | `~/Projects/indydevdan-harness-research/docs/superpowers/specs/feature-inventory.md` | Exhaustive catalog of 136 features with BUILT/GAP/INVENTED status |
| **Method Synthesis** | `~/Projects/indydevdan-harness-research/docs/03-indydevdan/method-synthesis.md` | 14 foundational principles |
| **Comprehensive Reference** | `~/Projects/indydevdan-harness-research/docs/IndyDevDan Comprehensive/indydevdan_method_comprehensive_reference.md` | 5-layer stack, skill taxonomy |

The v1 spec (`2026-04-09-arhugula-design.md`) is SUPERSEDED. Do not use it for new work.

## Source Precedence

| Rank | Source | Role |
|------|--------|------|
| 1 | Official Anthropic docs | Ground truth for Claude Code capabilities |
| 2 | v2 Design Spec + Feature Inventory | What to build and implementation status |
| 3 | IndyDevDan method reference + repos | Patterns, conventions, source code |
| 4 | Project-specific constraints | Hardware limits, environment config |

## Implementation Rules (MANDATORY)

These rules prevent scope drift, invented features, and missed gaps:

1. **Check the Feature Inventory BEFORE building anything.** Read `feature-inventory.md`
   and verify the feature is classified as GAP or SPEC-ONLY (not INVENTED or DEFERRED).
   If a feature is INVENTED, do not build it. If it is DEFERRED, explain why it should
   be reclassified before proceeding.

2. **Follow the v2 sub-project sequence.** The v2 spec defines 15 sub-projects with a
   dependency graph. Do not skip ahead. Do not reorder without explicit user approval.
   Current sequence: SP2 (Security) → SP3 (Validation) → SP4 (Multi-Model) → SP5 (Knowledge Base)
   → SP6 (Library) → SP7 (SFA) → SP8 (Drive+Listen+Direct, BUILT) → SP9 (Orchestration) → ...

3. **No invented components.** If a feature does not exist in any IndyDevDan repo
   (code, architecture doc, or concept), do not add it. The goal is identical replication,
   not enhancement. If you believe an enhancement is warranted, flag it explicitly as
   NON-INDYDEVDAN and get user approval before implementing.

4. **Verify source attribution.** For every component you build, identify the source repo
   (damage-control, hooks-mastery, just-prompt, pocket-pick, etc.) and source type
   (code exists, architecture doc, concept only). Code-exists sources can be referenced
   directly. Architecture-doc sources require greenfield implementation matching the
   documented interface. Concept-only sources require design before implementation.

5. **Use the IndyDevDan planning workflow.** The planning pipeline is:
   `/scout` (decompose spec) → `/build` (implement each unit) → `/harness-review` (verify).
   External planning tools (gstack /create-implementation-plan, /plan-ceo-review, etc.)
   may supplement but do not replace this pipeline.

6. **Update the Feature Inventory after each sub-project.** When a feature moves from
   GAP to BUILT, update `feature-inventory.md` in the research repo with the commit hash
   and date.

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
| Check feature status | `~/Projects/indydevdan-harness-research/docs/superpowers/specs/feature-inventory.md` |
| Read master spec | `~/Projects/indydevdan-harness-research/docs/superpowers/specs/2026-04-09-arhugula-design-v2.md` |

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

## Sub-Project Status

| SP | Name | Status | Features |
|----|------|--------|----------|
| SP1 | CC Harness | BUILT | 40/40 features |
| SP2 | Security Hardening | NOT STARTED | 6 features (3.08-3.13) |
| SP3 | Validation Pipeline | NOT STARTED | 8 features (6.01-6.08) |
| SP4 | Multi-Model (just-prompt) | NOT STARTED | 7 features (7.01-7.07) |
| SP5 | Knowledge Base (pocket-pick) | NOT STARTED | 7 features (8.01-8.07) |
| SP6 | Library Distribution | NOT STARTED | 6 features (9.02-9.07) |
| SP7 | Single-File Agents | NOT STARTED | 9 features (10.01-10.09) |
| SP8 | Drive + Listen + Direct | BUILT | 15 features |
| SP9 | Orchestration | NOT STARTED | 8 features (11.01-11.08) |
| SP10 | Drop Zones | NOT STARTED | 4 features (14.01-14.04) |
| SP11 | Prompt Testing | NOT STARTED | 4 features (15.02-15.05) |
| SP12 | Pi Integration | NOT STARTED | Depends on SP8 |
| SP13 | Steer (Swift GUI) | NOT STARTED | Depends on SP8 |
| SP14 | Browser Automation (bowser) | NOT STARTED | 6 features |
| SP15 | E2B Sandboxes | NOT STARTED | 4 features |

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
