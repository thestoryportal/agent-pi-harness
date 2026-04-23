---
description: Stage and commit ArhuGula changes. Autogenerates commit message from diff unless message provided as argument.
allowed-tools: Bash, Write
---

# Git Commit — ArhuGula

## Step 1 — Inspect changes

Run `git status --short` and `git diff HEAD` to understand what changed.

Check for sensitive files (.env, credentials, secrets, private keys). If any are staged or modified, stop and warn the user — do not include them.

## Step 2 — Determine commit message

If `$ARGUMENTS` is non-empty, use it verbatim as the commit message body.

If `$ARGUMENTS` is empty, generate a conventional commit message from the diff:
- Format: `type(scope): short description`
- Types: feat, fix, chore, docs, refactor, test
- Keep the subject line under 72 characters
- Add a one-line body only if the change needs explanation

## Step 3 — Write message to temp file

Write the commit message to `/tmp/arhugula-commit.txt`.

## Step 4 — Output the command

Identify the modified/untracked files from git status. Exclude any sensitive files.

Output this block for the user to run:

```
! git add <file1> <file2> ... && git commit -F /tmp/arhugula-commit.txt
```

Use specific file names from git status, not `-A`. Show the commit message so the user can verify it before running.
