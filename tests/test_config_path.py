"""Seam B: config-path resolution as a pure function of (platform, environment).

Covers every branch the spec calls out — Windows, macOS, Linux, a
``TOOLBOX_CONFIG`` file, and a ``TOOLBOX_CONFIG`` directory — with the platform
and environment injected rather than mocked at the OS level.
"""

import os
from pathlib import Path

import pytest

from toolbox import resources

DEFAULT = os.path.expanduser(os.path.join("~", ".config", "toolbox", "config.json"))


@pytest.mark.parametrize("system", ["Windows", "Darwin", "Linux"])
def test_default_path_is_dot_config_on_every_platform(system: str) -> None:
    # ADR 0003: all platforms deliberately share ~/.config/toolbox/. macOS
    # (Darwin) used to fall through to None here and crash on launch.
    assert resources.config_path(system, {}) == DEFAULT


def test_toolbox_config_file_overrides(tmp_path: Path) -> None:
    target = tmp_path / "my_config.json"  # a file path, not a directory
    assert resources.config_path("Linux", {"TOOLBOX_CONFIG": str(target)}) == str(target)


def test_toolbox_config_directory_gets_config_json_appended(tmp_path: Path) -> None:
    # tmp_path exists as a real directory, so the resolver appends config.json.
    assert resources.config_path("Darwin", {"TOOLBOX_CONFIG": str(tmp_path)}) == str(
        tmp_path / "config.json"
    )


def test_toolbox_config_expands_user(tmp_path: Path) -> None:
    # A ~ in the override is expanded like any other path.
    result = resources.config_path("Windows", {"TOOLBOX_CONFIG": "~/some_config.json"})
    assert result == os.path.expanduser("~/some_config.json")
