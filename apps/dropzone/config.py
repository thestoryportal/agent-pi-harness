"""Drop zone configuration — YAML schema and loader."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml


VALID_AGENTS = {"claude_code", "gemini_cli", "codex_cli"}
VALID_EVENTS = {"created", "modified", "deleted", "moved"}


@dataclass
class DropZoneConfig:
    name: str
    file_patterns: list[str]
    reusable_prompt: str
    zone_dirs: list[str]
    events: list[str]
    agent: str
    model: str = "sonnet"
    mcp_server_file: str | None = None
    create_zone_dir_if_not_exists: bool = True
    skip_permissions: bool = False


@dataclass
class DropsConfig:
    drop_zones: list[DropZoneConfig] = field(default_factory=list)


def load_drops_config(path: Path) -> DropsConfig:
    """Load and validate drops.yaml configuration."""
    with open(path) as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or "drop_zones" not in data:
        raise ValueError(f"drops config must contain 'drop_zones' key: {path}")

    zones = []
    for i, entry in enumerate(data["drop_zones"]):
        agent = entry.get("agent", "")
        if agent not in VALID_AGENTS:
            raise ValueError(
                f"drop_zones[{i}].agent must be one of {VALID_AGENTS}, got '{agent}'"
            )

        events = entry.get("events", [])
        invalid = set(events) - VALID_EVENTS
        if invalid:
            raise ValueError(
                f"drop_zones[{i}].events contains invalid values {invalid}, "
                f"valid: {VALID_EVENTS}"
            )

        zones.append(DropZoneConfig(
            name=entry["name"],
            file_patterns=entry["file_patterns"],
            reusable_prompt=entry["reusable_prompt"],
            zone_dirs=entry["zone_dirs"],
            events=events,
            agent=agent,
            model=entry.get("model", "sonnet"),
            mcp_server_file=entry.get("mcp_server_file"),
            create_zone_dir_if_not_exists=entry.get(
                "create_zone_dir_if_not_exists", True
            ),
            skip_permissions=entry.get("skip_permissions", False),
        ))

    return DropsConfig(drop_zones=zones)


def ensure_zone_dirs(config: DropsConfig) -> None:
    """Create zone directories that don't exist when flag is set."""
    for zone in config.drop_zones:
        if zone.create_zone_dir_if_not_exists:
            for zone_dir in zone.zone_dirs:
                Path(zone_dir).mkdir(parents=True, exist_ok=True)
