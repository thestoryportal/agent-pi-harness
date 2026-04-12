set dotenv-load := true
set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

# === Layer 1: Skill — interactive session with slash commands ===

# Load full project context
prime:
    claude "/prime"

# Spec analysis and task decomposition
scout:
    claude "/scout"

# === Layer 2: Subagent — interactive session with agent-backed commands ===

# Create implementation plan from scout output (architect agent)
architect:
    claude "/architect"

# Implementation via builder agent
build:
    claude "/build"

# Multi-agent consensus review (validator + spec-checker + security)
harness-review:
    claude "/harness-review"

# === Layer 3: Command — lifecycle slash commands ===

# Claude init session
cldi:
    claude --init

# Claude maintenance session
cldm:
    claude --maintenance

# Claude init + run /install
cldii:
    claude --init "/install"

# Claude maintenance + run /maintain
cldmm:
    claude --maintenance "/maintain"

# === Headless: Programmatic invocation via run-claude.py ===

# Headless project status report
prime-headless:
    python3 scripts/run-claude.py \
        --prompt "Report repository and environment status. Summarize git status, service health, and any missing setup." \
        --tools Read Grep Glob Bash \
        --approved-tools Read Grep Glob \
        --permission-mode dontAsk \
        --max-turns 10 \
        --workflow-id prime \
        --invocation-type headless

# Headless spec analysis
scout-headless SPEC:
    python3 scripts/run-claude.py \
        --prompt "Analyze {{SPEC}} and return implementation units with dependencies, risks, and validation steps." \
        --tools Read Grep Glob \
        --approved-tools Read Grep Glob \
        --permission-mode dontAsk \
        --max-turns 10 \
        --workflow-id scout \
        --invocation-type headless

# Headless code review against spec
review-headless SPEC:
    python3 scripts/run-claude.py \
        --prompt "Review the current diff against {{SPEC}} and return structured findings with severity, evidence, and recommended fixes." \
        --tools Read Grep Glob \
        --approved-tools Read Grep Glob \
        --permission-mode dontAsk \
        --max-turns 10 \
        --workflow-id harness-review \
        --invocation-type headless

# === Layer 4: Just — infrastructure app recipes ===

# Start Listen job server
listen:
    uv run apps/listen/main.py

# Send single command to Listen
send CMD:
    uv run apps/direct/main.py "{{CMD}}"

# Parallel dispatch from file (daily use)
fanout FILE:
    uv run apps/drive/main.py fanout --file "{{FILE}}"

# Drive session management
session CMD:
    uv run apps/drive/main.py session "{{CMD}}"

# Poll running sessions for completion
poll:
    uv run apps/drive/main.py poll

# List queued/running jobs
jobs:
    uv run apps/direct/main.py jobs

# Prune Observe events older than retention window
db-prune:
    uv run apps/observe/prune.py
