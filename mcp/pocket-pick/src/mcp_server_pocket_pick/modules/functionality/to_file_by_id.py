import logging
from pathlib import Path

from ..data_types import GetCommand, ToFileByIdCommand
from .get import get

logger = logging.getLogger(__name__)


def to_file_by_id(command: ToFileByIdCommand) -> bool:
    """Write a pocket pick item's content to a file by its ID."""
    try:
        get_command = GetCommand(id=command.id, db_path=command.db_path)
        item = get(get_command)

        if not item:
            logger.error(f"Item with ID {command.id} not found")
            return False

        output_path = Path(command.output_file_path_abs)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(item.text)

        return True
    except Exception as e:
        logger.error(
            f"Error writing to file {command.output_file_path_abs}: {e}"
        )
        return False
