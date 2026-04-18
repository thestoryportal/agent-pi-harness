---
description: Run setup_init hook and report installation results
argument-hint: [hil]
---

# Purpose

Execute the repository initialization hook (setup_init) which installs all dependencies and initializes the database, then summarize and report the results to the user.

## Variables

MODE: $1 (optional - if "true", run interactive mode)

## Workflow
> Execute the following steps in order, top to bottom:

1. **First**, execute `Skill(/prime)` to understand the codebase
2. Check for interactive mode: If MODE is "true", run `Skill(/install-hil)` and ignore the remainder of this prompt
3. Read the log file at `.claude/hooks/setup.init.log` (the hook already ran via `--init` flag)
4. Analyze for successes and failures
5. Write results to `app_docs/install_results.md`
6. Report to user

## Report

Write to `app_docs/install_results.md` and respond to user:

**Status**: SUCCESS or FAILED

**What worked**:
- [completed actions]

**What failed** (if any):
- [errors with context]

**Next steps**:
- [what to do now]

## Damage Control Installation (extension)

The damage-control security hooks system is installed as part of the
standard initialization flow above. The hook chain is wired in
`.claude/settings.json` (PreToolUse Bash/Edit/Write matchers) and points
at the canonical hook copies under
`.claude/hooks/damage-control/hooks/damage-control-python/`. The shared
rule file lives at `.claude/hooks/damage-control/patterns.yaml`.

Source: merged from `disler/claude-code-damage-control` upstream
`install.md` per SP2 D12=A. The upstream file's substantive content was
the one-line directive "Install the damage control system."; this section
absorbs that directive without losing the surrounding install-and-maintain
workflow that ArhuGula uses for the rest of the project initialization.

To install or update the damage control system specifically (e.g. after
upgrading the skill from a fresh upstream pull), invoke `Skill(damage-control)`
which the global skill catalog routes to `.claude/hooks/damage-control/SKILL.md`.
