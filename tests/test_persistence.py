"""Window geometry & last-toolset persistence (ticket 05, spec §5).

Headless GUI tests (offscreen Qt, like ``test_smoke``/``test_reload``) covering
the silently-persisted settings on ``ToolboxWindow``:

- on launch the saved ``window_geometry`` and ``last_toolset`` are restored,
  each falling back to the built-in default (centered 845×460, first toolset)
  when absent;
- ``window_geometry`` is saved on close and ``last_toolset`` on a genuine user
  change, both via load-modify-write so ``config_path`` / ``terminal`` survive;
- programmatic combo repopulation (launch restore, live reload) is guarded so it
  never persists a spurious ``last_toolset`` — only a user's own pick writes.

Each test drives a live in-memory store through ``settings.load_settings`` /
``settings.save_settings`` and injects the toolsets by monkeypatching
``resources.load_config`` (as ``test_reload`` does).
"""

from typing import Any

import pytest
from PySide6 import QtCore, QtGui
from pytestqt.qtbot import QtBot

from toolbox import data, resources, settings
from toolbox.ui import ToolboxWindow


def _config(names: list[str]) -> dict[str, Any]:
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


def _live_store(
    monkeypatch: pytest.MonkeyPatch, initial: dict[str, Any] | None = None
) -> dict[str, Any]:
    """A load-modify-write store: ``load_settings`` returns a copy, ``save_settings``
    replaces the contents — so tests observe exactly what the window persisted."""
    store: dict[str, Any] = dict(initial or {})

    def _save(payload: Any) -> None:
        store.clear()
        store.update(payload)

    monkeypatch.setattr(settings, "load_settings", lambda: dict(store))
    monkeypatch.setattr(settings, "save_settings", _save)
    return store


def _window_with(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, names: list[str]
) -> ToolboxWindow:
    monkeypatch.setattr(resources, "load_config", lambda: _config(names))
    data.populate()
    window = ToolboxWindow()
    qtbot.addWidget(window)
    return window


def _spy_centering(monkeypatch: pytest.MonkeyPatch) -> list[bool]:
    """Record calls to ``center_with_default_size`` (the geometry fallback)."""
    calls: list[bool] = []

    def _record(self: ToolboxWindow) -> None:
        calls.append(True)

    monkeypatch.setattr(ToolboxWindow, "center_with_default_size", _record)
    return calls


# --- Launch restore: last_toolset ------------------------------------------


def test_launch_restores_saved_last_toolset(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _live_store(monkeypatch, {"last_toolset": "Beta"})
    window = _window_with(qtbot, monkeypatch, ["Alpha", "Beta", "Gamma"])

    assert window.toolsets_combo.currentText() == "Beta"


def test_launch_falls_back_to_first_when_saved_toolset_absent(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A saved toolset that no longer exists in the Config falls back to index 0.
    _live_store(monkeypatch, {"last_toolset": "Deleted"})
    window = _window_with(qtbot, monkeypatch, ["Alpha", "Beta"])

    assert window.toolsets_combo.currentIndex() == 0
    assert window.toolsets_combo.currentText() == "Alpha"


def test_launch_falls_back_to_first_when_unset(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _live_store(monkeypatch, {})
    window = _window_with(qtbot, monkeypatch, ["Alpha", "Beta"])

    assert window.toolsets_combo.currentIndex() == 0


def test_launch_restore_does_not_persist_last_toolset(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Restoring the saved toolset is programmatic (signal-blocked), so it must
    # not itself write last_toolset — the store is only what was seeded.
    store = _live_store(monkeypatch, {"last_toolset": "Beta"})
    _window_with(qtbot, monkeypatch, ["Alpha", "Beta", "Gamma"])

    assert store == {"last_toolset": "Beta"}


# --- Launch restore: geometry ----------------------------------------------


def test_launch_centers_default_when_no_geometry(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    _live_store(monkeypatch, {})
    calls = _spy_centering(monkeypatch)

    _window_with(qtbot, monkeypatch, ["Alpha"])

    assert calls == [True]


def test_launch_restores_saved_geometry_without_centering(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A geometry blob the production save path wrote is restored on the next
    # launch, so the centered-default fallback is not taken.
    store = _live_store(monkeypatch, {})
    seed = _window_with(qtbot, monkeypatch, ["Alpha"])
    seed.closeEvent(QtGui.QCloseEvent())
    assert store.get("window_geometry")

    calls = _spy_centering(monkeypatch)
    _window_with(qtbot, monkeypatch, ["Alpha"])

    assert calls == []


def test_launch_centers_default_on_corrupt_geometry(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A present-but-unusable geometry (restoreGeometry returns False) still falls
    # back to the centered default rather than leaving the window unsized.
    _live_store(monkeypatch, {"window_geometry": "not-real-geometry"})
    calls = _spy_centering(monkeypatch)

    _window_with(qtbot, monkeypatch, ["Alpha"])

    assert calls == [True]


# --- Saving on change / close ----------------------------------------------


def test_user_toolset_change_persists_last_toolset(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    # config_path must survive the change (load-modify-write, spec §5).
    store = _live_store(
        monkeypatch, {"config_path": "/abs/custom.json", "last_toolset": "Alpha"}
    )
    window = _window_with(qtbot, monkeypatch, ["Alpha", "Beta", "Gamma"])

    # A genuine user pick: the combo's signal is live (not blocked), so this
    # fires on_toolset_changed and writes.
    window.toolsets_combo.setCurrentIndex(2)  # Gamma

    assert store["last_toolset"] == "Gamma"
    assert store["config_path"] == "/abs/custom.json"


def test_reload_does_not_persist_last_toolset(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Live reload repopulates the combo programmatically; the guard must keep it
    # from writing a spurious last_toolset off the transient selection.
    store = _live_store(monkeypatch, {"config_path": "/abs/custom.json"})
    window = _window_with(qtbot, monkeypatch, ["Alpha", "Beta", "Gamma"])

    monkeypatch.setattr(resources, "load_config", lambda: _config(["Alpha", "Beta"]))
    window.reload_config()

    assert "last_toolset" not in store
    assert store == {"config_path": "/abs/custom.json"}


def test_close_saves_window_geometry_load_modify_write(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = _live_store(
        monkeypatch, {"config_path": "/abs/custom.json", "last_toolset": "Beta"}
    )
    window = _window_with(qtbot, monkeypatch, ["Alpha", "Beta"])

    window.closeEvent(QtGui.QCloseEvent())

    assert store["window_geometry"]  # a non-empty base64 string was written
    # The base64 round-trips back to the window's own geometry blob.
    assert QtCore.QByteArray.fromBase64(
        store["window_geometry"].encode("ascii")
    ) == window.saveGeometry()
    # Load-modify-write preserved the other settings.
    assert store["config_path"] == "/abs/custom.json"
    assert store["last_toolset"] == "Beta"
