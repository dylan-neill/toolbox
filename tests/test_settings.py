"""The Settings store: a pure ``settings_path`` plus tolerant load/save I/O.

Mirrors the ``config_path``/``load_config`` seam pattern — a pure resolver
(``settings_path``) unit-tested by injection, and thin I/O wrappers
(``load_settings``/``save_settings``) exercised against a temp dir. ``load_settings``
never raises to the caller: a missing or corrupt file yields ``{}`` so a fresh or
mangled install is all-defaults, not a crash.
"""

import json
import os
from pathlib import Path

import pytest

from toolbox import settings

SETTINGS = os.path.expanduser(os.path.join("~", ".config", "toolbox", "settings.json"))


@pytest.mark.parametrize("system", ["Windows", "Darwin", "Linux"])
def test_settings_path_is_dot_config_on_every_platform(system: str) -> None:
    # Fixed location on every platform (ADR 0003 / ADR 0006), beside config.json.
    assert settings.settings_path(system) == SETTINGS


def test_settings_path_unaffected_by_toolbox_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Unlike config_path, the Settings file never moves for TOOLBOX_CONFIG.
    monkeypatch.setenv("TOOLBOX_CONFIG", "/somewhere/else")
    assert settings.settings_path("Linux") == SETTINGS


def _point_settings_at(monkeypatch: pytest.MonkeyPatch, path: Path) -> None:
    def fixed_settings_path(system: str) -> str:
        return str(path)

    monkeypatch.setattr(settings, "settings_path", fixed_settings_path)


def test_load_settings_returns_empty_on_missing_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _point_settings_at(monkeypatch, tmp_path / "settings.json")
    assert settings.load_settings() == {}


def test_load_settings_returns_empty_on_corrupt_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "settings.json"
    target.write_text("{ not valid json", encoding="utf-8")
    _point_settings_at(monkeypatch, target)
    assert settings.load_settings() == {}


def test_load_settings_returns_empty_when_top_level_is_not_an_object(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A JSON array parses cleanly but is not a SettingsDict — treat as corrupt.
    target = tmp_path / "settings.json"
    target.write_text("[1, 2, 3]", encoding="utf-8")
    _point_settings_at(monkeypatch, target)
    assert settings.load_settings() == {}


def test_load_settings_reads_a_saved_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "settings.json"
    target.write_text(json.dumps({"config_path": "/x/config.json"}), encoding="utf-8")
    _point_settings_at(monkeypatch, target)
    assert settings.load_settings() == {"config_path": "/x/config.json"}


def test_save_settings_creates_dir_and_round_trips(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "nested" / "settings.json"  # parent dir does not exist yet
    _point_settings_at(monkeypatch, target)

    settings.save_settings({"config_path": "/x/config.json", "last_toolset": "Prod"})

    assert target.is_file()
    assert settings.load_settings() == {
        "config_path": "/x/config.json",
        "last_toolset": "Prod",
    }


def test_save_then_load_modify_write_preserves_other_keys(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The load-modify-write contract callers rely on: updating one key leaves the
    # others intact.
    _point_settings_at(monkeypatch, tmp_path / "settings.json")
    settings.save_settings({"config_path": "/x/config.json", "terminal_id": "iterm2"})

    current = settings.load_settings()
    current["last_toolset"] = "Staging"
    settings.save_settings(current)

    assert settings.load_settings() == {
        "config_path": "/x/config.json",
        "terminal_id": "iterm2",
        "last_toolset": "Staging",
    }
