"""Seam E: a headless smoke test proving the main window constructs.

This is the reference GUI test for the suite: it runs under
``QT_QPA_PLATFORM=offscreen`` (set in ``conftest.py``) so it needs no display,
and it guards against gross startup breakage without asserting any internal
detail of the window.
"""


from pytestqt.qtbot import QtBot


def test_main_window_constructs(qtbot: QtBot) -> None:
    from toolbox.ui import ToolboxWindow

    window = ToolboxWindow()
    qtbot.addWidget(window)

    assert window.windowTitle().startswith("Toolbox")
