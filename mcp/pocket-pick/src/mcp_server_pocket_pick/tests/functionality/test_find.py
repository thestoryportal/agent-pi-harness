import os
import tempfile
from pathlib import Path

import pytest

from ...modules.data_types import AddCommand, FindCommand
from ...modules.functionality.add import add
from ...modules.functionality.find import find


@pytest.fixture
def temp_db_path():
    # Create a temporary file path
    fd, path = tempfile.mkstemp()
    os.close(fd)

    # Return the path as a Path object
    yield Path(path)

    # Clean up the temp file after test
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def populated_db(temp_db_path):
    # Create sample items
    items = [
        {"text": "Python programming is fun", "tags": ["python", "programming", "fun"]},
        {"text": "SQL databases are powerful", "tags": ["sql", "database", "programming"]},
        {"text": "Testing code is important", "tags": ["testing", "code", "programming"]},
        {
            "text": "Regular expressions can be complex",
            "tags": ["regex", "programming", "advanced"],
        },
        {
            "text": "Learning new technologies is exciting",
            "tags": ["learning", "technology", "fun"],
        },
    ]

    # Add items to the database
    for item in items:
        command = AddCommand(
            text=item["text"],
            tags=item["tags"],
            db_path=temp_db_path,
        )
        add(command)

    return temp_db_path


def test_find_substr(populated_db):
    # Search using substring mode
    command = FindCommand(
        text="Python",
        mode="substr",
        limit=10,
        db_path=populated_db,
    )

    results = find(command)

    # Should find the Python item
    assert len(results) == 1
    assert results[0].text == "Python programming is fun"


def test_find_fts(populated_db):
    # Search using FTS mode
    command = FindCommand(
        text="programming",
        mode="fts",
        limit=10,
        db_path=populated_db,
    )

    results = find(command)

    # Should find items with "programming" in the text
    texts = [r.text for r in results]
    assert "Python programming is fun" in texts


def test_find_glob(populated_db):
    # Search using glob mode
    command = FindCommand(
        text="*databases*",
        mode="glob",
        limit=10,
        db_path=populated_db,
    )

    results = find(command)

    # Should find the SQL item
    assert len(results) == 1
    assert results[0].text == "SQL databases are powerful"


def test_find_regex(populated_db):
    # Search using regex mode
    command = FindCommand(
        text=r"^Python",
        mode="regex",
        limit=10,
        db_path=populated_db,
    )

    results = find(command)

    # Should find the Python item
    assert len(results) == 1
    assert results[0].text == "Python programming is fun"


def test_find_exact(populated_db):
    # Search using exact mode
    command = FindCommand(
        text="Testing code is important",
        mode="exact",
        limit=10,
        db_path=populated_db,
    )

    results = find(command)

    # Should find the exact item
    assert len(results) == 1
    assert results[0].text == "Testing code is important"


def test_find_with_tag_filter(populated_db):
    # Search with tag filter
    command = FindCommand(
        text="is",
        mode="substr",
        tags=["fun"],
        limit=10,
        db_path=populated_db,
    )

    results = find(command)

    # Should only return items that have the "fun" tag and contain "is"
    for result in results:
        assert "fun" in result.tags

    texts = [r.text for r in results]
    assert "Python programming is fun" in texts
    # "Learning new technologies is exciting" has "fun" tag and contains "is"
    assert "Learning new technologies is exciting" in texts
    # "Testing code is important" has "programming" not "fun"
    assert "Testing code is important" not in texts
