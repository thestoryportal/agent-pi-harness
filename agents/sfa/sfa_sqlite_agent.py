#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "anthropic>=0.47.1",
#   "rich>=13.7.0",
# ]
# ///

# Requires: Python sqlite3 (stdlib — no external install needed)

"""
/// Example Usage

# Run SQLite agent with default compute loops (10)
uv run agents/sfa/sfa_sqlite_agent.py -d ./data/analytics.sqlite -p "Show me all users with score above 80"

# Run with custom compute loops
uv run agents/sfa/sfa_sqlite_agent.py -d ./data/analytics.sqlite -p "Show me all users with score above 80" -c 5

///
"""

import os
import re
import sys
import json
import sqlite3
import argparse
from typing import List

from anthropic import Anthropic  # ty: ignore[unresolved-import]
from rich.console import Console  # ty: ignore[unresolved-import]
from rich.panel import Panel  # ty: ignore[unresolved-import]

# Initialize rich console
console = Console()

# Global database path — set in main() before agent loop
DB_PATH: str = ""


AGENT_PROMPT = """<purpose>
    You are a world-class expert at crafting precise SQLite SQL queries.
    Your goal is to generate accurate queries that exactly match the user's data needs.
</purpose>

<instructions>
    <instruction>Use the provided tools to explore the database and construct the perfect query.</instruction>
    <instruction>Start by listing tables to understand what's available.</instruction>
    <instruction>Describe tables to understand their schema and columns.</instruction>
    <instruction>Sample tables to see actual data patterns.</instruction>
    <instruction>Test queries before finalizing them.</instruction>
    <instruction>Only call run_final_sql_query when you're confident the query is perfect.</instruction>
    <instruction>Be thorough but efficient with tool usage.</instruction>
    <instruction>If you find your run_test_sql_query tool call returns an error or won't satisfy the user request, try to fix the query or try a different query.</instruction>
    <instruction>Think step by step about what information you need.</instruction>
    <instruction>Be sure to specify every parameter for each tool call.</instruction>
    <instruction>Every tool call should have a reasoning parameter which gives you a place to explain why you are calling the tool.</instruction>
</instructions>

<tools>
    <tool>
        <name>list_tables</name>
        <description>Returns list of available tables in the SQLite database</description>
        <parameters>
            <parameter>
                <name>reasoning</name>
                <type>string</type>
                <description>Why we need to list tables relative to user request</description>
                <required>true</required>
            </parameter>
        </parameters>
    </tool>

    <tool>
        <name>describe_table</name>
        <description>Returns schema info for specified SQLite table</description>
        <parameters>
            <parameter>
                <name>reasoning</name>
                <type>string</type>
                <description>Why we need to describe this table</description>
                <required>true</required>
            </parameter>
            <parameter>
                <name>table_name</name>
                <type>string</type>
                <description>Name of table to describe</description>
                <required>true</required>
            </parameter>
        </parameters>
    </tool>

    <tool>
        <name>sample_table</name>
        <description>Returns sample rows from specified SQLite table, always specify row_sample_size</description>
        <parameters>
            <parameter>
                <name>reasoning</name>
                <type>string</type>
                <description>Why we need to sample this table</description>
                <required>true</required>
            </parameter>
            <parameter>
                <name>table_name</name>
                <type>string</type>
                <description>Name of table to sample</description>
                <required>true</required>
            </parameter>
            <parameter>
                <name>row_sample_size</name>
                <type>integer</type>
                <description>Number of rows to sample aim for 3-5 rows</description>
                <required>true</required>
            </parameter>
        </parameters>
    </tool>

    <tool>
        <name>run_test_sql_query</name>
        <description>Tests a SQLite SQL query and returns results (only visible to agent)</description>
        <parameters>
            <parameter>
                <name>reasoning</name>
                <type>string</type>
                <description>Why we're testing this specific query</description>
                <required>true</required>
            </parameter>
            <parameter>
                <name>sql_query</name>
                <type>string</type>
                <description>The SQL query to test</description>
                <required>true</required>
            </parameter>
        </parameters>
    </tool>

    <tool>
        <name>run_final_sql_query</name>
        <description>Runs the final validated SQLite SQL query and shows results to user</description>
        <parameters>
            <parameter>
                <name>reasoning</name>
                <type>string</type>
                <description>Final explanation of how query satisfies user request</description>
                <required>true</required>
            </parameter>
            <parameter>
                <name>sql_query</name>
                <type>string</type>
                <description>The validated SQL query to run</description>
                <required>true</required>
            </parameter>
        </parameters>
    </tool>
</tools>

<user-request>
    {{user_request}}
</user-request>
"""

