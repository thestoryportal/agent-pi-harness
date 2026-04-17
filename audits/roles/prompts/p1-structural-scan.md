# P1 — Structural Compliance Scan

## Purpose

Mechanical scan of all role files in `~/.claude/roles/` for:
1. Required section presence (11 sections from template)
2. UTF-8 encoding integrity (detect mojibake from December 2024 build)
3. Frontmatter metadata completeness (Department, Classification, Deployment, Version)

This is a read-only, grep-based pass. No LLM required for the scan itself.

## Inputs

- All `~/.claude/roles/**/*.md` files (excluding `role-template-v1.1.md` and `organizational-charter-v3.md`)
- Optional department filter from `$FILTER` argument

## Scan Steps

### Step 1 — Enumerate Files

```bash
find ~/.claude/roles -name "*.md" \
  ! -name "role-template-v1.1.md" \
  ! -name "organizational-charter-v3.md" \
  ! -name "README.md" \
  | sort
```

If `$FILTER` is set, restrict to files matching the department name.

### Step 2 — Encoding Integrity Check

```bash
grep -rlE 'â€|ðŸ|Ã¢' ~/.claude/roles/
```

Report: list of affected files, count per file.

### Step 3 — Section Presence Check

For each file, grep for the 11 required section headers:
- `## Role Definition`
- `## Core Identity`
- `### Mission`
- `### Philosophy`
- `### What You Own`
- `### What You Don't Own`
- `### Boundaries`
- `## Core Responsibilities`
- `## Workflows`
- `## Collaboration`
- `## Quality Standards`
- `## Context Requirements`
- `## Deployment Notes`
- `## Appendix: Story Portal Context`
- `## Document Control`

### Step 4 — Frontmatter Metadata Check

For each file, verify the frontmatter block (lines 2-7) includes:
- `**Department:**`
- `**Classification:**` with valid emoji (👤, 🔄, 🤖)
- `**Deployment:**`
- `**Version:**`

Note: encoding-corrupted files may have `ðŸ"„` instead of `🔄` — flag as encoding issue, not structural miss.

## Output Format

### P1 Report — Structural Compliance Scan

**Scan Date:** [date]
**Files Scanned:** N
**Department Filter:** [none | department-name]

#### Encoding Issues (N files)
| File | Mojibake Occurrences |
|------|---------------------|
| engineering/full-stack-developer.md | 2 |
| ... | ... |

**Fix command:**
```bash
# Preview (safe)
grep -c $'â€\|ðŸ' path/to/file.md

# Fix (requires user approval — modifies files in ~/.claude/roles/)
```

#### Section Compliance Matrix

| File | RoleDef | CoreId | Responsibilities | Workflows | Collaboration | Quality | Context | Deploy | StoryPortal | DocControl |
|------|---------|--------|-----------------|-----------|---------------|---------|---------|--------|-------------|------------|
| engineering/backend-developer.md | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ... | | | | | | | | | | |

#### Summary by Department
| Department | Files | Fully Compliant | Missing Sections | Encoding Issues |
|-----------|-------|-----------------|------------------|-----------------|
| engineering | N | N | N | N |
| ... | | | | |

#### Files Requiring Attention (sorted by issue count)
1. [most issues first]

## Persist Findings

Store per-department summary in pocket-pick:
- Tags: `roles-p1`, `structural-scan`, `[department-name]`
- Content: compliance matrix row for the department
- Separate entry for encoding issues list with tag `roles-p1-encoding`
