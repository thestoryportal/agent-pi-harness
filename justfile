set dotenv-load := true
set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

# === Layer 1: Skill — these recipes invoke Layer 1 skills ===

# Load full project context
prime:
    claude --dangerously-skip-permissions "/prime"

# Evaluate prompt quality (HOP/LOP)
scout:
    claude --dangerously-skip-permissions "/scout"

# === Layer 2: Subagent — these recipes invoke Layer 2 subagents ===

# Invoke builder subagent
build:
    claude --dangerously-skip-permissions "/build"

# Multi-model consensus review
review:
    claude --dangerously-skip-permissions "/review"

# === Layer 3: Command — these recipes invoke Layer 3 slash commands ===

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

# Start Observe dashboard
observe:
    uv run apps/observe/main.py

# Prune Observe events older than retention window
db-prune:
    uv run apps/observe/prune.py
