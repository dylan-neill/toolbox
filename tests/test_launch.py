"""Launching a Tool surfaces what happened in the log pane (issue #7).

Headless GUI tests (offscreen Qt, like ``test_reload``) driving
the window's ``ToolLauncher`` with a real ``QProcess``. A launch that cannot start
or that fails inside its shell must say so in the log, rather than leaving the
user with a silent double-click.
"""

import os
import platform
from typing import Any

import pytest
from pytestqt.qtbot import QtBot

from toolbox import data, resources
from toolbox.model import Tool
from toolbox.ui import ToolboxWindow
from toolbox.ui.launcher import ToolLauncher

MISSING_REZ = "/nonexistent/toolbox-test/rez-env"


def _no_toolsets() -> dict[str, Any]:
    return {"toolsets": []}


def _tool() -> Tool:
    return Tool("Maya", "2025", "", ["maya-2025"], "app_icon512.png", "maya")


def _window(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, system: str) -> ToolboxWindow:
    monkeypatch.setattr(resources, "load_config", _no_toolsets)
    monkeypatch.setattr(resources, "REZ_COMMAND", MISSING_REZ)
    monkeypatch.setattr(platform, "system", lambda: system)
    data.populate()
    window = ToolboxWindow()
    qtbot.addWidget(window)
    return window


def _log(window: ToolboxWindow) -> str:
    return window.log_text_box.toPlainText()


def test_launch_that_cannot_start_is_logged(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Off macOS the rez program is started directly; a missing one never starts.
    window = _window(qtbot, monkeypatch, "Linux")

    window.launcher.run(_tool())

    qtbot.waitUntil(lambda: "failed to start" in _log(window).lower(), timeout=5000)
    assert MISSING_REZ in _log(window)


@pytest.mark.skipif(not os.path.exists("/bin/zsh"), reason="needs /bin/zsh")
@pytest.mark.skipif(platform.system() == "Windows", reason="POSIX shell only")
def test_macos_launch_shell_output_and_exit_are_logged(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    # On macOS zsh itself starts fine; the failure is zsh not finding rez-env.
    # Its stderr and the non-zero exit must reach the log.
    monkeypatch.setenv("ZDOTDIR", "/nonexistent/toolbox-test")  # skip user rc files
    window = _window(qtbot, monkeypatch, "Darwin")

    window.launcher.run(_tool())

    qtbot.waitUntil(lambda: "exit code 127" in _log(window).lower(), timeout=5000)
    assert MISSING_REZ in _log(window).split("Command:", 1)[1].split("\n", 1)[1]


def test_launcher_reports_through_its_log_signal_alone(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The launcher has no UI: everything it has to say arrives on ``log``.
    monkeypatch.setattr(resources, "REZ_COMMAND", MISSING_REZ)
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    launcher = ToolLauncher()
    lines: list[str] = []
    launcher.log.connect(lines.append)

    launcher.run(_tool())

    qtbot.waitUntil(lambda: any("failed to start" in line for line in lines), timeout=5000)
    assert lines[0] == "Running: Maya 2025 ..."
    assert lines[1].startswith(f"Command: {MISSING_REZ} ")
