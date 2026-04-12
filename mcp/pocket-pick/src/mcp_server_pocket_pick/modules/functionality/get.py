import json
import logging
from datetime import datetime

from ..data_types import GetCommand, PocketItem
from ..init_db import init_db

logger = logging.getLogger(__name__)


def get(command: GetCommand) -> PocketItem | None:
    """Get an item from the pocket pick database by ID."""
    db = init_db(command.db_path)
    try:
        cursor = db.execute(
            "SELECT id, created, text, tags FROM POCKET_PICK WHERE id = ?",
            (command.id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None

        id_, created_str, text, tags_json = row
        created = datetime.fromisoformat(created_str)
        tags = json.loads(tags_json)
        return PocketItem(id=id_, created=created, text=text, tags=tags)
    except Exception as e:
        logger.error(f"Error getting item {command.id}: {e}")
        raise
    finally:
        db.close()
