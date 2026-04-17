# P5 — Deployment Readiness

## Purpose

Final pre-deployment check. Validates that each role can be loaded into a Claude session and function correctly — not just that it passes structural and quality checks, but that it can actually be used right now.

## Prerequisites

- P0 (template approved)
- P1 (encoding issues resolved or known)
- P3 (invalid role references identified)

## Checks

### 1. Skill Reference Validity

Each role's "Required Skills" table lists skill files (e.g., `skill-name.md`). Verify these exist in the skills library.

```bash
# List available skills
cat ~/.claude/skills/library/library.yaml
ls ~/.claude/skills/
```

For each role, cross-reference the skill names in "Required Skills" against the available library. Flag missing skills.

### 2. Context Requirements Specificity

The "Required Context" checklist should be specific enough to tell a user exactly what to provide before starting a session.

Flag as **VAGUE** if Required Context items are:
- "Understand the project" — too generic
- "Project requirements" — too generic

Flag as **SPECIFIC** if they name actual artifacts:
- "Read `specs/feature-spec.md`"
- "Review current sprint board in Linear"

### 3. Iteration Protocol Presence

For Hybrid (🔄) and AI-Primary (🤖) roles, the Deployment Notes section must include an Iteration Protocol loop. Verify the `LOOP:` block is present.

### 4. Classification Deployment Match

Match the Classification against the Deployment field:

| Classification | Expected Deployment |
|----------------|---------------------|
| Human-Primary 👤 | Browser or Hybrid |
| Hybrid 🔄 | Browser, CLI, or Browser + CLI |
| AI-Primary 🤖 | Agent or CLI |

Flag mismatches.

### 5. Agent Formula Readiness Score

For each role, compute a readiness score (0-5):
- +1: All required sections present (P1 pass)
- +1: No encoding issues (P1 pass)
- +1: All skill references valid
- +1: Context requirements are specific
- +1: Story Portal section is not a placeholder (P4 finding)

Score 5 = deployment-ready. Score ≤ 3 = blocked.

## Output Format

### P5 Deployment Readiness Report

**Date:** [date]
**Roles Assessed:** N

#### Deployment Readiness by Department

| Department | Ready (5/5) | Conditional (3-4) | Blocked (≤2) |
|-----------|------------|------------------|--------------|
| engineering | N | N | N |
| ... | | | |

#### Blocked Roles (priority fix list)
| Role | Score | Missing |
|------|-------|---------|
| [name] | 2/5 | encoding, story-portal |
| ... | | |

#### Deployment Manifest

| Role | Score | Classification | Deployment | Skills OK | Context OK | Story Portal |
|------|-------|---------------|-----------|-----------|-----------|-------------|
| engineering/backend-developer | 4/5 | 🔄 Hybrid | CLI | ✓ | ✗ | Specific |
| ... | | | | | | |

#### How to Load a Ready Role in Claude

```
Read the role file at ~/.claude/roles/[department]/[role-name].md.
Confirm the Required Context checklist before beginning.
Apply the Iteration Protocol in Deployment Notes for all outputs.
```

## Persist Findings

Store in pocket-pick:
- Tags: `roles-p5`, `deployment-readiness`
- Content: summary counts + blocked role list
- One entry per blocked role with specific fix needed
