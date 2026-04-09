---
description: Database and schema migration skill
---

# /migrate — Schema Migration

## Purpose

Run database or schema migrations in a controlled, reviewable sequence.

## Workflow

1. Identify pending migrations (check migration directory or schema diff)
2. Show migration plan with exact SQL/schema changes
3. Ask for user confirmation before applying
4. Apply migrations one at a time, verifying each
5. Report final schema state
