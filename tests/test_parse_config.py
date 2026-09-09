"""Seam C: config parsing as a pure dict -> models function.

Separated from disk reads and module-global mutation, so a bad Config fails
predictably. Covers well-formed and malformed input.
"""

import pytest

from toolbox.data import parse_config

WELL_FORMED = {
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


def test_parses_toolsets_and_tools():
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


def test_empty_toolsets_yields_empty_list():
    assert parse_config({"toolsets": []}) == []


def test_missing_toolsets_key_raises():
    with pytest.raises(KeyError):
        parse_config({})


def test_tool_missing_required_key_raises():
    malformed = {"toolsets": [{"name": "P", "tools": [{"name": "Maya"}]}]}
    with pytest.raises(KeyError):
        parse_config(malformed)
