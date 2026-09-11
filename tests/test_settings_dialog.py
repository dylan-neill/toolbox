"""The Settings dialog (ticket 04, spec §4).

Headless GUI tests (offscreen Qt, like ``test_smoke``/``test_reload``) covering
``SettingsDialog``: the Config-file row (current path, Browse, Clear, the
``TOOLBOX_CONFIG`` override note), the Open Shell terminal row (the OS's
predefined terminals + Custom, with the Custom program/arguments fields), and
the OK/Cancel save contract (load-modify-write of ``config_path`` /
``terminal_id`` / ``terminal_command``, ``config_path_changed`` for the caller's
live reload, and no writes on Cancel).

The dialog reads and writes the store through ``settings.load_settings`` /
``settings.save_settings``, so each test monkeypatches those rather than touching
the real ``~/.config/toolbox/settings.json``. ``system`` and ``environ`` are
injected so the terminal registry and the override note are deterministic off the
host OS.
"""

from typing import Any

import pytest
from PySide6 import QtWidgets
from pytestqt.qtbot import QtBot

from toolbox import settings, terminals
from toolbox.ui import SettingsDialog


def _capture_saves(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    """Redirect ``save_settings`` to a list, returning the captured payloads."""
    saved: list[dict[str, Any]] = []

    def _record(data: Any) -> None:
        saved.append(dict(data))

    monkeypatch.setattr(settings, "save_settings", _record)
    return saved


def _stub_store(monkeypatch: pytest.MonkeyPatch, store: dict[str, Any]) -> None:
    """Make ``load_settings`` return a fresh copy of ``store`` on every call."""
    monkeypatch.setattr(settings, "load_settings", lambda: dict(store))


def _dialog(
    qtbot: QtBot,
    *,
    system: str = "Darwin",
    environ: dict[str, str] | None = None,
) -> SettingsDialog:
    dialog = SettingsDialog(system=system, environ=environ or {})
    qtbot.addWidget(dialog)
    return dialog


def _combo_ids(dialog: SettingsDialog) -> list[str]:
    return [
        dialog.terminal_combo.itemData(i)
        for i in range(dialog.terminal_combo.count())
    ]


def test_terminal_combo_lists_os_terminals_plus_custom(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {})
    dialog = _dialog(qtbot, system="Darwin")

    # The macOS registry order followed by the Custom entry.
    expected = list(terminals.registry_for("Darwin").keys()) + [
        terminals.CUSTOM_TERMINAL_ID
    ]
    assert _combo_ids(dialog) == expected


def test_terminal_combo_selects_stored_id(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {"terminal_id": "iterm2"})
    dialog = _dialog(qtbot, system="Darwin")

    assert dialog.terminal_combo.currentData() == "iterm2"


def test_terminal_combo_defaults_to_os_default_when_unset(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {})
    dialog = _dialog(qtbot, system="Darwin")

    assert dialog.terminal_combo.currentData() == terminals.default_terminal_id("Darwin")


def test_terminal_combo_falls_back_to_default_on_stale_id(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A stored id from another OS (or a removed terminal) is not in this OS's
    # registry — it falls back to the OS default, not blindly to index 0.
    _stub_store(monkeypatch, {"terminal_id": "konsole"})  # a Linux id on macOS
    dialog = _dialog(qtbot, system="Darwin")

    assert dialog.terminal_combo.currentData() == terminals.default_terminal_id("Darwin")


def test_config_field_shows_saved_path(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {"config_path": "/abs/custom.json"})
    dialog = _dialog(qtbot)

    assert dialog.config_path_field.text() == "/abs/custom.json"


def test_config_field_shows_default_when_unset(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {})
    dialog = _dialog(qtbot)

    # Unset → the default config location (not blank), so the user sees what is
    # in effect. It ends in the default filename.
    assert dialog.config_path_field.text().endswith("config.json")


def test_override_note_visible_only_when_env_set(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {})

    without = _dialog(qtbot, environ={})
    assert not without.override_note.isVisibleTo(without)

    with_env = _dialog(qtbot, environ={"TOOLBOX_CONFIG": "/env/config.json"})
    assert with_env.override_note.isVisibleTo(with_env)


def test_browse_sets_config_path(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {})
    dialog = _dialog(qtbot)

    monkeypatch.setattr(
        QtWidgets.QFileDialog,
        "getOpenFileName",
        staticmethod(lambda *a, **k: ("/picked/config.json", "Config files (*.json)")),
    )
    dialog.on_browse()

    assert dialog.config_path_field.text() == "/picked/config.json"


def test_browse_cancelled_leaves_path_unchanged(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {"config_path": "/abs/custom.json"})
    dialog = _dialog(qtbot)

    # QFileDialog returns an empty string when the user cancels.
    monkeypatch.setattr(
        QtWidgets.QFileDialog,
        "getOpenFileName",
        staticmethod(lambda *a, **k: ("", "")),
    )
    dialog.on_browse()

    assert dialog.config_path_field.text() == "/abs/custom.json"


def test_clear_reverts_to_default(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {"config_path": "/abs/custom.json"})
    dialog = _dialog(qtbot)
    dialog.on_clear()

    assert dialog.config_path_field.text().endswith("config.json")
    assert dialog.config_path_field.text() != "/abs/custom.json"


def test_custom_fields_hidden_unless_custom_selected(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {})
    dialog = _dialog(qtbot, system="Darwin")

    # A predefined terminal is selected by default → custom fields hidden.
    assert not dialog.custom_program_field.isVisibleTo(dialog)

    index = dialog.terminal_combo.findData(terminals.CUSTOM_TERMINAL_ID)
    dialog.terminal_combo.setCurrentIndex(index)
    assert dialog.custom_program_field.isVisibleTo(dialog)
    assert dialog.custom_args_field.isVisibleTo(dialog)


def test_custom_fields_prefilled_from_stored_command(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(
        monkeypatch,
        {
            "terminal_id": "custom",
            "terminal_command": {"program": "kitty", "args": ["-e", "{command}"]},
        },
    )
    dialog = _dialog(qtbot, system="Darwin")

    assert dialog.terminal_combo.currentData() == "custom"
    assert dialog.custom_program_field.text() == "kitty"
    assert dialog.custom_args_field.text() == "-e {command}"


def test_save_writes_config_and_terminal_load_modify_write(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Unrelated keys already in the store must survive the save.
    _stub_store(
        monkeypatch,
        {"version": 1, "window_geometry": "GEOM", "last_toolset": "Prod"},
    )
    saved = _capture_saves(monkeypatch)
    dialog = _dialog(qtbot, system="Darwin")

    monkeypatch.setattr(
        QtWidgets.QFileDialog,
        "getOpenFileName",
        staticmethod(lambda *a, **k: ("/picked/config.json", "")),
    )
    dialog.on_browse()
    dialog.terminal_combo.setCurrentIndex(
        dialog.terminal_combo.findData("iterm2")
    )
    dialog.accept()

    assert len(saved) == 1
    written = saved[0]
    assert written["config_path"] == "/picked/config.json"
    assert written["terminal_id"] == "iterm2"
    # Non-custom terminal → no terminal_command key.
    assert "terminal_command" not in written
    # Load-modify-write preserved the silent-persistence keys.
    assert written["window_geometry"] == "GEOM"
    assert written["last_toolset"] == "Prod"


def test_save_custom_terminal_splits_args(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {})
    saved = _capture_saves(monkeypatch)
    dialog = _dialog(qtbot, system="Darwin")

    dialog.terminal_combo.setCurrentIndex(
        dialog.terminal_combo.findData(terminals.CUSTOM_TERMINAL_ID)
    )
    dialog.custom_program_field.setText("kitty")
    dialog.custom_args_field.setText("-e {command}")
    dialog.accept()

    written = saved[0]
    assert written["terminal_id"] == "custom"
    # Whitespace-split into argv, with {command} its own element (spec §3/§4).
    assert written["terminal_command"] == {
        "program": "kitty",
        "args": ["-e", "{command}"],
    }


def test_clear_then_save_removes_config_path(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {"config_path": "/abs/custom.json"})
    saved = _capture_saves(monkeypatch)
    dialog = _dialog(qtbot)

    dialog.on_clear()
    dialog.accept()

    assert "config_path" not in saved[0]


def test_config_path_changed_true_when_path_changes(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {"config_path": "/abs/old.json"})
    _capture_saves(monkeypatch)
    dialog = _dialog(qtbot)

    monkeypatch.setattr(
        QtWidgets.QFileDialog,
        "getOpenFileName",
        staticmethod(lambda *a, **k: ("/abs/new.json", "")),
    )
    dialog.on_browse()
    dialog.accept()

    assert dialog.config_path_changed is True


def test_config_path_changed_false_when_only_terminal_changes(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {"config_path": "/abs/same.json", "terminal_id": "terminal"})
    _capture_saves(monkeypatch)
    dialog = _dialog(qtbot, system="Darwin")

    dialog.terminal_combo.setCurrentIndex(
        dialog.terminal_combo.findData("iterm2")
    )
    dialog.accept()

    assert dialog.config_path_changed is False


def test_cancel_writes_nothing(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_store(monkeypatch, {})
    saved = _capture_saves(monkeypatch)
    dialog = _dialog(qtbot)

    dialog.reject()

    assert saved == []
