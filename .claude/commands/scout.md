---
description: Evaluate prompt quality before dispatch (HOP/LOP pattern)
---

# /scout — Prompt Quality Evaluator

## Purpose

Evaluate a prompt using the Higher-Order Prompt / Lower-Order Prompt (HOP/LOP) pattern.
Assess whether a prompt is specific enough, well-scoped, and likely to produce a good result.

## Workflow

1. Ask the user for the prompt they want to evaluate
2. Analyze against these criteria:
   - **Specificity**: Does it name exact files, functions, or behaviors?
   - **Scope**: Is it a single task or multiple tasks bundled together?
   - **Testability**: Can you verify the result is correct?
   - **Context**: Does it provide enough background for an agent to act?
3. Rate: HIGH (ready), MEDIUM (needs refinement), LOW (rewrite)
4. If MEDIUM or LOW, suggest a rewritten version

## Report

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Specificity | HIGH/MED/LOW | ... |
| Scope | HIGH/MED/LOW | ... |
| Testability | HIGH/MED/LOW | ... |
| Context | HIGH/MED/LOW | ... |
| **Overall** | **HIGH/MED/LOW** | ... |
