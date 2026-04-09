---
description: Session maintenance — verify environment health
---

# /maintain — Session Maintenance

## Purpose

Verify environment health and clean up stale state.

## Workflow

1. Run `uv sync` to ensure dependencies are current
2. Run hook health checks (same as session_start)
3. Check `.claude/logs/` disk usage
4. Prune event logs older than retention window if Observe DB exists
5. Verify git status is clean
6. Report environment health summary
