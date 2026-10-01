"""Live config reload from the top-bar refresh button (ticket 03, spec §5).

Headless GUI tests (offscreen Qt, like ``test_smoke``) covering
``ToolboxWindow.reload_config``: an external Config edit is reflected without a
restart; a read/parse error is caught and logged while the currently-loaded
toolsets stay on screen (the grid never blanks); and the selected toolset is
preserved by name across a reload, falling back to the first when it is gone.

The reload path runs through ``data.populate`` → ``resources.load_config``, so
each test injects a Config by monkeypatching ``resources.load_config`` and then
calls ``data.populate`` to seed the window's starting state.
"""

from typing import Any

import pytest
from pytestqt.qtbot import QtBot

from toolbox import data, resources
from toolbox.ui import ToolboxWindow


def _config(names: list[str]) -> dict[str, Any]:
    # A minimal well-formed Config: one toolset per name, each with a single
    # tool so the icon grid has something to (re)build.
    return {
        "toolsets": [
            {
                "name": name,
                "tools": [
                    {
                        "name": name,
                        "version": "1",
                        "desc": "",
                        "rez_wants": [],
                        "icon": "app_icon512.png",
                        "command": "run",
                    }
                ],
            }
            for name in names
        ]
    }


def _combo_items(window: ToolboxWindow) -> list[str]:
    return [
        window.toolsets_combo.itemText(i)
        for i in range(window.toolsets_combo.count())
    ]


def _window_with(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, names: list[str]
) -> ToolboxWindow:
    monkeypatch.setattr(resources, "load_config", lambda: _config(names))
    data.populate()
    window = ToolboxWindow()
    qtbot.addWidget(window)
    return window


def test_reload_reflects_an_external_edit(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    window = _window_with(qtbot, monkeypatch, ["Alpha", "Beta"])
    assert _combo_items(window) == ["Alpha", "Beta"]

    # Simulate an external edit adding a toolset, then refresh.
    monkeypatch.setattr(resources, "load_config", lambda: _config(["Alpha", "Beta", "Gamma"]))
    window.reload_config()

    assert _combo_items(window) == ["Alpha", "Beta", "Gamma"]


def test_reload_with_parse_error_keeps_current_toolsets_and_logs(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    window = _window_with(qtbot, monkeypatch, ["Alpha", "Beta"])

    # A malformed Config: parse_config raises KeyError on the missing "name".
    def malformed() -> dict[str, Any]:
        return {"toolsets": [{"tools": []}]}

    monkeypatch.setattr(resources, "load_config", malformed)
    window.reload_config()

    # Grid never blanks — the previously loaded toolsets stay on screen.
    assert _combo_items(window) == ["Alpha", "Beta"]
    assert "reload failed" in window.log_text_box.toPlainText().lower()


def test_reload_with_wrong_typed_config_keeps_current_toolsets_and_logs(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    window = _window_with(qtbot, monkeypatch, ["Alpha", "Beta"])

    # A well-formed-JSON but wrong-typed Config: a toolset that is a string, not
    # an object. parse_config indexes it and raises TypeError, not KeyError — the
    # "never crashes" contract must still hold.
    def wrong_type() -> dict[str, Any]:
        return {"toolsets": ["not-an-object"]}

    monkeypatch.setattr(resources, "load_config", wrong_type)
    window.reload_config()

    assert _combo_items(window) == ["Alpha", "Beta"]
    assert "reload failed" in window.log_text_box.toPlainText().lower()


def test_reload_with_read_error_keeps_current_toolsets_and_logs(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    window = _window_with(qtbot, monkeypatch, ["Alpha", "Beta"])

    def boom() -> dict[str, Any]:
        raise OSError("config file vanished")

    monkeypatch.setattr(resources, "load_config", boom)
    window.reload_config()

    assert _combo_items(window) == ["Alpha", "Beta"]
    assert "reload failed" in window.log_text_box.toPlainText().lower()


def test_reload_preserves_selected_toolset_by_name(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    window = _window_with(qtbot, monkeypatch, ["Alpha", "Beta", "Gamma"])
    window.toolsets_combo.setCurrentIndex(2)  # Gamma
    assert window.toolsets_combo.currentText() == "Gamma"

    # Reorder the toolsets on reload; the selection must follow the name, not
    # the index.
    monkeypatch.setattr(resources, "load_config", lambda: _config(["Gamma", "Alpha", "Beta"]))
    window.reload_config()

    assert window.toolsets_combo.currentText() == "Gamma"


def test_reload_falls_back_to_first_when_selection_gone(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    window = _window_with(qtbot, monkeypatch, ["Alpha", "Beta", "Gamma"])
    window.toolsets_combo.setCurrentIndex(2)  # Gamma

    # Gamma no longer exists after the edit — selection falls back to index 0.
    monkeypatch.setattr(resources, "load_config", lambda: _config(["Alpha", "Beta"]))
    window.reload_config()

    assert window.toolsets_combo.currentIndex() == 0
    assert window.toolsets_combo.currentText() == "Alpha"
