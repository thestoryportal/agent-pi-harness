# AGENTS.md — ArhuGula Pi Agent Harness

This file is read by Pi agents at session start. It defines the project structure,
conventions, and rules for all Pi agent operations.

## Project Structure

```
.pi/
  agents/         — Agent persona markdown files
    teams.yaml    — Team membership definitions
    agent-chain.yaml — Sequential pipeline definitions
    pi-pi/        — Pi Pi meta-agent experts
  expertise/      — Agent mental model YAML files (persistent learning)
  skills/         — Runtime skill files loaded by agents
  themes/         — Color theme JSON files
  settings.json   — Pi configuration
  damage-control-rules.yaml — Security rules
extensions/       — TypeScript extensions
AGENTS.md         — This file (Pi equivalent of CLAUDE.md)
TOOLS.md          — Available tool signatures
```

## Agent Hierarchy

```
ORCHESTRATOR (dispatch_agent only — no code tools)
  └── TEAM LEADS (role: lead — has delegate tool, read-only code tools)
      └── WORKERS (role: worker — has code tools, no delegate)
```

- Orchestrator never writes code. It decomposes and delegates to team leads.
- Team leads decompose tasks from the orchestrator and delegate to workers.
- Workers execute — they write code, run tests, produce artifacts.

## Available Teams

Teams are defined in `.pi/agents/teams.yaml`. Use `/agents-team` to switch teams.

| Team | Members | Purpose |
|------|---------|---------|
| full | scout, planner, builder, reviewer, documenter, red-team | Complete dev cycle |
| plan-build | planner, builder, reviewer | Fast implementation |
| info | scout, documenter, reviewer | Research and documentation |
| frontend | planner, builder, bowser | UI development |
| arhugula | scout, planner, builder, reviewer | ArhuGula harness work |
| pi-pi | 10 domain experts | Build Pi components |

## Agent Chains

Chains are defined in `.pi/agents/agent-chain.yaml`. Use `/chain` to switch chains.

| Chain | Flow | Purpose |
|-------|------|---------|
| plan-build-review | planner → builder → reviewer | Standard dev cycle |
| plan-build | planner → builder | Fast two-step |
| scout-flow | scout → scout → scout | Triple-scout deep recon |
| plan-review-plan | planner → plan-reviewer → planner | Iterative planning |
| full-review | scout → planner → builder → reviewer | End-to-end pipeline |

## Runtime Skills

Every agent loads these 5 skills at task start:

1. **conversational-response** — Format responses for readability
2. **mental-model** — Read/update persistent learning at `.pi/expertise/`
3. **active-listener** — Read conversation log before every response
4. **zero-micro-management** — Leaders delegate, workers execute
5. **high-autonomy** — Act autonomously, ask zero questions

## Domain Ownership

Each agent declares which paths it can access in its frontmatter `domain:` field.
The `domain-ownership.ts` extension enforces these boundaries at runtime.

## Naming Conventions

- Agent files: lowercase-with-hyphens.md
- Expertise files: `<agent-name>-mental-model.yaml`
- Extension files: lowercase-with-hyphens.ts
- Skill files: lowercase-with-hyphens.md

## Rules

1. Workers never delegate. Leads never write code directly.
2. Read your mental model (`.pi/expertise/<name>-mental-model.yaml`) at task start.
3. Update your mental model after completing work.
4. Domain boundaries are enforced — do not touch paths outside your domain.
5. Follow existing patterns in the codebase.
