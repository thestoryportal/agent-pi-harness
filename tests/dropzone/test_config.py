import pytest
import yaml

from apps.dropzone.config import (
    DropsConfig,
    DropZoneConfig,
    ensure_zone_dirs,
    load_drops_config,
)


def _write_yaml(tmp_path, data):
    p = tmp_path / "drops.yaml"
    with open(p, "w") as f:
        yaml.dump(data, f)
    return p


def _minimal_zone(**overrides):
    base = {
        "name": "Test Zone",
        "file_patterns": ["*.txt"],
        "reusable_prompt": "prompt.md",
        "zone_dirs": ["/tmp/zone"],
        "events": ["created"],
        "agent": "claude_code",
    }
    base.update(overrides)
    return base


def test_load_drops_config_valid(tmp_path):
    p = _write_yaml(tmp_path, {"drop_zones": [_minimal_zone()]})
    cfg = load_drops_config(p)
    assert len(cfg.drop_zones) == 1
    assert cfg.drop_zones[0].name == "Test Zone"
    assert cfg.drop_zones[0].agent == "claude_code"
    assert cfg.drop_zones[0].model == "sonnet"


def test_load_drops_config_missing_key(tmp_path):
    p = _write_yaml(tmp_path, {"zones": []})
    with pytest.raises(ValueError, match="drop_zones"):
        load_drops_config(p)


def test_load_drops_config_invalid_agent(tmp_path):
    p = _write_yaml(tmp_path, {"drop_zones": [_minimal_zone(agent="unknown_llm")]})
    with pytest.raises(ValueError, match="unknown_llm"):
        load_drops_config(p)


def test_load_drops_config_invalid_event(tmp_path):
    p = _write_yaml(tmp_path, {"drop_zones": [_minimal_zone(events=["exploded"])]})
    with pytest.raises(ValueError, match="exploded"):
        load_drops_config(p)


def test_load_drops_config_defaults(tmp_path):
    p = _write_yaml(tmp_path, {"drop_zones": [_minimal_zone()]})
    cfg = load_drops_config(p)
    zone = cfg.drop_zones[0]
    assert zone.model == "sonnet"
    assert zone.mcp_server_file is None
    assert zone.create_zone_dir_if_not_exists is True


def test_ensure_zone_dirs_creates_dirs(tmp_path):
    zone_dir = str(tmp_path / "myzone")
    cfg = DropsConfig(drop_zones=[
        DropZoneConfig(
            name="T", file_patterns=["*"], reusable_prompt="x",
            zone_dirs=[zone_dir], events=["created"], agent="claude_code",
            create_zone_dir_if_not_exists=True,
        )
    ])
    ensure_zone_dirs(cfg)
    assert (tmp_path / "myzone").is_dir()


def test_ensure_zone_dirs_skip_if_false(tmp_path):
    zone_dir = str(tmp_path / "skipzone")
    cfg = DropsConfig(drop_zones=[
        DropZoneConfig(
            name="T", file_patterns=["*"], reusable_prompt="x",
            zone_dirs=[zone_dir], events=["created"], agent="claude_code",
            create_zone_dir_if_not_exists=False,
        )
    ])
    ensure_zone_dirs(cfg)
    assert not (tmp_path / "skipzone").exists()
