from __future__ import annotations

import json
from pathlib import Path

from toolbox.services.config_store import JsonConfigStore
from toolbox.services.tool_repository import InMemoryToolRepository


def write_default_config(app_path: Path) -> dict:
    data = {
        "toolsets": [
            {
                "name": "Production",
                "apps": [
                    {
                        "app": "Blender",
                        "version": "2.81",
                        "desc": "",
                        "tools": ["blender-2.81", "dnvfx"],
                        "command": "blender",
                        "icon": "blender_icon.png",
                    }
                ],
            }
        ]
    }
    resources_dir = app_path / "resources"
    resources_dir.mkdir(parents=True, exist_ok=True)
    (resources_dir / "default_config.json").write_text(json.dumps(data), encoding="utf-8")
    return data


def test_config_bootstrap_creates_config_from_default(tmp_path, monkeypatch):
    app_path = tmp_path / "app"
    expected = write_default_config(app_path)
    config_file = tmp_path / "config.json"
    monkeypatch.setenv("TOOLBOX_CONFIG", str(config_file))

    store = JsonConfigStore(app_path=app_path)
    loaded = store.load()

    assert config_file.is_file()
    assert loaded == expected
    assert store.path() == str(config_file)


def test_config_persistence_updates_tools_only(tmp_path, monkeypatch):
    app_path = tmp_path / "app"
    write_default_config(app_path)
    config_file = tmp_path / "config.json"
    monkeypatch.setenv("TOOLBOX_CONFIG", str(config_file))

    store = JsonConfigStore(app_path=app_path)
    repo = InMemoryToolRepository(store)
    toolsets = repo.load_toolsets()
    tool = toolsets[0].tools[0]

    ok, err = repo.update_tool_packages(tool.tool_id, ["blender-2.82", "dnvfx"])
    assert ok is True
    assert err is None

    payload = json.loads(config_file.read_text(encoding="utf-8"))
    app_entry = payload["toolsets"][0]["apps"][0]
    assert app_entry["app"] == "Blender"
    assert app_entry["tools"] == ["blender-2.82", "dnvfx"]


def test_repository_parse_default_config_counts(monkeypatch, tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    app_path = repo_root
    config_file = tmp_path / "config.json"
    monkeypatch.setenv("TOOLBOX_CONFIG", str(config_file))

    store = JsonConfigStore(app_path=app_path)
    repo = InMemoryToolRepository(store)
    toolsets = repo.load_toolsets()

    source = json.loads(
        (repo_root / "resources" / "default_config.json").read_text(encoding="utf-8")
    )
    expected_toolsets = len(source["toolsets"])
    expected_apps = sum(len(toolset["apps"]) for toolset in source["toolsets"])

    assert len(toolsets) == expected_toolsets
    assert sum(len(toolset.tools) for toolset in toolsets) == expected_apps