# Tool schemas passed to the Anthropic API
TOOLS = [
    {
        "name": "list_tables",
        "description": "Returns list of available tables in the SQLite database",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Why we need to list tables relative to user request",
                }
            },
            "required": ["reasoning"],
        },
    },
    {
        "name": "describe_table",
        "description": "Returns schema info for specified SQLite table",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Why we need to describe this table",
                },
                "table_name": {
                    "type": "string",
                    "description": "Name of table to describe",
                },
            },
            "required": ["reasoning", "table_name"],
        },
    },
    {
        "name": "sample_table",
        "description": "Returns sample rows from specified SQLite table",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Why we need to sample this table",
                },
                "table_name": {
                    "type": "string",
                    "description": "Name of table to sample",
                },
                "row_sample_size": {
                    "type": "integer",
                    "description": "Number of rows to sample aim for 3-5 rows",
                },
            },
            "required": ["reasoning", "table_name", "row_sample_size"],
        },
    },
    {
        "name": "run_test_sql_query",
        "description": "Tests a SQLite SQL query and returns results (only visible to agent)",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Why we're testing this specific query",
                },
                "sql_query": {
                    "type": "string",
                    "description": "The SQL query to test",
                },
            },
            "required": ["reasoning", "sql_query"],
        },
    },
    {
        "name": "run_final_sql_query",
        "description": "Runs the final validated SQLite SQL query and shows results to user",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Final explanation of how query satisfies user request",
                },
                "sql_query": {
                    "type": "string",
                    "description": "The validated SQL query to run",
                },
            },
            "required": ["reasoning", "sql_query"],
        },
    },
]


def _validate_table_name(table_name: str) -> None:
    """Reject table names that contain characters outside alphanumeric + underscore.

    SQLite table names cannot be safely parameterized in FROM clauses, so we
    validate the identifier manually before interpolating it into SQL.

    Args:
        table_name: The table name to validate.

    Raises:
        ValueError: If the table name contains unsafe characters.
    """
    if not re.fullmatch(r"[A-Za-z0-9_]+", table_name):
        raise ValueError(
            f"Invalid table name '{table_name}': only alphanumeric characters and "
            "underscores are allowed."
        )


def _format_rows(cursor: sqlite3.Cursor, rows: list) -> str:
    """Format cursor rows with column headers into a readable string.

    Args:
        cursor: The executed cursor (provides column descriptions).
        rows: The fetched rows.

    Returns:
        A formatted string with a header line and one row per line.
    """
    if cursor.description is None:
        return "(no results)"
    headers = [desc[0] for desc in cursor.description]
    lines = [" | ".join(headers)]
    lines.append("-" * len(lines[0]))
    for row in rows:
        lines.append(" | ".join(str(v) for v in row))
    return "\n".join(lines)


def list_tables(reasoning: str) -> List[str]:
    """Returns a list of tables in the SQLite database.

    The agent uses this to discover available tables and make informed decisions.

    Args:
        reasoning: Explanation of why we're listing tables relative to user request.

    Returns:
        List of table names as strings.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        console.log(f"[blue]List Tables Tool[/blue] - Reasoning: {reasoning}")
        return tables
    except Exception as e:
        console.log(f"[red]Error listing tables: {str(e)}[/red]")
        return []


def describe_table(reasoning: str, table_name: str) -> str:
    """Returns schema information about the specified SQLite table.

    The agent uses this to understand table structure and available columns.

    Args:
        reasoning: Explanation of why we're describing this table.
        table_name: Name of table to describe.

    Returns:
        String containing table schema information.
    """
    try:
        _validate_table_name(table_name)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            return f"Table '{table_name}' not found or has no columns."
        lines = ["cid | name | type | notnull | dflt_value | pk"]
        lines.append("-" * 50)
        for row in rows:
            lines.append(" | ".join(str(v) for v in row))
        result = "\n".join(lines)
        console.log(
            f"[blue]Describe Table Tool[/blue] - Table: {table_name} - Reasoning: {reasoning}"
        )
        return result
    except Exception as e:
        console.log(f"[red]Error describing table: {str(e)}[/red]")
        return str(e)


def sample_table(reasoning: str, table_name: str, row_sample_size: int) -> str:
    """Returns a sample of rows from the specified SQLite table.

    The agent uses this to understand actual data content and patterns.

    Args:
        reasoning: Explanation of why we're sampling this table.
        table_name: Name of table to sample from.
        row_sample_size: Number of rows to sample; aim for 3-5 rows.

    Returns:
        String containing sample rows in readable format.
    """
    try:
        _validate_table_name(table_name)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT ?", (row_sample_size,))
        rows = cursor.fetchall()
        result = _format_rows(cursor, rows)
        conn.close()
        console.log(
            f"[blue]Sample Table Tool[/blue] - Table: {table_name} - "
            f"Rows: {row_sample_size} - Reasoning: {reasoning}"
        )
        return result
    except Exception as e:
        console.log(f"[red]Error sampling table: {str(e)}[/red]")
        return str(e)


def run_test_sql_query(reasoning: str, sql_query: str) -> str:
    """Executes a test SQL query against the SQLite database and returns results.

    The agent uses this to validate queries before finalizing them.
    Results are only shown to the agent, not the user.

    Args:
        reasoning: Explanation of why we're running this test query.
        sql_query: The SQL query to test.

    Returns:
        Query results as a formatted string.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        result = _format_rows(cursor, rows)
        conn.close()
        console.log(f"[blue]Test Query Tool[/blue] - Reasoning: {reasoning}")
        console.log(f"[dim]Query: {sql_query}[/dim]")
        return result
    except Exception as e:
        console.log(f"[red]Error running test query: {str(e)}[/red]")
        return str(e)


