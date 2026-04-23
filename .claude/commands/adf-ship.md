---
description: Stage, commit, and push ADF (agent-deployment-framework) in one shot from ArhuGula session. Autogenerates commit message from diff unless message provided as argument.
allowed-tools: Bash, Write
---

# Git Ship — ADF

ADF repo is at `~/Projects/agent-deployment-framework`. All git commands use `git -C ~/Projects/agent-deployment-framework`.

## Step 1 — Inspect changes

Run `git -C ~/Projects/agent-deployment-framework status --short` and `git -C ~/Projects/agent-deployment-framework diff HEAD` to understand what changed.

Check for sensitive files (.env, credentials, secrets, private keys). If any are staged or modified, stop and warn the user — do not include them.

## Step 2 — Determine commit message

If `$ARGUMENTS` is non-empty, use it verbatim as the commit message body.

If `$ARGUMENTS` is empty, generate a conventional commit message from the diff:
- Format: `type(scope): short description`
- Types: feat, fix, chore, docs, refactor, test
- Keep the subject line under 72 characters
- Add a one-line body only if the change needs explanation

## Step 3 — Write message to temp file

Write the commit message to `/tmp/adf-commit.txt`.

## Step 4 — Output the ship command

Identify the modified/untracked files from git status. Exclude any sensitive files. Use paths relative to the ADF root.

Show the commit message, then output this single command for the user to run:

```
! git -C ~/Projects/agent-deployment-framework add <file1> <file2> ... && git -C ~/Projects/agent-deployment-framework commit -F /tmp/adf-commit.txt && git -C ~/Projects/agent-deployment-framework push origin main
```

Use specific file names from git status, not `-A`.
