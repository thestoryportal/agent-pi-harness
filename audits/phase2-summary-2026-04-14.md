# Phase 2 SP Fan-out Summary

**Date:** 2026-04-14
**Branch:** audit/identicality-2026-04-13
**SPs targeted:** 16
**Mailbox entries:** 16

## Results by verdict

### PASS (2)
- **SP1** — 1 iter(s), 0 finding(s)
- **SP10** — 1 iter(s), 0 finding(s)

### FAIL (0)
- (none)

### ESCALATE (14)
- **SP11** — 3 iter(s), 5 finding(s)
- **SP12** — 3 iter(s), 4 finding(s)
- **SP13** — 1 iter(s), 2 finding(s)
- **SP14** — 0 iter(s), 0 finding(s)
- **SP15** — 0 iter(s), 0 finding(s)
- **SP16** — 0 iter(s), 0 finding(s)
- **SP2** — 0 iter(s), 0 finding(s)
- **SP3** — 0 iter(s), 0 finding(s)
- **SP4** — 1 iter(s), 0 finding(s)
- **SP5** — 1 iter(s), 0 finding(s)
- **SP6** — 1 iter(s), 1 finding(s)
- **SP7** — 0 iter(s), 0 finding(s)
- **SP8** — 1 iter(s), 4 finding(s)
- **SP9** — 1 iter(s), 5 finding(s)

## Per-SP details

### SP1 — PASS
- Iterations: 1
- Coder model: anthropic:claude-haiku-4-5
- Validator model: openai:o4-mini

### SP10 — PASS
- Iterations: 1
- Coder model: anthropic:claude-haiku-4-5
- Validator model: openai:o4-mini

### SP11 — ESCALATE
- Iterations: 3
- Coder model: anthropic:claude-haiku-4-5
- Validator model: openai:o4-mini
- Escalate reason: fabricated findings detected
- Findings (5):
  - [P1] apps/prompt-testing/custom_models/groq-mistral.js:1 — file not found or content does not match
  - [P1] apps/prompt-testing/run_local_llm.sh:1 — file not found
  - [P2] apps/prompt-testing/package.json:1 — package.json exists but does not list the specified dependencies
  - [P2] apps/prompt-testing/nlq_to_sql/prompt.txt:1 — file not found
  - [P3] apps/prompt-testing/custom_models/groq-mistral.js:45 — file not found or content mismatch

### SP12 — ESCALATE
- Iterations: 3
- Coder model: anthropic:claude-haiku-4-5
- Validator model: openai:o4-mini
- Escalate reason: P0 unresolved at iteration cap (3/3)
- Findings (4):
  - [P0] apps/listen/worker.py:95 — claude_cmd = (
        f"claude --dangerously-skip-permissions"
        f' --app
  - [P0] apps/listen/main.py:60 — job_file = JOBS_DIR / f"{job_id}.yaml"
    if not job_file.exists():
        rai
  - [P0] apps/listen/main.py:75 — def stop_job(job_id: str):
    job_file = JOBS_DIR / f"{job_id}.yaml"
    if not
  - [P0] apps/listen/worker.py:88 — escaped = tmux_cmd.replace("\\", "\\\\").replace('"', '\\"')
    subprocess.run(

### SP13 — ESCALATE
- Iterations: 1
- Coder model: anthropic:claude-haiku-4-5
- Validator model: openai:o4-mini
- Escalate reason: fabricated findings
- Findings (2):
  - [P3] apps/steer:0 — Directory not found in repository at apps/steer
  - [P3] .claude/skills/steer:0 — Directory not found in repository at .claude/skills/steer

### SP14 — ESCALATE
- Iterations: 0
- Coder model: unknown
- Validator model: unknown
- Escalate reason: E2B sandbox rate limit (429): maximum 20 concurrent sandboxes reached. Cannot create new sandbox. Requires cleanup of existing sandboxes or quota increase.

### SP15 — ESCALATE
- Iterations: 0
- Coder model: unknown
- Validator model: unknown
- Escalate reason: E2B sandbox creation failed: 429 Rate limit exceeded - maximum number of concurrent E2B sandboxes (20) reached. Cannot proceed with audit.

### SP16 — ESCALATE
- Iterations: 0
- Coder model: unknown
- Validator model: unknown
- Escalate reason: E2B rate limit exceeded: maximum number of concurrent sandboxes (20) reached. Cannot create new sandbox for audit.

### SP2 — ESCALATE
- Iterations: 0
- Coder model: unknown
- Validator model: unknown
- Escalate reason: SFA process failed with exit code 1 during agents/sfa/sfa_coder_validator_loop.py execution. Error message: 'Aborted!' - likely indicates upstream agent or validator failure.

### SP3 — ESCALATE
- Iterations: 0
- Coder model: unknown
- Validator model: unknown
- Escalate reason: MCP server failed to register mcp__e2b_sandbox__create_sandbox tool after 3 warmup retry attempts. Cannot initialize sandbox for audit.

### SP4 — ESCALATE
- Iterations: 1
- Coder model: anthropic:claude-haiku-4-5
- Validator model: openai:o4-mini
- Escalate reason: Mismatched sp_id: expected SP15 scope but got SP4

### SP5 — ESCALATE
- Iterations: 1
- Coder model: anthropic:claude-haiku-4-5
- Validator model: openai:o4-mini
- Escalate reason: Empty sp_scope prevents validation

### SP6 — ESCALATE
- Iterations: 1
- Coder model: anthropic:claude-haiku-4-5
- Validator model: openai:o4-mini
- Escalate reason: fabricated finding
- Findings (1):
  - [P0] skills/library:0 — File or directory 'skills/library' does not exist in the repo

### SP7 — ESCALATE
- Iterations: 0
- Coder model: unknown
- Validator model: unknown
- Escalate reason: SFA exited with code 1: 'Error: Aborted!' with no further error details from sfa_coder_validator_loop.py invocation

### SP8 — ESCALATE
- Iterations: 1
- Coder model: anthropic:claude-haiku-4-5
- Validator model: openai:o4-mini
- Escalate reason: fabricated findings
- Findings (4):
  - [P2] apps/drive/main.py:3 — Relative imports from 'commands.*' modules without explicit package structure ve
  - [P3] apps/drive/main.py:1 — Unable to run ruff static checks on apps/drive directory due to tool limitations
  - [P1] audits/exceptions.md:1 — Exception 20 referenced in spec_refs but full exceptions.md file could not be co
  - [P2] apps/listen:1 — apps/listen/** directory not accessible for review. Cannot inspect for command i

### SP9 — ESCALATE
- Iterations: 1
- Coder model: anthropic:claude-haiku-4-5
- Validator model: openai:o4-mini
- Escalate reason: Fabricated findings
- Findings (5):
  - [P1] .claude/commands/infinite.md:1 — File describes 'INFINITE AGENTIC LOOP COMMAND' that orchestrates parallel sub-ag
  - [P0] .claude/commands/infinite.md:45 — Lines 45-65 describe 'Parallel Agent Coordination' with 'Sub-Agent Distribution 
  - [P1] .claude/agents/meta-agent.md:1 — File describes a sub-agent generator that creates new agent configuration files.
  - [P0] .claude/agents/meta-agent.md:14 — Lines 14-17 instruct the agent to 'Scrape the Claude Code sub-agent feature to g
  - [P2] .claude/commands/infinite.md:1 — File contains no attribution to IndyDevDan source or upstream Disler repository.
