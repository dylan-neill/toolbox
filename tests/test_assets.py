"""Seam D: bundled assets resolve via ``importlib.resources``.

Guards the packaging contract that ticket 05's installers rely on: a change that
hides the icons or the example Config would otherwise surface only for a user
launching an installer into missing icons and no default Config. Assert that a
known bundled asset resolves (an icon and the example Config) — nothing about how
they are loaded.
"""

import json
from pathlib import Path

from toolbox import resources


def test_icon_asset_resolves() -> None:
    path = Path(resources.icon_path("app_icon512.png"))
    assert path.is_file()


def test_settings_gear_icon_resolves() -> None:
    # The top-bar gear button (ticket 03) loads this bundled icon by name; a
    # packaging change that drops it should fail here, not at a blank button.
    path = Path(resources.icon_path("settings_icon.png"))
    assert path.is_file()


def test_example_config_asset_resolves() -> None:
    data = json.loads(resources.example_config_text())
    assert "toolsets" in data


def test_every_icon_named_in_example_config_resolves() -> None:
    # A packaging change that renames or drops an icon should fail here, not when
    # an artist opens the default Config and finds a blank tile.
    data = json.loads(resources.example_config_text())
    icons = {
        tool["icon"]
        for toolset in data["toolsets"]
        for tool in toolset["tools"]
    }
    assert icons, "example Config names no icons"
    missing = [name for name in icons if not Path(resources.icon_path(name)).is_file()]
    assert not missing, f"bundled icons missing: {missing}"
