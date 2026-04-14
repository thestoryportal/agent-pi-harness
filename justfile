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

# Claude maintenance + run /maintenance
cldmm:
    claude --maintenance "/maintenance"

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

# Bash/editor agent (Anthropic tool use)
sfa-bash PROMPT:
    uv run agents/sfa/sfa_bash_editor_agent_anthropic_v3.py --prompt "{{PROMPT}}"

# DuckDB query agent (Anthropic)
sfa-duckdb DB PROMPT:
    uv run agents/sfa/sfa_duckdb_anthropic_v2.py --db "{{DB}}" --prompt "{{PROMPT}}"

# SQLite query agent (OpenAI)
sfa-sqlite DB PROMPT:
    uv run agents/sfa/sfa_sqlite_openai_v2.py --db "{{DB}}" --prompt "{{PROMPT}}"

# Polars CSV analysis agent (Anthropic)
sfa-polars INPUT PROMPT:
    uv run agents/sfa/sfa_polars_csv_agent_anthropic_v3.py --input "{{INPUT}}" --prompt "{{PROMPT}}"

# JQ JSON processing agent (Gemini)
sfa-jq PROMPT:
    uv run agents/sfa/sfa_jq_gemini_v1.py --exe "{{PROMPT}}"

# Meta-prompt generator (OpenAI)
sfa-metaprompt PURPOSE INSTRUCTIONS:
    uv run agents/sfa/sfa_meta_prompt_openai_v1.py --purpose "{{PURPOSE}}" --instructions "{{INSTRUCTIONS}}"

# Codebase context discovery agent
sfa-context PROMPT DIR="." EXT="py":
    uv run agents/sfa/sfa_codebase_context_agent_v3.py --prompt "{{PROMPT}}" --directory "{{DIR}}" --extensions "{{EXT}}"

# === Layer 4: Just — infrastructure app recipes ===
# SP8 recipes match upstream mac-mini-agent justfile interface (byte-identical
# command patterns). Uses per-app CWD + bare `python main.py` invocations.

_sandbox_url := env("AGENT_SANDBOX_URL", "")
default_url := if _sandbox_url == "" { "http://localhost:7600" } else { _sandbox_url }

# Start the listen server
listen:
    cd apps/listen && uv run python main.py

# Send a job to the listen server
send prompt url=default_url:
    cd apps/direct && uv run python main.py start {{url}} "{{prompt}}"

# Send a job from a local file
sendf file url=default_url:
    #!/usr/bin/env bash
    prompt="$(cat '{{file}}')"
    cd apps/direct && uv run python main.py start '{{url}}' "$prompt"

# Get a job's status
job id url=default_url:
    cd apps/direct && uv run python main.py get {{url}} {{id}}

# List all jobs (pass --archived to see archived)
jobs *flags:
    cd apps/direct && uv run python main.py list {{default_url}} {{flags}}

# Show full details of the latest N jobs (default: 1)
latest n="1" url=default_url:
    cd apps/direct && uv run python main.py latest {{url}} {{n}}

# Stop a running job
stop id url=default_url:
    cd apps/direct && uv run python main.py stop {{url}} {{id}}

# Archive all jobs
clear url=default_url:
    cd apps/direct && uv run python main.py clear {{url}}

# Prune Observe events older than retention window
db-prune:
    uv run apps/observe/prune.py

# Start Drop Zone watcher (reads drops.yaml from apps/dropzone/)
dropzone:
    cd apps/dropzone && uv run sfs_agentic_drop_zone.py

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

# Pi with pi-pi meta-agent (builds Pi components via expert research)
pi-pi:
    pi -e extensions/pi-pi.ts -e extensions/theme-cycler.ts

# Pi with cross-agent compatibility (loads .claude/ commands + agents)
pi-cross:
    pi -e extensions/cross-agent.ts -e extensions/theme-cycler.ts

# Pi with system prompt selector (/system to pick agent persona)
pi-system:
    pi -e extensions/system-select.ts -e extensions/minimal.ts -e extensions/theme-cycler.ts

# Pi with subagent widget (/sub, /subcont, /subclear)
pi-sub:
    pi -e extensions/subagent-widget.ts -e extensions/theme-cycler.ts

# Pi with agent-im chat room (scaffold)
pi-im:
    pi -e extensions/agent-im.ts -e extensions/theme-cycler.ts

