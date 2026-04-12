"""YAML work item discovery — auto-discover tasks from YAML files.

Follows bowser ui-review.md Phase 1 pattern: glob discovery, parse array,
build flat list with source file tracking, skip unparseable files.

Key name: bowser uses 'stories' for its QA domain. This module uses 'items'
as the generic key, matching the Source of Truth O03 description. Callers
adapting bowser-format YAML should rename 'stories' → 'items' in their files.
"""

import sys
from pathlib import Path

import yaml


def discover_work_items(
    search_dir: Path,
    filename_filter: str | None = None,
) -> list[dict]:
    """Discover work items from YAML files under search_dir.

    Security: search_dir is not confined — callers must ensure it points
    within the project root. This function is internal to the orchestration
    layer and should not be exposed to untrusted input.

    For each *.yaml file (optionally filtered by filename_filter substring):
    - Parse the file
    - Extract the 'items' list
    - Attach 'source_file' (str of the yaml path) to each item
    - Skip files that fail to parse with a warning to stderr
    - Skip files with no 'items' key silently

    Returns flat list of item dicts, each with 'source_file' injected.
    """
    search_path = Path(search_dir)
    if not search_path.is_dir():
        return []

    yaml_files = sorted(search_path.glob("*.yaml"))

    if filename_filter:
        yaml_files = [f for f in yaml_files if filename_filter in f.name]

    result: list[dict] = []
    for f in yaml_files:
        try:
            data = yaml.safe_load(f.read_text())
        except Exception as e:
            print(f"WARNING: skipping {f}: {e}", file=sys.stderr)
            continue

        if not isinstance(data, dict):
            continue

        items = data.get("items")
        if not items or not isinstance(items, list):
            continue

        for item in items:
            if isinstance(item, dict):
                result.append({**item, "source_file": str(f)})

    return result