def run_final_sql_query(reasoning: str, sql_query: str) -> str:
    """Executes the final SQL query against the SQLite database and shows results to user.

    This is the last tool call the agent should make after validating the query.

    Args:
        reasoning: Final explanation of how this query satisfies user request.
        sql_query: The validated SQL query to run.

    Returns:
        Query results as a formatted string.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        result = _format_rows(cursor, rows)
        conn.close()
        console.log(
            Panel(
                f"[green]Final Query Tool[/green]\nReasoning: {reasoning}\nQuery: {sql_query}"
            )
        )
        return result
    except Exception as e:
        console.log(f"[red]Error running final query: {str(e)}[/red]")
        return str(e)


def main() -> None:
    parser = argparse.ArgumentParser(description="SQLite Agent using Anthropic API")
    parser.add_argument(
        "-d", "--db", required=True, help="Path to SQLite database file"
    )
    parser.add_argument("-p", "--prompt", required=True, help="The user's request")
    parser.add_argument(
        "-c",
        "--compute",
        type=int,
        default=10,
        help="Maximum number of agent loops (default: 10)",
    )
    args = parser.parse_args()

    # Configure the API key
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        console.print(
            "[red]Error: ANTHROPIC_API_KEY environment variable is not set[/red]"
        )
        console.print("Please get your API key from your Anthropic dashboard")
        console.print("Then set it with: export ANTHROPIC_API_KEY='your-api-key-here'")
        sys.exit(1)

    # Set global DB_PATH for tool functions
    global DB_PATH
    DB_PATH = args.db

    client = Anthropic()

    completed_prompt = AGENT_PROMPT.replace("{{user_request}}", args.prompt)
    messages = [{"role": "user", "content": completed_prompt}]

    compute_iterations = 0
    break_loop = False
    thinking_block = None

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
                "[yellow]Warning: Reached maximum compute loops without final query[/yellow]"
            )
            raise Exception(
                f"Maximum compute loops reached: {compute_iterations}/{args.compute}"
            )

        try:
            response = client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=3000,
                messages=messages,  # type: ignore[arg-type]
                tools=TOOLS,  # type: ignore[arg-type]
                thinking={"type": "enabled", "budget_tokens": 1024},
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
                    console.print(
                        f"[cyan]Model response:[/cyan] {content_block.text}"
                    )

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
                    if tool_name == "list_tables":
                        result = list_tables(reasoning=tool_input["reasoning"])
                    elif tool_name == "describe_table":
                        result = describe_table(
                            reasoning=tool_input["reasoning"],
                            table_name=tool_input["table_name"],
                        )
                    elif tool_name == "sample_table":
                        result = sample_table(
                            reasoning=tool_input["reasoning"],
                            table_name=tool_input["table_name"],
                            row_sample_size=tool_input["row_sample_size"],
                        )
                    elif tool_name == "run_test_sql_query":
                        result = run_test_sql_query(
                            reasoning=tool_input["reasoning"],
                            sql_query=tool_input["sql_query"],
                        )
                    elif tool_name == "run_final_sql_query":
                        result = run_final_sql_query(
                            reasoning=tool_input["reasoning"],
                            sql_query=tool_input["sql_query"],
                        )
                        console.print("\n[green]Final Results:[/green]")
                        console.print(result)
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
                                    "content": str(error_msg),
                                }
                            ],
                        }
                    )

        except Exception as e:
            console.print(f"[red]Error in agent loop: {str(e)}[/red]")
            raise e


if __name__ == "__main__":
    main()
