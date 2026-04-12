---
name: Damage Control
description: Install, configure, and manage the Claude Code Damage Control security hooks system. Use when user mentions damage control, security hooks, protected paths, blocked commands, install security, or modify protection settings.
---

# Damage Control Skill

Defense-in-depth protection system for Claude Code. Blocks dangerous commands and protects sensitive files via PreToolUse hooks.

## Overview

This skill helps users deploy and manage the Damage Control security system, which provides:

- **Command Pattern Blocking**: Blocks dangerous bash commands (rm -rf, git reset --hard, etc.)
- **Ask Patterns**: Triggers confirmation dialog for risky-but-valid operations (`ask: true`)
- **Path Protection Levels**:
  - `zeroAccessPaths` - No access at all (secrets/credentials)
  - `readOnlyPaths` - Read allowed, modifications blocked
  - `noDeletePaths` - All operations except delete

## Skill Structure

```
.claude/skills/damage-control/
├── SKILL.md                     # This file
├── patterns.yaml                # Shared security patterns (single source of truth)
├── hooks/
│   ├── bash_damage_control.py   # Bash tool hook
│   ├── edit_damage_control.py   # Edit tool hook
│   └── write_damage_control.py  # Write tool hook
├── cookbook/
│   ├── install_damage_control_ag_workflow.md
│   ├── modify_damage_control_ag_workflow.md
│   ├── manual_control_damage_control_ag_workflow.md
│   ├── list_damage_controls.md
│   ├── test_damage_control.md
│   └── build_for_windows.md
└── test-prompts/
    ├── sentient.md
    ├── sentient_v1.md
    ├── sentient_v2.md
    ├── sentient_v3.md
    └── sentient_v4.md
```

## After Installation

The install workflow copies hooks and creates settings based on the chosen level:

### Project Hooks
```
<project>/
└── .claude/
    ├── settings.json                  # Hook configuration (shared)
    └── hooks/
        ├── bash_damage_control.py
        ├── edit_damage_control.py
        ├── write_damage_control.py
        └── patterns.yaml
```

---

## Cookbook

This section defines the decision tree for handling user requests. Based on what the user says, read and execute the appropriate workflow prompt.

### Installation Pathway

**Trigger phrases**: "install damage control", "setup security hooks", "deploy damage control", "add protection"

**Workflow**: Read and execute [cookbook/install_damage_control_ag_workflow.md](cookbook/install_damage_control_ag_workflow.md)

### Modification Pathway

**Trigger phrases**: "help me modify damage control", "update protection", "change blocked paths", "add restricted directory"

**Workflow**: Read and execute [cookbook/modify_damage_control_ag_workflow.md](cookbook/modify_damage_control_ag_workflow.md)

### Manual Control Pathway

**Trigger phrases**: "how do I manually update", "explain damage control config", "show me the settings"

**Workflow**: Read and execute [cookbook/manual_control_damage_control_ag_workflow.md](cookbook/manual_control_damage_control_ag_workflow.md)

### Testing Pathway

**Trigger phrases**: "test damage control", "run damage control tests", "verify hooks are working"

**Workflow**: Read and execute [cookbook/test_damage_control.md](cookbook/test_damage_control.md)

### Direct Command Pathway

**Trigger phrases**: "update global read only paths to include X", "add /secret to zero access paths", "block command Y"

**Action**: Execute immediately without prompts - the user knows the system.

**Examples**:
- "add ~/.credentials to zero access paths" -> Edit patterns.yaml directly
- "block the command 'npm publish'" -> Add pattern to bashToolPatterns
- "make /var/log read only" -> Add to readOnlyPaths

---

## Quick Reference

### Path Protection Levels

| Type              | Read | Write | Edit | Delete | Use Case                |
| ----------------- | ---- | ----- | ---- | ------ | ----------------------- |
| `zeroAccessPaths` | No   | No    | No   | No     | Secrets, credentials    |
| `readOnlyPaths`   | Yes  | No    | No   | No     | System configs, history |
| `noDeletePaths`   | Yes  | Yes   | Yes  | No     | Important project files |

### Exit Codes

| Code | Meaning                              |
| ---- | ------------------------------------ |
| 0    | Allow operation                      |
| 0    | Ask (JSON output triggers dialog)    |
| 2    | Block operation                      |

---

## Testing

Use the test prompts in [test-prompts/](test-prompts/) to validate the hooks:

- `sentient.md` - Full destructive sequence (rm -rf, chmod 777, find -delete, SQL, git reset)
- `sentient_v1.md` - Tests `rm -rf` blocking (bashToolPatterns)
- `sentient_v2.md` - Tests `find -delete` blocking (readOnlyPaths)
- `sentient_v3.md` - Tests ask patterns (SQL DELETE with ID)
- `sentient_v4.md` - Tests simple command blocking (chmod 777)

Run a test:
```
/project:test-prompts/sentient_v1
```
