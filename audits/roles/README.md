# Role File Audit Methodology

5-pass progressive audit for `~/.claude/roles/` — validates template quality, structural compliance, LLM-readiness, consistency, and deployment fitness before any role is used in an agent session.

## Passes

| Pass | Name | Method | Destructive |
|------|------|--------|-------------|
| P0 | Template Audit | LLM review of `role-template-v1.1.md` | No |
| P1 | Structural Scan | Mechanical grep across all 170+ files | No |
| P2 | Quality Assessment | Multi-model board review per department | No |
| P3 | Cross-Role Consistency | Charter + role cross-reference analysis | No |
| P4 | Story Portal Extraction | Extract appendix sections to consolidated doc | No (read + write to audits/) |
| P5 | Deployment Readiness | Skill refs + context requirements validation | No |

## Usage

```
/audit-roles p0                    # Validate template quality
/audit-roles p1                    # Structural + encoding scan of all roles
/audit-roles p1 engineering        # Scan only engineering department
/audit-roles p2                    # Quality assessment (all departments)
/audit-roles p3                    # Cross-role consistency
/audit-roles p4                    # Story Portal extraction
/audit-roles p5                    # Deployment readiness check
/audit-roles all                   # Sequential full audit
```

## Findings Persistence

All passes store findings in pocket-pick with structured tags:
- `roles-p0` — template quality findings
- `roles-p1` — structural compliance issues
- `roles-p2` — quality scores and recommendations
- `roles-p3` — consistency gaps and overlaps
- `roles-p5` — deployment blockers

P4 writes a consolidated file to `audits/roles/story-portal-context-<date>.md`. It does NOT modify role files.

## Encoding Issues (31 files affected)

P1 flags UTF-8 mojibake (`â€"` instead of `—`, `ðŸ"„` instead of `🔄`). To fix:
```bash
# Preview corrupted files (P1 output)
grep -rlE 'â€|ðŸ|Ã¢' ~/.claude/roles/

# Fix encoding in a single file — test on ONE file first, verify output before applying broadly
# The mojibake is double-encoded UTF-8 (UTF-8 bytes read as Windows-1252, re-encoded as UTF-8)
# Correct fix direction: strip the outer UTF-8 layer to recover original bytes
iconv -f utf-8 -t windows-1252 file.md > file.md.fixed
# Then verify file.md.fixed looks correct before overwriting

# Alternatively: pip install ftfy && python3 -c "import ftfy; print(ftfy.fix_file('file.md'))"
```
Run the fix on specific files after P1 identifies them; re-run P1 to verify. Always preview before applying to multiple files.

## Tool Dependencies

- `just-prompt` MCP: required for P0, P2, P3 (multi-model review)
- `pocket-pick` MCP: required for P1-P5 findings persistence
- `Bash`: required for P1 mechanical scan
- API keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY` for P2 board pattern

## Prompt Files

Each pass has a corresponding prompt at `audits/roles/prompts/p<N>-*.md`. The slash command reads these and executes them. To customize a pass, edit the prompt file.
