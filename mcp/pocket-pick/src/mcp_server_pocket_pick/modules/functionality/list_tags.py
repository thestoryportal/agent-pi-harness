import json
import logging

from ..data_types import ListTagsCommand
from ..init_db import init_db

logger = logging.getLogger(__name__)


def list_tags(command: ListTagsCommand) -> list[dict[str, int]]:
    """List all tags in the pocket pick database with their counts."""
    db = init_db(command.db_path)
    try:
        cursor = db.execute("SELECT tags FROM POCKET_PICK")
        tag_counts: dict[str, int] = {}
        for (tags_json,) in cursor.fetchall():
            tags = json.loads(tags_json)
            for tag in tags:
                if tag in tag_counts:
                    tag_counts[tag] += 1
                else:
                    tag_counts[tag] = 1

        sorted_tags = sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))
        return [
            {"tag": tag, "count": count}
            for tag, count in sorted_tags[: command.limit]
        ]
    except Exception as e:
        logger.error(f"Error listing tags: {e}")
        raise
    finally:
        db.close()
