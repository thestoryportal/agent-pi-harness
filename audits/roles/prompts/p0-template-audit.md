# P0 — Template Audit

## Purpose

Validate `role-template-v1.1.md` before using it as the standard against which 170+ role files are judged. A flawed template produces flawed audit results.

## Inputs

- `~/.claude/roles/role-template-v1.1.md` — the standard being evaluated
- `~/.claude/roles/organizational-charter-v3.md` — the charter it references

## Evaluation Dimensions

### 1. Section Completeness
Does the template specify all 11 required sections clearly?
- Role Definition, Core Identity (Mission + Philosophy + Ownership + Boundaries)
- Core Responsibilities, Workflows, Collaboration
- Quality Standards, Context Requirements, Deployment Notes
- Story Portal Appendix, Document Control

### 2. Quality Checklist Self-Consistency
The template includes a 10-item quality checklist. Does the checklist test things the template actually specifies in enough detail to be verifiable?
- Flag any checklist item that cannot be verified from the template text alone
- Flag any template section that has no corresponding checklist item

### 3. Philosophy Guidance Quality
The "Common Mistakes" section warns against "generic philosophy." Does the template give enough concrete guidance about what non-generic philosophy looks like?

### 4. Classification Accuracy
Does the Classification Guide (Human-Primary / Hybrid / AI-Primary) give enough criteria to make consistent decisions across 170+ roles?

### 5. Charter Alignment
Does the template reference the organizational charter correctly? Are the department names, role names, and classification symbols consistent with the charter?

### 6. Agent Deployment Guidance
Is the Deployment Notes section specific enough for an AI agent to know how to load and use a role file correctly?

## Output Format

### P0 Findings

**Template Quality Score:** [1-10]

**Section Completeness:** [Pass/Fail per section]

**Checklist Gaps:**
- [Items that can't be verified from template text]
- [Template sections with no checklist coverage]

**Issues:**
| Severity | Section | Finding | Recommendation |
|----------|---------|---------|----------------|
| [P0/P1/P2] | ... | ... | ... |

**Verdict:** [APPROVED — proceed to P1 | CONDITIONAL — proceed with caveats | BLOCKED — fix template first]

**Proceed to P1?** [Yes/No with rationale]

## Persist Findings

Store summary in pocket-pick:
- Tags: `roles-p0`, `template-audit`
- Content: verdict + top 3 issues
