import json
import logging
from datetime import datetime

from ..data_types import ListCommand, PocketItem
from ..init_db import init_db, normalize_tags

logger = logging.getLogger(__name__)


def list_items(command: ListCommand) -> list[PocketItem]:
    """List items in the pocket pick database, optionally filtered by tags."""
    normalized_tags = normalize_tags(command.tags) if command.tags else []

    db = init_db(command.db_path)
    try:
        query = "SELECT id, created, text, tags FROM POCKET_PICK"
        params: list[str] = []

        if normalized_tags:
            tag_clauses = []
            for tag in normalized_tags:
                tag_clauses.append("tags LIKE ?")
                params.append(f'%"{tag}"%')
            query += f" WHERE {' AND '.join(tag_clauses)}"

        query += f" ORDER BY created DESC LIMIT {command.limit}"

        cursor = db.execute(query, params)
        results = []
        for row in cursor.fetchall():
            id_, created_str, text, tags_json = row
            created = datetime.fromisoformat(created_str)
            tags = json.loads(tags_json)
            results.append(
                PocketItem(id=id_, created=created, text=text, tags=tags)
            )
        return results
    except Exception as e:
        logger.error(f"Error listing items: {e}")
        raise
    finally:
        db.close()
