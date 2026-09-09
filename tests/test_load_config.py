"""Integration: the residual load-Config glue (Seams B + C + D wired together).

Exercises the real filesystem path once in a temp dir: first launch seeds the
default Config from the bundled example, and a subsequent launch reads it back.
"""

import json
from pathlib import Path

import pytest

from toolbox import resources
from toolbox.data import parse_config


def test_first_launch_seeds_default_then_reads_it_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # TOOLBOX_CONFIG points at an existing directory, so the resolver targets
    # config.json inside it; on first launch that file does not exist yet.
    monkeypatch.setenv("TOOLBOX_CONFIG", str(tmp_path))

    result = resources.load_config()

    config_file = tmp_path / "config.json"
    assert config_file.is_file()
    assert "toolsets" in result
    # The seeded Config is the bundled example and parses into models.
    assert result == json.loads(resources.example_config_text())
    assert parse_config(result)  # non-empty toolsets


def test_second_launch_reads_existing_without_overwriting(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({"toolsets": []}), encoding="utf-8")
    monkeypatch.setenv("TOOLBOX_CONFIG", str(config_file))

    result = resources.load_config()

    assert result == {"toolsets": []}  # existing Config left untouched
