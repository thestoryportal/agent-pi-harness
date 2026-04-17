# P3 — Cross-Role Consistency

## Purpose

Identify gaps, overlaps, and naming inconsistencies across the full 170+ role file set. Validates that the organizational charter and role files form a coherent system rather than 170 isolated documents.

## Prerequisites

- P1 complete (structural compliance known)
- `~/.claude/roles/organizational-charter-v3.md` loaded

## Checks

### 1. Charter Completeness
Every role listed in `organizational-charter-v3.md` must have a corresponding role file.

```bash
# Extract role names from charter (grep for the role table rows)
grep -E "^\|.*\|.*\|.*\|" ~/.claude/roles/organizational-charter-v3.md

# List all role files
find ~/.claude/roles -name "*.md" \
  ! -name "role-template-v1.1.md" \
  ! -name "organizational-charter-v3.md" \
  ! -name "README.md" \
  | sed 's|.*/||; s|\.md||' | sort
```

Flag: roles in charter with no file, files with no charter entry.

### 2. Role Reference Validity
Every role file references other roles in "Works With", "Reports To", and handoff sections. Those referenced roles must exist.

For each role file, extract referenced role names and verify they appear in the charter.

### 3. Responsibility Overlap Analysis
Using just-prompt, identify responsibilities that appear in multiple roles across departments. Some overlap is expected (e.g., "code review"), but unowned responsibilities or conflicting ownership are bugs.

**Prompt for LLM:**
```
Given these role summaries from different departments, identify:
1. Responsibilities claimed by multiple roles (who owns it?)
2. Responsibilities that appear in no role (gap)
3. Escalation chains that have no landing point (escalates to a role that doesn't escalate-up to anyone)

Role summaries: [excerpt What You Own from each role]
```

### 4. Classification Consistency
The organizational charter assigns Human-Primary / Hybrid / AI-Primary to each role. Do the role files' Deployment Notes sections match the charter classification?

### 5. Naming Conventions
Are role names consistent across:
- File names (kebab-case: `backend-developer.md`)
- Document titles (`# Backend Developer — Role Template`)
- Charter references (`Backend Developer`)
- Cross-role references in "Works With" tables

## Output Format

### P3 Report — Cross-Role Consistency

**Date:** [date]
**Total Role Files:** N
**Charter Entries:** N

#### Coverage Gaps
| Type | Item | Action |
|------|------|--------|
| Charter-only | [role name] | Create role file |
| File-only | [filename] | Add to charter or delete |

#### Invalid Role References
| File | Referenced Role | Status |
|------|----------------|--------|
| engineering/backend-developer.md | Senior Backend Developer | NOT IN CHARTER |
| ... | | |

#### Responsibility Overlaps
| Responsibility | Claimed By | Recommended Owner |
|---------------|-----------|------------------|
| Database schema design | Backend Developer, Data Engineer | Backend Developer |
| ... | | |

#### Responsibility Gaps
| Domain | No Owner Found |
|--------|---------------|
| Legal/compliance review | — |
| ... | |

#### Classification Mismatches
| Role | Charter Classification | File Classification | Match? |
|------|----------------------|--------------------|----|
| ... | | | |

#### Summary
- Coverage: N/N charter roles have files (N missing)
- Invalid references: N
- Overlaps: N (N critical, N acceptable)
- Gaps: N
- Classification mismatches: N

## Persist Findings

Store in pocket-pick:
- Tags: `roles-p3`, `cross-role-consistency`
- Content: summary counts + list of critical gaps/overlaps
