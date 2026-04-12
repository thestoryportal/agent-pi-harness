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

## Canonical Source Document

| Document | Path | Role |
|----------|------|------|
| **Source of Truth** | `~/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md` | **THE** canonical document. 101 features, 19 patterns, 14 principles, 15 sub-projects. Drives all implementation. |

All prior specs (v1, v2, feature-inventory.md) are SUPERSEDED by this document.
Reference docs (method-synthesis, comprehensive reference, repo analyses) remain as background material.

## Source Precedence

| Rank | Source | Role |
|------|--------|------|
| 1 | Official Anthropic docs | Ground truth for Claude Code capabilities |
| 2 | v2 Design Spec + Feature Inventory | What to build and implementation status |
| 3 | IndyDevDan method reference + repos | Patterns, conventions, source code |
| 4 | Project-specific constraints | Hardware limits, environment config |

## Implementation Rules (MANDATORY)

These rules prevent scope drift, invented features, and missed gaps:

1. **Check the Source of Truth BEFORE building anything.** Read `arhugula-source-of-truth.md`
   Section 4 and verify the feature is classified as GAP (not REJECTED).
   If a feature is REJECTED, do not build it. If it is not in the document, it is not
   in scope — flag it as NON-INDYDEVDAN and get user approval.

2. **Follow the sub-project priority order.** Section 8 of the source of truth defines
   priority order. Do not skip ahead. Do not reorder without explicit user approval.
   Current: SP4 → SP5 → SP6 → SP7 → ...

3. **No invented components.** If a feature does not exist in any IndyDevDan repo
   (code, architecture doc, or concept), do not add it. The goal is identical replication.
   The REJECTED list (Section 7) is final — do not re-propose rejected features.

4. **Verify source attribution.** For every component, identify the source repo and
   whether code exists or is concept-only. Check the repo snapshot in
   `research/repo-snapshots/` for actual implementation patterns to follow.

5. **Use the IndyDevDan planning workflow.** The pipeline is:
   `/scout` (decompose) → `/build` (implement) → `/harness-review` (verify).
   External tools (gstack) may supplement but do not replace this pipeline.

6. **Update the Source of Truth after each sub-project.** When a feature moves from
   GAP to BUILT, update `arhugula-source-of-truth.md` Section 4 with the date.

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
| Check feature status | `~/Projects/indydevdan-harness-research/docs/superpowers/specs/arhugula-source-of-truth.md` |

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

See Source of Truth Section 8 for priority order. Fix structural issues (Section 3) first.

| SP | Name | Status | Features | Source |
|----|------|--------|:--------:|--------|
| SP1 | CC Harness | BUILT | 40 | hooks-mastery, install-maintain, damage-control |
| SP2 | Security Hardening | BUILT | 6 | damage-control |
| SP3 | Validation Pipeline | BUILT | 8 | agentic-finance-review, hooks-mastery |
| SP4 | Multi-Model | BUILT | 7 | just-prompt |
| SP5 | Knowledge Base | **NEXT** | 7 | pocket-pick |
| SP6 | Library Distribution | NOT STARTED | 6 | the-library |
| SP7 | Single-File Agents | NOT STARTED | 9 | single-file-agents |
| SP8 | Drive + Listen + Direct | BUILT | 15 | mac-mini-agent |
| SP9 | Orchestration | NOT STARTED | 11 | bowser, comprehensive-ref, infinite-agentic-loop |
| SP10 | Drop Zones | NOT STARTED | 4 | agentic-drop-zones |
| SP11 | Prompt Testing | NOT STARTED | 4 | llm-prompt-testing |
| SP12 | Pi Integration | NOT STARTED | 3 | pi-agent |
| SP13 | Steer (Swift GUI) | NOT STARTED | 3 | mac-mini-agent |
| SP14 | Browser Automation | NOT STARTED | 6 | bowser |
| SP15 | E2B Sandboxes | NOT STARTED | 4 | agent-sandboxes |

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
