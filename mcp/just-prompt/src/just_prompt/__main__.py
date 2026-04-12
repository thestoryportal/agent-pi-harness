"""Entry point for just-prompt MCP server."""

import argparse
import os

from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="just-prompt MCP server")
    parser.add_argument(
        "--default-models",
        type=str,
        default="anthropic:claude-sonnet-4-20250514",
        help="Comma-separated list of default models (provider:model[:suffix])",
    )
    args = parser.parse_args()
    default_models = [m.strip() for m in args.default_models.split(",")]
    os.environ["JUST_PROMPT_DEFAULT_MODELS"] = ",".join(default_models)

    from just_prompt.server import create_server

    server = create_server(default_models=default_models)
    server.run()


if __name__ == "__main__":
    main()
