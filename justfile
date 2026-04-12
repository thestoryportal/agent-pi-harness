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

# === SP7: Single-File Agents ===

# Bash/editor agent
sfa-bash PROMPT:
    uv run agents/sfa/sfa_bash_editor_agent.py --prompt "{{PROMPT}}"

# DuckDB query agent
sfa-duckdb DB PROMPT:
    uv run agents/sfa/sfa_duckdb_agent.py --db "{{DB}}" --prompt "{{PROMPT}}"

# SQLite query agent
sfa-sqlite DB PROMPT:
    uv run agents/sfa/sfa_sqlite_agent.py --db "{{DB}}" --prompt "{{PROMPT}}"

# Polars CSV analysis agent
sfa-polars INPUT PROMPT:
    uv run agents/sfa/sfa_polars_csv_agent.py --input "{{INPUT}}" --prompt "{{PROMPT}}"

# JQ JSON processing agent
sfa-jq EXE:
    uv run agents/sfa/sfa_jq_agent.py --exe "{{EXE}}"

# Meta-prompt generator
sfa-metaprompt PURPOSE INSTRUCTIONS:
    uv run agents/sfa/sfa_meta_prompt_agent.py --purpose "{{PURPOSE}}" --instructions "{{INSTRUCTIONS}}"

# Codebase context discovery agent
sfa-context PROMPT DIR="." EXT="py":
    uv run agents/sfa/sfa_codebase_context_agent.py --prompt "{{PROMPT}}" --directory "{{DIR}}" --extensions "{{EXT}}"

# Self-correcting SQL agent
sfa-sql-correcting DB PROMPT:
    uv run agents/sfa/sfa_self_correcting_sql_agent.py --db "{{DB}}" --prompt "{{PROMPT}}"

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

# Start Drop Zone watcher (uses drops.yaml in cwd)
dropzone:
    uv run apps/dropzone/main.py watch

# Start Drop Zone watcher with custom config
dropzone-config CONFIG:
    uv run apps/dropzone/main.py watch --config "{{CONFIG}}"

# === SP11: Prompt Testing ===

# Evaluate builder agent prompt tests
eval-builder:
    npm run eval:builder

# Evaluate validator agent prompt tests
eval-validator:
    npm run eval:validator

# Evaluate scout agent prompt tests
eval-scout:
    npm run eval:scout

# Evaluate all agent prompt tests
eval-all:
    npm run eval:builder
    npm run eval:validator
    npm run eval:scout

# Open promptfoo results UI
promptfoo-view:
    npx promptfoo view

# === SP12: Pi Integration ===

# Launch Pi (default TUI)
pi:
    pi

# Pi with agent-team orchestrator + theme cycler
pi-team:
    pi -e extensions/agent-team.ts -e extensions/theme-cycler.ts

# Pi with agent-chain sequential pipeline + theme cycler
pi-chain:
    pi -e extensions/agent-chain.ts -e extensions/theme-cycler.ts

# Pi with damage-control safety rules + minimal + theme cycler
pi-safe:
    pi -e extensions/damage-control.ts -e extensions/minimal.ts -e extensions/theme-cycler.ts

# Pi with ArhuGula Drive dispatch
pi-drive:
    pi -e extensions/drive-dispatch.ts -e extensions/minimal.ts -e extensions/theme-cycler.ts

# Pi with ArhuGula Listen job submission
pi-listen:
    pi -e extensions/listen-submit.ts -e extensions/minimal.ts -e extensions/theme-cycler.ts

# Pi with full ArhuGula integration (Drive + Listen + damage-control)
pi-full:
    pi -e extensions/drive-dispatch.ts -e extensions/listen-submit.ts -e extensions/damage-control.ts -e extensions/theme-cycler.ts
