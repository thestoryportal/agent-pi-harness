import json
import logging
import uuid
from datetime import datetime

from ..data_types import AddCommand, PocketItem
from ..init_db import init_db, normalize_tags

logger = logging.getLogger(__name__)


def add(command: AddCommand) -> PocketItem:
    """Add a new item to the pocket pick database."""
    normalized_tags = normalize_tags(command.tags)
    item_id = str(uuid.uuid4())
    timestamp = datetime.now()

    db = init_db(command.db_path)
    try:
        tags_json = json.dumps(normalized_tags)
        db.execute(
            "INSERT INTO POCKET_PICK (id, created, text, tags) VALUES (?, ?, ?, ?)",
            (item_id, timestamp.isoformat(), command.text, tags_json),
        )
        db.commit()
        return PocketItem(
            id=item_id, created=timestamp, text=command.text, tags=normalized_tags
        )
    except Exception as e:
        logger.error(f"Error adding item: {e}")
        raise
    finally:
        db.close()
