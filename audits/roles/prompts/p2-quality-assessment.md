# P2 — Quality Assessment

## Purpose

LLM-based quality review of role files using the just-prompt CEO/board pattern. Evaluates depth, specificity, AI-readiness, and alignment with the organizational charter. Processes one department at a time.

## Prerequisites

- P0 must be complete with APPROVED or CONDITIONAL verdict
- P1 must be complete so encoding-corrupted files are known
- API keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`

## Inputs

- Role files for the target department (or all departments if no filter)
- `~/.claude/roles/role-template-v1.1.md` — quality checklist
- `~/.claude/roles/organizational-charter-v3.md` — for role reference validation

## Processing Strategy

Process one department at a time. For each department, use the just-prompt board pattern:
- **Board**: `openai:o4-mini`, `anthropic:claude-sonnet-4-6`, `gemini:gemini-2.0-flash`
- **CEO**: `openai:o3` — synthesizes board findings
- Verify available models at runtime with `just-prompt list_models` before calling

For each role file:

### Board Prompt Template

```
You are reviewing a role file from an enterprise AI workforce framework.
Rate this role on 5 dimensions (1-10 each) and provide specific findings.

TEMPLATE STANDARD (quality checklist):
[paste quality checklist from role-template-v1.1.md]

ROLE FILE CONTENT:
[paste role file content]

Rate these dimensions:
1. Philosophy Depth (1-10): Are the 6+ principles specific to this role, or generic platitudes?
2. Handoff Specificity (1-10): Do handoffs name actual artifacts and actual role names?
3. Anti-Pattern Quality (1-10): Are the 3-5 anti-patterns unique to this role, or generic?
4. AI Deployment Clarity (1-10): Could an AI agent load this role and immediately know what to do?
5. Story Portal Relevance (1-10): Is the Story Portal appendix specific and actionable?

For each low score (<7), provide one specific improvement with an example rewrite.
Format: JSON with keys: role, scores, findings, top_improvement
```

### CEO Synthesis Prompt

```
Three board members reviewed [role-name]. Synthesize their findings into:
1. Consensus score (average of averages)
2. Top strength (most agreed-upon positive)
3. Top weakness (most agreed-upon gap)
4. Single highest-priority improvement recommendation

Board findings: [board results]
```

## Batching Rules

- Skip encoding-corrupted files (flag them — fix encoding in P1 first)
- Process max 5 roles per board call to avoid token overflow
- Store findings after each department before moving to next

## Output Format

### P2 Quality Report — [Department Name]

**Date:** [date]
**Roles Assessed:** N
**Skipped (encoding):** N

| Role | Philosophy | Handoffs | Anti-Patterns | AI-Clarity | StoryPortal | Consensus |
|------|-----------|---------|---------------|-----------|-------------|-----------|
| backend-developer | 7 | 6 | 8 | 7 | 5 | 6.6 |
| ... | | | | | | |

#### Department Summary
- **Highest scoring role:** [name] ([score])
- **Lowest scoring role:** [name] ([score])
- **Most common weakness:** [dimension]
- **Recommended first fixes:** [top 3 roles by improvement impact]

#### Priority Findings
| Priority | Role | Dimension | Finding | Recommended Fix |
|----------|------|-----------|---------|----------------|
| P1 | ... | ... | ... | ... |

## Persist Findings

Store per-role findings in pocket-pick:
- Tags: `roles-p2`, `[department]`, `[role-name]`
- Content: consensus score + top improvement
- One entry per role with full JSON findings
