---
description: "5-pass audit and optimization of ~/.claude/roles/ role files"
argument-hint: "[p0|p1|p2|p3|p4|p5|all] [department-filter]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Agent
  - mcp__pocket-pick__pocket_add
  - mcp__pocket-pick__pocket_find
  - mcp__just-prompt__prompt
  - mcp__just-prompt__ceo_and_board
---

# /audit-roles — Role File Audit and Optimization

Runs a structured 5-pass audit of the role files at `~/.claude/roles/`. Each pass builds on the previous. Run them in order for a first-time audit; run individual passes when re-checking after fixes.

## Variables

```
ARGUMENTS: $ARGUMENTS   # e.g., "p1 engineering" or "all"
```

## Argument Parsing

Parse `$ARGUMENTS` by splitting on whitespace:
1. First token → PASS (required): `p0`, `p1`, `p2`, `p3`, `p4`, `p5`, or `all`. If missing or "help", show the table below and stop.
2. Second token → FILTER (optional): department name (e.g., `engineering`). If not provided, process all departments.

**Available passes:**
| Pass | Name | What it does |
|------|------|-------------|
| p0 | Template Audit | Validates `role-template-v1.1.md` quality before using it as a standard |
| p1 | Structural Scan | Mechanical grep for required sections + encoding integrity across all files |
| p2 | Quality Assessment | Multi-model board review per department (requires API keys) |
| p3 | Cross-Role Consistency | Charter coverage, invalid references, responsibility gaps/overlaps |
| p4 | Story Portal Extraction | Extracts appendix sections into consolidated doc (read-only on role files) |
| p5 | Deployment Readiness | Skill refs, context specificity, iteration protocol, readiness scores |
| all | Full Audit | Run p0→p5 in sequence |

## Routing

Route to the workflow below that matches PASS. For `all`, run each pass in sequence (p0 → p1 → p2 → p3 → p4 → p5), stopping and reporting if any pass returns a BLOCKED verdict.

---

## P0 — Template Audit

Read and execute: `audits/roles/prompts/p0-template-audit.md`

**Inputs to load first:**
- `~/.claude/roles/role-template-v1.1.md`
- `~/.claude/roles/organizational-charter-v3.md`

**Guard:** If the template receives a BLOCKED verdict, report the specific issues and stop. Do not proceed to P1 until the template is fixed.

---

## P1 — Structural Scan

Read and execute: `audits/roles/prompts/p1-structural-scan.md`

**Apply FILTER** if set: restrict the file glob to `~/.claude/roles/[FILTER]/*.md`

**Key outputs:**
1. Encoding-corrupted files (list + fix command)
2. Compliance matrix per department
3. Files requiring attention sorted by issue count

Store findings in pocket-pick with tags `roles-p1` and `[FILTER or "all"]`.

---

## P2 — Quality Assessment

Read and execute: `audits/roles/prompts/p2-quality-assessment.md`

**Prerequisite check:** Verify P0 was APPROVED or CONDITIONAL (check pocket-pick for `roles-p0` tag).

**API key check before starting:**
```bash
echo "OPENAI_API_KEY: ${OPENAI_API_KEY:+set}" 
echo "ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY:+set}"
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:+set}"
```
If any key is missing, report which providers are unavailable and continue with available providers only.

**Apply FILTER** if set: process only the matching department.

Store per-role findings in pocket-pick with tags `roles-p2`, `[department]`, `[role-slug]`.

---

## P3 — Cross-Role Consistency

Read and execute: `audits/roles/prompts/p3-cross-role-consistency.md`

**Note:** FILTER is ignored for P3 — consistency analysis requires the full role set.

Store findings in pocket-pick with tags `roles-p3`, `cross-role-consistency`.

---

## P4 — Story Portal Extraction

Read and execute: `audits/roles/prompts/p4-story-portal-extraction.md`

**Scope gate — confirm before proceeding:**
> "P4 will read all role files and write a consolidated extraction to `audits/roles/story-portal-context-YYYY-MM-DD.md`. It will NOT modify any file in `~/.claude/roles/`. Proceed?"

If the user has not already confirmed (i.e., this is running as part of `all` automatically), pause and ask.

**Apply FILTER** if set: extract only roles from the matching department.

Write output to: `audits/roles/story-portal-context-[date].md`

---

## P5 — Deployment Readiness

Read and execute: `audits/roles/prompts/p5-deployment-readiness.md`

**Apply FILTER** if set: assess only roles from the matching department.

Store findings in pocket-pick with tags `roles-p5`, `deployment-readiness`.
Store blocked roles individually with tags `roles-p5`, `blocked`, `[role-slug]`.

---

## Final Report (for `all` mode)

After all passes complete, produce a consolidated summary:

### Role Audit Complete

| Pass | Status | Key Finding |
|------|--------|-------------|
| P0 | [APPROVED/CONDITIONAL/BLOCKED] | [verdict summary] |
| P1 | [N issues] | [top issue] |
| P2 | [avg score] | [weakest dimension] |
| P3 | [N gaps, N overlaps] | [most critical gap] |
| P4 | [N extracted, N placeholder] | [extraction output path] |
| P5 | [N ready, N blocked] | [top blocker] |

**Recommended next actions** (ordered by impact):
1. [highest priority fix]
2. [second priority]
3. ...

All findings are in pocket-pick. Search with: `pocket find "roles-audit"` or filter by pass tag.
