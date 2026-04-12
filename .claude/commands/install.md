---
description: Two-phase bootstrap — install tools and verify environment
---

# /install — Environment Bootstrap

## Purpose

Set up a fresh ArhuGula development environment with all required tools.

## Manual Prerequisites (user must complete before running)

| Permission | How to Enable |
|-----------|--------------|
| Accessibility | System Preferences > Privacy & Security > Accessibility |
| Screen Recording | System Preferences > Privacy & Security > Screen Recording |
| Full Disk Access | System Preferences > Privacy & Security > Full Disk Access |

## Phase 1: Install

Run each command. Report PASS/FAIL for each step.

1. `brew install tmux just uv yq node@22`
2. `xcode-select --install` (skip if already installed, required for sub-project 4)
3. `npm install -g @anthropic-ai/claude-code` (if not already installed)
4. Pi Agent: `bun add -g @mariozechner/pi-coding-agent` (global install via bun)
5. Playwright CLI: `npm install -g --ignore-scripts @playwright/cli@latest` (required for SP14 playwright-bowser skill; `--ignore-scripts` blocks arbitrary postinstall code, which is a supply-chain risk per SP14 round-2 hardening S-07)
6. Playwright browsers: `npx playwright install chromium` (one-time Chromium download for headless runs)
7. `uv sync`
8. `cp .env.example .env` (if .env does not exist)
9. `sudo pmset -a sleep 0 displaysleep 0 disksleep 0 powernap 0` (macOS only)

## Phase 2: Verify

Run each check. Report PASS/FAIL/SKIP with actual version.

| # | Check | Command | Minimum |
|---|-------|---------|---------|
| 1 | brew | `brew --version` | any |
| 2 | swift | `swift --version` | 5.9+ (SKIP for sub-projects 1-3) |
| 3 | tmux | `tmux -V` | 3.0+ |
| 4 | just | `just --version` | 1.0+ |
| 5 | uv | `uv --version` | 0.4+ |
| 6 | yq | `yq --version` | 4.0+ |
| 7 | claude | `claude --version` | pinned range |
| 8 | node | `node --version` | 22.x |
| 9 | pi | `pi --version` | any |
| 10 | playwright-cli | `playwright-cli --version` | any (SP14 playwright-bowser skill) |
| 11 | playwright chromium | `npx playwright install --dry-run chromium` | installed (SP14 headless runs) |
| 12 | chrome mcp | `claude mcp list \| grep -i chrome` | `claude --chrome` support (SP14 claude-bowser skill; SKIP if not yet configured) |

## Report

Present results as a markdown table with Status (PASS/FAIL/SKIP) and Version columns.
