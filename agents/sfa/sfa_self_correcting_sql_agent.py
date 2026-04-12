#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "anthropic>=0.47.1",
#   "rich>=13.7.0",
# ]
# ///

# Requires: duckdb CLI (brew install duckdb)

"""
/// Example Usage

uv run agents/sfa/sfa_self_correcting_sql_agent.py --db ./data/analytics.db --prompt "Show active users by city"
uv run agents/sfa/sfa_self_correcting_sql_agent.py --db ./data/analytics.db --prompt "Calculate average score per status" --max-retries 5

///
"""

import os
import sys
import json
import argparse
import subprocess

from anthropic import Anthropic  # ty: ignore[unresolved-import]
from rich.console import Console  # ty: ignore[unresolved-import]
from rich.panel import Panel  # ty: ignore[unresolved-import]
from rich.table import Table  # ty: ignore[unresolved-import]

# Initialize rich console
console = Console()

# Global database path — set in main() before agent loop
DB_PATH: str = ""

# Maximum SQL correction attempts — set in main() from --max-retries
MAX_RETRIES: int = 3

# Tracks each SQL attempt: attempt number, query text, error or None, success flag
CORRECTION_LOG: list = []

AGENT_PROMPT = """<purpose>
    You are a self-correcting SQL expert. Your goal is to generate DuckDB SQL queries
    that satisfy the user's request. When a query fails, analyze the error message,
    identify the issue, and generate a corrected query.
</purpose>

<instructions>
    <instruction>Start by calling execute_sql with your best attempt at the query.</instruction>
    <instruction>If execute_sql returns an error, analyze the error message carefully.</instruction>
    <instruction>Call execute_sql again with a corrected query that addresses the specific error.</instruction>
    <instruction>Repeat until the query succeeds or you've exhausted your attempts.</instruction>
    <instruction>When you have a successful result, call complete_task with the final query and result.</instruction>
    <instruction>Provide detailed reasoning with every tool call explaining your approach.</instruction>
    <instruction>Never give up after a single error — analyze and correct.</instruction>
</instructions>

<user-request>
    {{user_request}}
</user-request>
"""

tools = [
    {
        "name": "execute_sql",
        "description": "Execute a SQL query against the DuckDB database. If the query fails, analyze the error and call execute_sql again with a corrected query.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Explain why this query should work, or what you changed to fix the previous error",
                },
                "sql_query": {
                    "type": "string",
                    "description": "The SQL query to execute",
                },
            },
            "required": ["reasoning", "sql_query"],
        },
    },
    {
        "name": "complete_task",
        "description": "Finalize the task after getting a successful SQL result. Show the correction history.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Explain how the final query satisfies the user request",
                },
                "final_sql": {
                    "type": "string",
                    "description": "The final successful SQL query",
                },
                "final_result": {
                    "type": "string",
                    "description": "The query result to show the user",
                },
            },
            "required": ["reasoning", "final_sql", "final_result"],
        },
    },
]


