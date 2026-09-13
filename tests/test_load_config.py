"""Integration: the residual load-Config glue (Seams B + C + D wired together).

Exercises the real filesystem path once in a temp dir: first launch seeds the
default Config from the bundled example, and a subsequent launch reads it back.
"""

import json
from collections.abc import Mapping
from pathlib import Path

import pytest

from toolbox import resources, settings
from toolbox.data import parse_config
from toolbox.settings import SettingsDict


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


def test_saved_config_path_setting_selects_the_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # With no TOOLBOX_CONFIG, a saved config_path setting picks the Config file —
    # the "no env var needed" win, wired end to end (settings → resolve → read).
    monkeypatch.delenv("TOOLBOX_CONFIG", raising=False)
    saved_config = tmp_path / "prod_config.json"
    saved_config.write_text(json.dumps({"toolsets": []}), encoding="utf-8")

    def fake_load_settings() -> SettingsDict:
        return {"config_path": str(saved_config)}

    monkeypatch.setattr(settings, "load_settings", fake_load_settings)

    assert resources.load_config() == {"toolsets": []}


def test_gone_config_path_setting_falls_back_to_default_without_crashing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # A saved config_path that no longer exists must not crash: load_config falls
    # back to the default Config, surfaces a message, and leaves the setting
    # untouched. The default is redirected under tmp_path (patching the resolver's
    # None-branch) so the test never touches the real ~/.config.
    gone = tmp_path / "gone" / "prod_config.json"
    saved: list[SettingsDict] = []

    def fake_load_settings() -> SettingsDict:
        return {"config_path": str(gone)}

    def record_save(settings_dict: SettingsDict) -> None:
        saved.append(settings_dict)

    monkeypatch.setattr(settings, "load_settings", fake_load_settings)
    monkeypatch.setattr(settings, "save_settings", record_save)
    monkeypatch.delenv("TOOLBOX_CONFIG", raising=False)

    fallback_default = tmp_path / "default" / "config.json"
    real_config_path = resources.config_path

    def redirected_config_path(
        system: str, environ: Mapping[str, str], setting_config_path: str | None
    ) -> str:
        # The default (setting_config_path=None) branch points under tmp_path.
        if not environ.get("TOOLBOX_CONFIG") and not setting_config_path:
            return str(fallback_default)
        return real_config_path(system, environ, setting_config_path)

    monkeypatch.setattr(resources, "config_path", redirected_config_path)

    result = resources.load_config()  # must not raise

    assert "toolsets" in result  # fell back and seeded the default from the example
    assert fallback_default.is_file()
    assert str(gone) in capsys.readouterr().out  # message names the missing path
    assert saved == []  # the setting was never rewritten/wiped
