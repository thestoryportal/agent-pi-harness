import json
import logging
import re
import sqlite3
from datetime import datetime

from ..data_types import FindCommand, PocketItem
from ..init_db import init_db, normalize_tags

logger = logging.getLogger(__name__)


def find(command: FindCommand) -> list[PocketItem]:
    """Find items in the pocket pick database matching the search criteria."""
    normalized_tags = normalize_tags(command.tags) if command.tags else []

    db = init_db(command.db_path)
    try:
        query = "SELECT id, created, text, tags FROM POCKET_PICK"
        params: list[str] = []
        where_clauses: list[str] = []

        # Apply search mode
        if command.text:
            if command.mode == "substr":
                where_clauses.append("text LIKE ?")
                params.append(f"%{command.text}%")
            elif command.mode == "fts":
                try:
                    # Use FTS5 virtual table
                    query = """
                    SELECT POCKET_PICK.id, POCKET_PICK.created,
                           POCKET_PICK.text, POCKET_PICK.tags
                    FROM pocket_pick_fts
                    JOIN POCKET_PICK ON pocket_pick_fts.rowid = POCKET_PICK.rowid
                    """

                    # FTS5 query — quoted phrases, multi-word, or single word
                    search_term = command.text

                    where_clauses = ["pocket_pick_fts MATCH ?"]
                    params = [search_term]

                    # Add tag filter for FTS query
                    if normalized_tags:
                        tag_clauses = []
                        for tag in normalized_tags:
                            tag_clauses.append("POCKET_PICK.tags LIKE ?")
                            params.append(f'%"{tag}"%')
                        where_clauses.append(
                            f"({' AND '.join(tag_clauses)})"
                        )

                    use_fts5 = True
                except sqlite3.OperationalError:
                    logger.warning(
                        "FTS5 not available, falling back to basic search"
                    )
                    use_fts5 = False
                    search_words = command.text.split()
                    word_clauses = []
                    for word in search_words:
                        word_clauses.append("text LIKE ?")
                        params.append(f"%{word}%")
                    where_clauses.append(
                        f"({' AND '.join(word_clauses)})"
                    )
            elif command.mode == "glob":
                where_clauses.append("text GLOB ?")
                params.append(command.text)
            elif command.mode == "regex":
                # Regex filter applied after query
                pass
            elif command.mode == "exact":
                where_clauses.append("text = ?")
                params.append(command.text)

        # Apply tag filter (for non-FTS modes)
        if normalized_tags and not (
            command.mode == "fts"
            and "use_fts5" in locals()
            and use_fts5  # noqa: F821
        ):
            tag_clauses = []
            for tag in normalized_tags:
                tag_clauses.append("tags LIKE ?")
                params.append(f'%"{tag}"%')
            where_clauses.append(f"({' AND '.join(tag_clauses)})")

        # Build final query
        if (
            command.mode == "fts"
            and "use_fts5" in locals()
            and use_fts5  # noqa: F821
        ):
            if where_clauses:
                query += f" WHERE {' AND '.join(where_clauses)}"
            query += f" ORDER BY rank, created DESC LIMIT {command.limit}"
        else:
            if where_clauses:
                query += f" WHERE {' AND '.join(where_clauses)}"
            query += f" ORDER BY created DESC LIMIT {command.limit}"

        # Execute query with FTS5 fallback
        try:
            cursor = db.execute(query, params)
        except sqlite3.OperationalError as e:
            if (
                command.mode == "fts"
                and "use_fts5" in locals()
                and use_fts5  # noqa: F821
            ):
                logger.warning(
                    f"FTS5 query failed: {e}. Falling back to basic search."
                )
                query = "SELECT id, created, text, tags FROM POCKET_PICK"
                params = []

                if command.text:
                    search_words = command.text.split()
                    word_clauses = []
                    for word in search_words:
                        word_clauses.append("text LIKE ?")
                        params.append(f"%{word}%")
                    query += f" WHERE ({' AND '.join(word_clauses)})"

                    if normalized_tags:
                        tag_clauses = []
                        for tag in normalized_tags:
                            tag_clauses.append("tags LIKE ?")
                            params.append(f'%"{tag}"%')
                        query += f" AND ({' AND '.join(tag_clauses)})"

                query += f" ORDER BY created DESC LIMIT {command.limit}"
                cursor = db.execute(query, params)
            else:
                raise

        # Process results
        results = []
        for row in cursor.fetchall():
            id_, created_str, text, tags_json = row
            created = datetime.fromisoformat(created_str)
            tags = json.loads(tags_json)
            item = PocketItem(id=id_, created=created, text=text, tags=tags)

            # Apply regex filter post-query
            if command.mode == "regex" and command.text:
                try:
                    pattern = re.compile(command.text, re.IGNORECASE)
                    if not pattern.search(text):
                        continue
                except re.error:
                    logger.warning(f"Invalid regex pattern: {command.text}")
                    continue

            results.append(item)

        return results
    except Exception as e:
        logger.error(f"Error finding items: {e}")
        raise
    finally:
        db.close()