def execute_sql(reasoning: str, sql_query: str) -> dict:
    """Run a SQL query via the duckdb CLI and log the attempt.

    Args:
        reasoning: Why this query should work, or what was changed to fix a prior error.
        sql_query: The SQL query to execute.

    Returns:
        Dict with key "result" on success, or "error" on failure.
    """
    attempt_number = len(CORRECTION_LOG) + 1

    # Enforce max retries
    failed_attempts = sum(1 for e in CORRECTION_LOG if not e["success"])
    if failed_attempts >= MAX_RETRIES:
        console.log(f"[red]Max retries ({MAX_RETRIES}) reached. Stopping.[/red]")
        return {"error": f"Max retries ({MAX_RETRIES}) exhausted. Call complete_task with the best result so far."}

    console.log(
        f"[blue]Execute SQL Tool[/blue] - Attempt {attempt_number} - Reasoning: {reasoning}"
    )
    console.log(f"[dim]Query: {sql_query}[/dim]")

    result = subprocess.run(
        ["duckdb", DB_PATH, "-c", sql_query],
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        stderr = result.stderr.strip()
        CORRECTION_LOG.append(
            {
                "attempt": attempt_number,
                "query": sql_query,
                "error": stderr,
                "success": False,
            }
        )
        console.log(f"[red]SQL Error:[/red] {stderr}")
        return {"error": stderr}

    stdout = result.stdout
    CORRECTION_LOG.append(
        {
            "attempt": attempt_number,
            "query": sql_query,
            "error": None,
            "success": True,
        }
    )
    console.log(f"[green]SQL Success[/green] - {len(stdout.splitlines())} lines returned")
    return {"result": stdout}


def complete_task(reasoning: str, final_sql: str, final_result: str) -> dict:
    """Print correction log summary and final result, then signal loop exit.

    Args:
        reasoning: How the final query satisfies the user request.
        final_sql: The final successful SQL query.
        final_result: The query result to show the user.

    Returns:
        Dict with key "result" set to "Task completed".
    """
    # Print correction history table
    table = Table(title="SQL Correction History")
    table.add_column("Attempt", style="cyan")
    table.add_column("Query", style="dim")
    table.add_column("Result", style="green")
    for entry in CORRECTION_LOG:
        status = (
            "[green]Success[/green]"
            if entry["success"]
            else f"[red]Error: {entry['error'][:60]}[/red]"
        )
        table.add_row(str(entry["attempt"]), entry["query"][:80], status)
    console.print(table)

    total = len(CORRECTION_LOG)
    failures = sum(1 for e in CORRECTION_LOG if not e["success"])
    console.print(
        Panel(
            f"Total attempts: {total}  |  Failures: {failures}  |  "
            f"Reasoning: {reasoning}",
            title="Task Complete",
        )
    )
    console.print("\n[green]Final SQL:[/green]")
    console.print(final_sql)
    console.print("\n[green]Final Result:[/green]")
    console.print(final_result)

    return {"result": "Task completed"}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Self-Correcting SQL Agent using Anthropic API + DuckDB"
    )
    parser.add_argument("-d", "--db", required=True, help="Path to DuckDB database file")
    parser.add_argument("-p", "--prompt", required=True, help="The user's natural language query")
    parser.add_argument(
        "-c",
        "--compute",
        type=int,
        default=10,
        help="Maximum number of agent loops (default: 10)",
    )
    parser.add_argument(
        "-r",
        "--max-retries",
        type=int,
        default=3,
        help="Maximum SQL correction attempts (default: 3)",
    )
    args = parser.parse_args()

    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        console.print(
            "[red]Error: ANTHROPIC_API_KEY environment variable is not set[/red]"
        )
        console.print("Please get your API key from your Anthropic dashboard")
        console.print("Then set it with: export ANTHROPIC_API_KEY='your-api-key-here'")
        sys.exit(1)

    # Validate DB path
    if not os.path.isfile(args.db):
        console.print(f"[red]Error: Database file not found: {args.db}[/red]")
        sys.exit(1)

    # Set global state for tool functions
    global DB_PATH, MAX_RETRIES
    DB_PATH = args.db
    MAX_RETRIES = args.max_retries

    client = Anthropic()

    completed_prompt = AGENT_PROMPT.replace("{{user_request}}", args.prompt)
    messages = [{"role": "user", "content": completed_prompt}]

    compute_iterations = 0
    break_loop = False

    # Main agent loop
    while True:
        if break_loop:
            break

        console.rule(
            f"[yellow]Agent Loop {compute_iterations + 1}/{args.compute}[/yellow]"
        )
        compute_iterations += 1

        if compute_iterations >= args.compute:
            console.print(
                "[yellow]Warning: Reached maximum compute loops without completing task[/yellow]"
            )
            raise Exception(
                f"Maximum compute loops reached: {compute_iterations}/{args.compute}"
            )

        try:
            response = client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=5000,
                messages=messages,  # type: ignore[arg-type]
                tools=tools,  # type: ignore[arg-type]
                thinking={"type": "enabled", "budget_tokens": 2048},
                tool_choice={"type": "any"},
            )

            # Extract thinking, tool_use, and text blocks from response
            thinking_block = None
            tool_use_block = None
            text_block = None
            tool_name = ""
            tool_input: dict = {}
            tool_id = ""

            for content_block in response.content:
                if content_block.type == "thinking":
                    thinking_block = content_block
                elif content_block.type == "tool_use":
                    tool_use_block = content_block
                    tool_name = content_block.name
                    tool_input = content_block.input  # type: ignore[assignment]
                    tool_id = content_block.id
                elif content_block.type == "text":
                    text_block = content_block
                    console.print(f"[cyan]Model response:[/cyan] {content_block.text}")

            # If only text, no tool call — append and continue
            if not tool_use_block and text_block:
                messages.append(  # type: ignore[arg-type]
                    {
                        "role": "assistant",
                        "content": [
                            *([thinking_block] if thinking_block else []),
                            {"type": "text", "text": text_block.text},
                        ],
                    }
                )
                continue

            if tool_use_block:
                console.print(
                    f"[blue]Tool Call:[/blue] {tool_name}({json.dumps(tool_input, indent=2)})"
                )

                try:
                    if tool_name == "execute_sql":
                        result = execute_sql(
                            reasoning=tool_input["reasoning"],
                            sql_query=tool_input["sql_query"],
                        )
                    elif tool_name == "complete_task":
                        result = complete_task(
                            reasoning=tool_input["reasoning"],
                            final_sql=tool_input["final_sql"],
                            final_result=tool_input["final_result"],
                        )
                        break_loop = True
                    else:
                        raise Exception(f"Unknown tool call: {tool_name}")

                    console.print(
                        f"[blue]Tool Call Result:[/blue] {tool_name}(...) ->\n{result}"
                    )

                    messages.append(  # type: ignore[arg-type]
                        {
                            "role": "assistant",
                            "content": [
                                *([thinking_block] if thinking_block else []),
                                {
                                    "type": "tool_use",
                                    "id": tool_id,
                                    "name": tool_name,
                                    "input": tool_input,
                                },
                            ],
                        }
                    )

                    messages.append(  # type: ignore[arg-type]
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_id,
                                    "content": str(result),
                                }
                            ],
                        }
                    )

                except Exception as e:
                    error_msg = f"Error executing {tool_name}: {e}"
                    console.print(f"[red]{error_msg}[/red]")

                    messages.append(  # type: ignore[arg-type]
                        {
                            "role": "assistant",
                            "content": [
                                *([thinking_block] if thinking_block else []),
                                {
                                    "type": "tool_use",
                                    "id": tool_id,
                                    "name": tool_name,
                                    "input": tool_input,
                                },
                            ],
                        }
                    )

                    messages.append(  # type: ignore[arg-type]
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_id,
                                    "content": error_msg,
                                }
                            ],
                        }
                    )

        except Exception as e:
            console.print(f"[red]Error in agent loop: {str(e)}[/red]")
            raise e


if __name__ == "__main__":
    main()
