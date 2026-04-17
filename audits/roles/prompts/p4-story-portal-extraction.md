# P4 — Story Portal Context Extraction

## Purpose

Extract the "Appendix: Story Portal Context" section from all role files and consolidate into a single reference document. This creates a project-specific context snapshot without modifying the role files themselves.

## IMPORTANT: Scope Constraints

**This pass is READ-ONLY on role files.** It writes ONE output file to `audits/roles/`, which is in the sandbox write allowlist. It does NOT modify any file in `~/.claude/roles/`.

If future work requires updating the Story Portal sections in the role files themselves, that is a SEPARATE action requiring explicit user approval for each file write (those files are outside the sandbox write allowlist).

## Prerequisites

- P1 complete (know which files are structurally compliant)
- Role files with missing `## Appendix: Story Portal Context` sections are noted but skipped

## Extraction Steps

### Step 1 — Enumerate Compliant Files

Use P1 findings to get the list of files with a Story Portal appendix section present.

### Step 2 — Extract Sections

For each compliant role file:
1. Read the file
2. Extract the content between `## Appendix: Story Portal Context` and the next `##` section (or end of file)
3. Note the role name, department, and classification

### Step 3 — Assess Extraction Quality

For each extracted section, flag if it appears to be:
- **Placeholder** (contains `[What exists now]` or template fill-in markers)
- **Generic** (describes what the role does generally, not Story Portal specifically)
- **Specific** (mentions actual Story Portal features, tech stack, or current state)

### Step 4 — Compile Output

Write to `audits/roles/story-portal-context-YYYY-MM-DD.md` with:
- One section per department
- Within each department: one subsection per role
- Quality flag alongside each section
- Summary table at top

## Output Format

### `audits/roles/story-portal-context-YYYY-MM-DD.md`

```markdown
# Story Portal Context — Extracted from Role Files
**Date:** YYYY-MM-DD
**Source:** ~/.claude/roles/ (170+ files)
**Roles with section:** N/N (N placeholder, N generic, N specific)

## Summary Table

| Department | Role | Quality | Key Priorities |
|-----------|------|---------|---------------|
| engineering | backend-developer | Specific | [one-line summary] |
| ... | | | |

---

## Engineering

### Backend Developer [Hybrid 🔄]

[extracted content verbatim]

**Quality:** Specific
**Key priorities extracted:** [bullet list of named priorities]

---

[repeat per role]
```

### Session Report

After writing the file, report:

**P4 Extraction Complete**
- Output: `audits/roles/story-portal-context-YYYY-MM-DD.md`
- Roles extracted: N
- Placeholder sections: N (list filenames)
- Generic sections: N (list filenames)
- Specific sections: N

**Recommended next step:** Review placeholder and generic sections — those roles need Story Portal context populated before they can be used in project sessions.
