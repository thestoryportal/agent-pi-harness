#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "anthropic>=0.47.1",
#   "rich>=13.7.0",
# ]
# ///

# Requires: jq CLI (brew install jq)

"""
Usage:
    uv run agents/sfa/sfa_jq_agent.py --exe "Filter scores above 80 from agents/sfa/data/analytics.json and save to high_scores.json"
    uv run agents/sfa/sfa_jq_agent.py --exe "Show all active users from agents/sfa/data/analytics.json"
"""

import os
import sys
import argparse
import json
import subprocess
import traceback
from rich.console import Console
import anthropic

# Initialize global console
console = Console()

AGENT_PROMPT = """<purpose>
    You are an expert at crafting precise jq commands for JSON processing.
    Your goal is to generate accurate jq commands that exactly match the user's data needs.
</purpose>

<instructions>
    <instruction>Use the provided tools to generate and test jq commands.</instruction>
    <instruction>First generate the jq command, then execute it to verify correctness.</instruction>
    <instruction>If the command fails, analyze the error and try a corrected command.</instruction>
    <instruction>When you have a working result, call complete_task to finalize.</instruction>
    <instruction>Provide reasoning with every tool call.</instruction>
</instructions>

<user-request>
    {{user_request}}
</user-request>
"""


def tool_generate_jq_command(tool_input: dict) -> dict:
    try:
        reasoning = tool_input.get("reasoning")
        jq_command = tool_input.get("jq_command")
        explanation = tool_input.get("explanation")

        console.log(
            f"[tool_generate_jq_command] reasoning: {reasoning}, jq_command: {jq_command}, explanation: {explanation}"
        )

        if not jq_command or not jq_command.strip():
            error_message = "No jq command provided: jq_command is empty."
            console.log(f"[tool_generate_jq_command] Error: {error_message}")
            return {"error": error_message}

        return {"result": jq_command}
    except Exception as e:
        console.log(f"[tool_generate_jq_command] Error: {str(e)}")
        console.log(traceback.format_exc())
        return {"error": str(e)}


def tool_execute_jq_command(tool_input: dict) -> dict:
    try:
        reasoning = tool_input.get("reasoning")
        jq_command = tool_input.get("jq_command")
        input_file = tool_input.get("input_file")

        console.log(
            f"[tool_execute_jq_command] reasoning: {reasoning}, jq_command: {jq_command}, input_file: {input_file}"
        )

        if not jq_command or not jq_command.strip():
            error_message = "No jq command provided: jq_command is empty."
            console.log(f"[tool_execute_jq_command] Error: {error_message}")
            return {"error": error_message}

        if not input_file or not input_file.strip():
            error_message = "No input file provided: input_file is empty."
            console.log(f"[tool_execute_jq_command] Error: {error_message}")
            return {"error": error_message}

        result = subprocess.run(
            ["jq", jq_command, input_file],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            error_message = result.stderr.strip() or "jq command failed with non-zero exit code."
            console.log(f"[tool_execute_jq_command] Error: {error_message}")
            return {"error": error_message}

        return {"result": result.stdout.strip()}
    except Exception as e:
        console.log(f"[tool_execute_jq_command] Error: {str(e)}")
        console.log(traceback.format_exc())
        return {"error": str(e)}


def tool_complete_task(tool_input: dict) -> dict:
    try:
        reasoning = tool_input.get("reasoning")

        if not reasoning:
            error_message = "No reasoning provided for task completion."
            console.log(f"[tool_complete_task] Error: {error_message}")
            return {"error": error_message}

        console.log(f"[tool_complete_task] reasoning: {reasoning}")
        return {"result": "Task completed"}
    except Exception as e:
        console.log(f"[tool_complete_task] Error: {str(e)}")
        console.log(traceback.format_exc())
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="JQ Agent using Anthropic API")
    parser.add_argument("-e", "--exe", required=True, help="The jq task description")
    parser.add_argument(
        "-c", "--compute", type=int, default=10, help="Maximum compute loops"
    )
    args = parser.parse_args()

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    if not ANTHROPIC_API_KEY:
        Console().print(
            "[red]Error: ANTHROPIC_API_KEY environment variable is not set.[/red]"
        )
        sys.exit(1)

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    initial_message = AGENT_PROMPT.replace("{{user_request}}", args.exe)
    messages = [{"role": "user", "content": initial_message}]

    compute_iterations = 0

    tools = [
        {
            "name": "generate_jq_command",
            "description": "Generate a jq command with explanation before executing it",
            "input_schema": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": "Why this jq command was chosen",
                    },
                    "jq_command": {
                        "type": "string",
                        "description": "The jq filter expression to use",
                    },
                    "explanation": {
                        "type": "string",
                        "description": "Human-readable explanation of what the command does",
                    },
                },
                "required": ["reasoning", "jq_command", "explanation"],
            },
        },
        {
            "name": "execute_jq_command",
            "description": "Execute a jq command against a JSON input file",
            "input_schema": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": "Why this command is being executed",
                    },
                    "jq_command": {
                        "type": "string",
                        "description": "The jq filter expression to run",
                    },
                    "input_file": {
                        "type": "string",
                        "description": "Path to the JSON input file",
                    },
                },
                "required": ["reasoning", "jq_command", "input_file"],
            },
        },
        {
            "name": "complete_task",
            "description": "Complete the task and exit the agent loop",
            "input_schema": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": "Why the task is complete",
                    }
                },
                "required": ["reasoning"],
            },
        },
    ]

    tool_functions = {
        "generate_jq_command": tool_generate_jq_command,
        "execute_jq_command": tool_execute_jq_command,
        "complete_task": tool_complete_task,
    }

    while compute_iterations < args.compute:
        compute_iterations += 1
        console.rule(f"[yellow]Agent Loop {compute_iterations}/{args.compute}[/yellow]")
        try:
            response = client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=3000,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 1024,
                },
                messages=messages,
                tools=tools,
            )
        except Exception as e:
            console.print(f"[red]Error in API call: {str(e)}[/red]")
            console.print(traceback.format_exc())
            break

        console.log("[green]API Response:[/green]", response.model_dump())

        tool_calls = [
            block
            for block in response.content
            if hasattr(block, "type") and block.type == "tool_use"
        ]

        if tool_calls:
            messages.append({"role": "assistant", "content": response.content})

            for tool in tool_calls:
                console.print(
                    f"[blue]Tool Call:[/blue] {tool.name}({json.dumps(tool.input)})"
                )
                func = tool_functions.get(tool.name)
                if func:
                    output = func(tool.input)
                    result_text = output.get("error") or output.get("result", "")
                    console.print(f"[green]Tool Result:[/green] {result_text}")

                    tool_result_message = {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool.id,
                                "content": result_text,
                            }
                        ],
                    }
                    messages.append(tool_result_message)

                    if tool.name == "complete_task":
                        console.print(
                            "[green]Task completed. Exiting agent loop.[/green]"
                        )
                        return
                else:
                    raise ValueError(f"Unknown tool: {tool.name}")

    console.print("[yellow]Reached compute limit without completing task.[/yellow]")


if __name__ == "__main__":
    main()
