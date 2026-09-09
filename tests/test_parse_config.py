"""Seam C: config parsing as a pure dict -> models function.

Separated from disk reads and module-global mutation, so a bad Config fails
predictably. Covers well-formed and malformed input.
"""

import pytest

from toolbox.data import ConfigDict, parse_config

WELL_FORMED: ConfigDict = {
    "toolsets": [
        {
            "name": "Production",
            "job": "shot_010",
            "tools": [
                {
                    "name": "Maya",
                    "version": "2025",
                    "desc": "Redshift",
                    "rez_wants": ["maya-2025", "redshift-2025.6"],
                    "command": "maya",
                    "icon": "maya_icon.png",
                }
            ],
        }
    ]
}


def test_parses_toolsets_and_tools() -> None:
    toolsets = parse_config(WELL_FORMED)
    assert len(toolsets) == 1
    toolset = toolsets[0]
    assert toolset.name == "Production"
    assert len(toolset.tools) == 1
    tool = toolset.tools[0]
    assert tool.name == "Maya"
    assert tool.version == "2025"
    assert tool.subtitle == "Redshift"
    assert tool.command == "maya"
    assert tool.icon == "maya_icon.png"
    assert tool.rez_wants == ["maya-2025", "redshift-2025.6"]


def test_empty_toolsets_yields_empty_list() -> None:
    assert parse_config({"toolsets": []}) == []


def test_missing_toolsets_key_raises() -> None:
    with pytest.raises(KeyError):
        # Deliberately malformed: proves a bad Config fails at the parse. The
        # empty dict violates ConfigDict on purpose, hence the targeted ignore.
        parse_config({})  # pyright: ignore[reportArgumentType]


def test_tool_missing_required_key_raises() -> None:
    malformed = {"toolsets": [{"name": "P", "tools": [{"name": "Maya"}]}]}
    with pytest.raises(KeyError):
        # Deliberately malformed input (missing Tool keys); the runtime KeyError
        # is the contract under test, so the static type mismatch is expected.
        parse_config(malformed)  # pyright: ignore[reportArgumentType]
