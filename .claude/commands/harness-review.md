---
description: Multi-model consensus code review
---

# /review — Consensus Review

## Purpose

Run a CEO-and-board style multi-model consensus review on recent changes.

## Workflow

1. Identify the changes to review (uncommitted, last commit, or branch diff)
2. Dispatch the `validator` subagent to check correctness
3. Dispatch the `spec-checker` subagent to verify spec compliance
4. Synthesize findings into a single review with:
   - APPROVE / REQUEST CHANGES / COMMENT verdict
   - Numbered findings with priority (P0-P3)
