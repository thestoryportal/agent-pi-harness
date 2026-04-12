import asyncio
import logging
import sys
from pathlib import Path

import click

from .server import serve


@click.command()
@click.option(
    "--database",
    "-d",
    type=Path,
    help="SQLite database path (default: ~/.pocket_pick.db)",
)
@click.option("-v", "--verbose", count=True)
def main(database: Path | None, verbose: int) -> None:
    """Pocket Pick - Your Personal Knowledge Base"""
    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)
    asyncio.run(serve(database))


if __name__ == "__main__":
    main()