# Pi with agent-forge evolutionary tools (scaffold)
pi-forge:
    pi -e extensions/agent-forge.ts -e extensions/theme-cycler.ts

# Pi with chronicle state machine (scaffold)
pi-chronicle:
    pi -e extensions/chronicle.ts -e extensions/agent-team.ts -e extensions/theme-cycler.ts

# Pi with domain ownership enforcement + team dispatch
pi-team-safe:
    pi -e extensions/agent-team.ts -e extensions/domain-ownership.ts -e extensions/theme-cycler.ts

# Pi with full harness: team + domain + damage-control + chain
pi-harness:
    pi -e extensions/agent-team.ts -e extensions/domain-ownership.ts -e extensions/damage-control.ts -e extensions/agent-chain.ts -e extensions/theme-cycler.ts

# === SP13: Steer GUI Automation ===

# Build steer Swift CLI (release mode)
steer-build:
    cd apps/steer && swift build -c release 2>&1

# Take a screenshot of the primary screen
steer-see:
    apps/steer/.build/release/steer see --screen 0 --json

# List running apps
steer-apps:
    apps/steer/.build/release/steer apps list --json

# OCR the primary screen
steer-ocr:
    apps/steer/.build/release/steer ocr --screen 0 --store --json

# === SP14: Browser Automation ===

# Playwright skill — direct headless/headed capability test
test-playwright-skill headed="true" prompt="Get the current date, then go to https://simonwillison.net/, find the latest blog post, summarize it, and give it a rating out of 10.":
    claude "/playwright-bowser (headed: {{headed}}) {{prompt}}"

# Chrome MCP skill — direct (requires claude --chrome session)
test-chrome-skill prompt="Get the current date, then go to https://simonwillison.net/, find the latest blog post, summarize it, and give it a rating out of 10.":
    claude --chrome "/claude-bowser {{prompt}}"

# Playwright subagent — isolated parallel browser session
test-playwright-agent headed="true" prompt="Get the current date, then go to https://simonwillison.net/, find the latest blog post, summarize it, and give it a rating out of 10.":
    claude "Use a @playwright-bowser-agent to do this: (headed: {{headed}}) {{prompt}}"

# Chrome subagent — single-instance browser (requires --chrome)
test-chrome-agent prompt="Get the current date, then go to https://simonwillison.net/, find the latest blog post, summarize it, and give it a rating out of 10.":
    claude --chrome "Use a @claude-bowser-agent to do this: {{prompt}}"

# QA agent — structured user story validation
test-qa headed="true" prompt="Navigate to https://news.ycombinator.com/. Verify the front page loads with posts. Click 'More' to go to the next page. Verify page 2 loads with a new set of posts. Go back to page 1. Click into the first post's comments link. Verify the comments page loads and at least one comment is visible.":
    claude "Use a @bowser-qa-agent: (headed: {{headed}}) {{prompt}}"

# Run a saved browser automation workflow via hop-automate (requires --chrome for claude-bowser workflows)
# Note (SP14 round-10 S-05): {{prompt}} and {{flags}} are shell-interpolated
# directly into the claude command. An unquoted prompt containing shell
# metacharacters (e.g. `$(...)`, backticks, `;`) will be interpreted by the
# shell. This is user-level self-harm only, not an agent-escalation vector
# (the user invoking the recipe is the one running the shell), but quote the
# prompt if it contains special characters: just hop workflow 'my prompt'.
hop workflow="amazon-add-to-cart" prompt="pack of 10 sketch notebooks" *flags="":
    export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 && claude --chrome "/bowser:hop-automate {{workflow}} {{prompt}} {{flags}}"

# UI Review — parallel user story validation across all YAML stories in ai_review/user_stories/
# headed defaults to "false" (matches /ui-review command's own default). Pass headed="true" or "headed" to see the browser.
ui-review headed="false" filter="" *flags="":
    export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 && claude "/ui-review {{headed}} {{filter}} {{flags}}"

# Amazon add-to-cart — multiple items in one shot (requires --chrome)
automate-amazon prompt="m4 mac mini with top specs, flowers for valentines day, pack of 10 sketch notebooks":
    just hop amazon-add-to-cart "{{prompt}}"

# Summarize a blog's latest post (headless, no auth needed)
summarize-blog url="https://simonwillison.net/":
    claude "/bowser:hop-automate blog-summarizer \"{{url}}\" playwright headless"
