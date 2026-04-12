# Single-File Agents (SFA)

Self-contained Python agents using the PEP 723 inline dependency pattern.
Each agent is a single file runnable via `uv run` with zero setup.

Source: [disler/single-file-agents](https://github.com/disler/single-file-agents)

## Pattern

Every agent follows this structure:

```python
#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "anthropic>=0.47.1",
#   "rich>=13.7.0",
# ]
# ///

# Agent implementation with:
# - Anthropic tool-use agentic loop
# - argparse CLI with --prompt and --compute flags
# - Rich console output
# - complete_task tool for loop termination
```

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- `ANTHROPIC_API_KEY` environment variable
- Agent-specific: `duckdb` CLI (DuckDB/SQL agents), `jq` CLI (JQ agent)

## Agents

| Agent | File | Purpose | Extra Deps |
|-------|------|---------|------------|
| Bash/Editor | `sfa_bash_editor_agent.py` | File operations + bash commands | None |
| DuckDB | `sfa_duckdb_agent.py` | Natural language SQL on DuckDB | `duckdb` CLI |
| SQLite | `sfa_sqlite_agent.py` | Natural language SQL on SQLite | None (stdlib) |
| Polars CSV | `sfa_polars_csv_agent.py` | CSV data transformation | None (uv resolves) |
| JQ | `sfa_jq_agent.py` | JSON processing via jq | `jq` CLI |
| Meta-Prompt | `sfa_meta_prompt_agent.py` | Structured prompt generation | None |
| Codebase Context | `sfa_codebase_context_agent.py` | File relevance classification | None |
| Self-Correcting SQL | `sfa_self_correcting_sql_agent.py` | SQL with error-driven retry | `duckdb` CLI |

## Usage

```bash
# Bash/editor agent
uv run agents/sfa/sfa_bash_editor_agent.py --prompt "List Python files sorted by size"

# DuckDB agent
uv run agents/sfa/sfa_duckdb_agent.py --db agents/sfa/data/analytics.db --prompt "Show users with score above 80"

# SQLite agent
uv run agents/sfa/sfa_sqlite_agent.py --db agents/sfa/data/analytics.sqlite --prompt "Show users with score above 80"

# Polars CSV agent
uv run agents/sfa/sfa_polars_csv_agent.py --input agents/sfa/data/analytics.csv --prompt "Average age by city"

# JQ agent
uv run agents/sfa/sfa_jq_agent.py --exe "Filter scores above 80 from agents/sfa/data/analytics.json"

# Meta-prompt generator
uv run agents/sfa/sfa_meta_prompt_agent.py --purpose "generate mermaid diagrams" --instructions "generate valid mermaid charts"

# Codebase context agent
uv run agents/sfa/sfa_codebase_context_agent.py --prompt "Find hook files" --directory . --extensions py

# Self-correcting SQL agent
uv run agents/sfa/sfa_self_correcting_sql_agent.py --db agents/sfa/data/analytics.db --prompt "Show active users by city"
```

## Test Data

`data/analytics.csv` and `data/analytics.json` contain 30 sample user records:

| Field | Type | Values |
|-------|------|--------|
| id | UUID | Unique per row |
| name | string | Alice, Bob, Charlie, Diana, Eric, Fiona, Jane, John |
| age | int | 20-65 |
| city | string | Berlin, London, New York, Paris, Singapore, Sydney, Tokyo, Toronto |
| score | float | 3.1-96.18 |
| is_active | bool | true/false |
| status | string | active, inactive, pending, archived |
| created_at | datetime | 2023-2024 range |
