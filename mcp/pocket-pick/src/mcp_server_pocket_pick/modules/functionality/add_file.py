import json
import logging
import uuid
from datetime import datetime
from pathlib import Path

from ..data_types import AddFileCommand, PocketItem
from ..init_db import init_db, normalize_tags

logger = logging.getLogger(__name__)


def add_file(command: AddFileCommand) -> PocketItem:
    """Add a new item to the pocket pick database from a file."""
    try:
        file_path = Path(command.file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        logger.error(f"Error reading file {command.file_path}: {e}")
        raise

    normalized_tags = normalize_tags(command.tags)
    item_id = str(uuid.uuid4())
    timestamp = datetime.now()

    db = init_db(command.db_path)
    try:
        tags_json = json.dumps(normalized_tags)
        db.execute(
            "INSERT INTO POCKET_PICK (id, created, text, tags) VALUES (?, ?, ?, ?)",
            (item_id, timestamp.isoformat(), text, tags_json),
        )
        db.commit()
        return PocketItem(
            id=item_id, created=timestamp, text=text, tags=normalized_tags
        )
    except Exception as e:
        logger.error(f"Error adding item from file: {e}")
        raise
    finally:
        db.close()
