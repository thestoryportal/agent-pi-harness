#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "anthropic>=0.47.1",
#   "rich>=13.7.0",
# ]
# ///

"""
Usage:
    uv run agents/sfa/sfa_meta_prompt_agent.py --purpose "generate mermaid diagrams" --instructions "generate a mermaid valid chart, use diagram type specified or default flow"
    uv run agents/sfa/sfa_meta_prompt_agent.py --purpose "generate mermaid diagrams" --instructions "generate valid charts" --sections "examples,user-prompt" --variables "user-prompt" --output prompt.md
"""

import os
import sys
import argparse
import json
import traceback
from rich.console import Console
from rich.panel import Panel
import anthropic

# Initialize global console
console = Console()

# Module-level output file path (set from args in main)
output_file: str | None = None

AGENT_PROMPT = """<purpose>
    You are an expert prompt engineer. Your goal is to generate comprehensive, structured prompts
    for language models using XML-tagged sections.
</purpose>

<instructions>
    <instruction>Generate a structured prompt with clear XML tags: purpose, instructions, examples (if requested), and variable placeholders.</instruction>
    <instruction>Use {{variable_name}} syntax for placeholder variables.</instruction>
    <instruction>Make the prompt specific, actionable, and well-organized.</instruction>
    <instruction>When complete, call generate_prompt with the full prompt text.</instruction>
    <instruction>Then call complete_task to finalize.</instruction>
</instructions>

<prompt-specification>
    Purpose: {{purpose}}
    Instructions: {{instructions}}
    Sections: {{sections}}
    Examples: {{examples}}
    Variables: {{variables}}
</prompt-specification>
"""


def tool_generate_prompt(tool_input: dict) -> dict:
    try:
        reasoning = tool_input.get("reasoning")
        prompt_text = tool_input.get("prompt_text")

        console.log(f"[tool_generate_prompt] reasoning: {reasoning}")

        if not prompt_text:
            error_message = "No prompt_text provided."
            console.log(f"[tool_generate_prompt] Error: {error_message}")
            return {"error": error_message}

        if output_file:
            dir_name = os.path.dirname(output_file)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(output_file, "w") as f:
                f.write(prompt_text)
            console.print(f"[green]Prompt written to {output_file}[/green]")
        else:
            console.print(Panel(prompt_text, title="Generated Prompt"))

        return {"result": "Prompt generated successfully"}
    except Exception as e:
        console.log(f"[tool_generate_prompt] Error: {str(e)}")
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
    global output_file

    parser = argparse.ArgumentParser(
        description="Meta-Prompt Generator Agent using Anthropic API"
    )
    parser.add_argument(
        "-u", "--purpose", required=True, help="Main goal of the prompt"
    )
    parser.add_argument(
        "-i", "--instructions", required=True, help="Detailed model instructions"
    )
    parser.add_argument(
        "-s",
        "--sections",
        default="",
        help="Comma-separated section names",
    )
    parser.add_argument(
        "-x",
        "--examples",
        default="",
        help="Description of examples to generate",
    )
    parser.add_argument(
        "-v",
        "--variables",
        default="",
        help="Comma-separated placeholder variable names",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file path. If not provided, prints to console.",
    )
    parser.add_argument(
        "-c",
        "--compute",
        type=int,
        default=5,
        help="Maximum compute loops (default: 5)",
    )
    args = parser.parse_args()

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    if not ANTHROPIC_API_KEY:
        console.print(
            "[red]Error: ANTHROPIC_API_KEY environment variable is not set.[/red]"
        )
        sys.exit(1)

    output_file = args.output

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Build initial message by substituting args into AGENT_PROMPT
    initial_message = (
        AGENT_PROMPT.replace("{{purpose}}", args.purpose)
        .replace("{{instructions}}", args.instructions)
        .replace("{{sections}}", args.sections)
        .replace("{{examples}}", args.examples)
        .replace("{{variables}}", args.variables)
    )
    messages = [{"role": "user", "content": initial_message}]

    tools = [
        {
            "name": "generate_prompt",
            "description": "Generate and output the structured prompt",
            "input_schema": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": "Why this prompt design was chosen",
                    },
                    "prompt_text": {
                        "type": "string",
                        "description": "The full generated prompt text",
                    },
                },
                "required": ["reasoning", "prompt_text"],
            },
        },
        {
            "name": "complete_task",
            "description": "Finalize the task and exit the agent loop",
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
        "generate_prompt": tool_generate_prompt,
        "complete_task": tool_complete_task,
    }

    compute_iterations = 0

    while compute_iterations < args.compute:
        compute_iterations += 1
        console.rule(
            f"[yellow]Agent Loop {compute_iterations}/{args.compute}[/yellow]"
        )
        try:
            response = client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=8000,
                thinking={"type": "enabled", "budget_tokens": 2048},
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
        else:
            # No tool calls — model finished without calling complete_task
            console.print(
                "[yellow]No tool calls in response. Exiting agent loop.[/yellow]"
            )
            break

    console.print("[yellow]Reached compute limit without completing task.[/yellow]")


if __name__ == "__main__":
    main()
