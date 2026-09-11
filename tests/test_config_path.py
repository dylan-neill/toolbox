"""Seam B: config-path resolution as a pure function of (platform, environment,
saved setting).

Covers the full precedence the spec calls out — ``TOOLBOX_CONFIG`` (file or dir)
› ``settings.json`` ``config_path`` (file only) › the default — with the platform,
environment, and setting injected rather than mocked at the OS level.
"""

import os
from pathlib import Path

import pytest

from toolbox import resources

DEFAULT = os.path.expanduser(os.path.join("~", ".config", "toolbox", "config.json"))


@pytest.mark.parametrize("system", ["Windows", "Darwin", "Linux"])
def test_default_path_is_dot_config_on_every_platform(system: str) -> None:
    # ADR 0003: all platforms deliberately share ~/.config/toolbox/. macOS
    # (Darwin) used to fall through to None here and crash on launch. No env
    # override and no saved setting → the default.
    assert resources.config_path(system, {}, None) == DEFAULT


def test_toolbox_config_file_overrides(tmp_path: Path) -> None:
    target = tmp_path / "my_config.json"  # a file path, not a directory
    assert resources.config_path("Linux", {"TOOLBOX_CONFIG": str(target)}, None) == str(
        target
    )


def test_toolbox_config_directory_gets_config_json_appended(tmp_path: Path) -> None:
    # tmp_path exists as a real directory, so the resolver appends config.json.
    assert resources.config_path(
        "Darwin", {"TOOLBOX_CONFIG": str(tmp_path)}, None
    ) == str(tmp_path / "config.json")


def test_toolbox_config_expands_user(tmp_path: Path) -> None:
    # A ~ in the override is expanded like any other path.
    result = resources.config_path(
        "Windows", {"TOOLBOX_CONFIG": "~/some_config.json"}, None
    )
    assert result == os.path.expanduser("~/some_config.json")


def test_setting_config_path_selects_config_when_no_env_override() -> None:
    # With no TOOLBOX_CONFIG, a saved config_path setting picks the Config file.
    result = resources.config_path("Linux", {}, "/srv/toolbox/prod_config.json")
    assert result == "/srv/toolbox/prod_config.json"


def test_setting_config_path_expands_user() -> None:
    # The saved path is user-expanded like the env override is.
    result = resources.config_path("Darwin", {}, "~/configs/toolbox.json")
    assert result == os.path.expanduser("~/configs/toolbox.json")


def test_setting_config_path_is_treated_as_a_file_not_a_directory(
    tmp_path: Path,
) -> None:
    # "File only": even when the saved path is an existing directory, the setting
    # is used verbatim (no config.json appended). Only TOOLBOX_CONFIG does the
    # directory dance.
    result = resources.config_path("Linux", {}, str(tmp_path))
    assert result == str(tmp_path)


def test_env_override_wins_over_setting(tmp_path: Path) -> None:
    # Precedence: TOOLBOX_CONFIG beats a saved config_path.
    env_target = tmp_path / "env_config.json"
    result = resources.config_path(
        "Linux", {"TOOLBOX_CONFIG": str(env_target)}, "/ignored/setting.json"
    )
    assert result == str(env_target)


# --- resolve_config_file: the gone/invalid fallback (Seam B, filesystem probe
# injected so the decision stays pure and testable) ---


def _all_missing(path: str) -> bool:
    return False  # nothing on disk


def _all_present(path: str) -> bool:
    return True  # everything on disk


def test_resolve_uses_setting_when_the_saved_config_exists() -> None:
    path, message = resources.resolve_config_file(
        "Linux", {}, "/srv/prod_config.json", _all_present
    )
    assert path == "/srv/prod_config.json"
    assert message is None  # happy path: no fallback, no message


def test_resolve_falls_back_to_default_when_saved_config_is_gone() -> None:
    path, message = resources.resolve_config_file(
        "Linux", {}, "/srv/prod_config.json", _all_missing
    )
    assert path == DEFAULT  # fell back to the default Config
    assert message is not None
    assert "/srv/prod_config.json" in message  # names the missing path
    assert DEFAULT in message  # names where it fell back to


def test_resolve_does_not_validate_a_toolbox_config_override(tmp_path: Path) -> None:
    # A TOOLBOX_CONFIG dir may legitimately not exist yet (first launch seeds it),
    # so the override is used verbatim with no fallback even when "missing".
    env_target = tmp_path / "env_config.json"
    path, message = resources.resolve_config_file(
        "Linux", {"TOOLBOX_CONFIG": str(env_target)}, "/srv/setting.json", _all_missing
    )
    assert path == str(env_target)
    assert message is None


def test_resolve_default_path_is_not_validated() -> None:
    # No setting and no override → the default, which load_config seeds if absent;
    # no fallback message even when it does not exist yet.
    path, message = resources.resolve_config_file("Linux", {}, None, _all_missing)
    assert path == DEFAULT
    assert message is None
