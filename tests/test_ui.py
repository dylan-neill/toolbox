from __future__ import annotations

import sys
import time

import pytest

pytest.importorskip("PySide6")
from PySide6 import QtCore

from toolbox.services.launcher import LaunchSpec
from toolbox.ui.main_window import ToolboxWindow


class NoopLauncher:
    def build_launch(self, tool, open_shell=False, system_name=None):
        return LaunchSpec(program="noop", args=[], display_command="noop")

    def start(self, tool, open_shell=False, parent=None):
        process = QtCore.QProcess(parent)
        QtCore.QTimer.singleShot(0, lambda: process.start(sys.executable, ["-c", "pass"]))
        return process, LaunchSpec(
            program=sys.executable,
            args=["-c", "pass"],
            display_command="pass",
        )


class ScriptLauncher:
    def build_launch(self, tool, open_shell=False, system_name=None):
        return LaunchSpec(program=sys.executable, args=["-c", "script"], display_command="script")

    def start(self, tool, open_shell=False, parent=None):
        process = QtCore.QProcess(parent)
        code = "import sys,time;print('hello');sys.stderr.write('warn\\n');time.sleep(0.05)"
        QtCore.QTimer.singleShot(0, lambda: process.start(sys.executable, ["-c", code]))
        return process, LaunchSpec(
            program=sys.executable,
            args=["-c", code],
            display_command=f"{sys.executable} -c {code}",
        )


def wait_until(predicate, qapp, timeout=3.0):
    end = time.time() + timeout
    while time.time() < end:
        if predicate():
            return True
        qapp.processEvents()
        time.sleep(0.01)
    return False


def test_ui_smoke_builds_window(qapp, stub_repository):
    window = ToolboxWindow(repository=stub_repository, launcher=NoopLauncher())

    assert window.toolsets_combo.count() == 1
    assert window.tools_list.count() == 1

    window.close()


def test_process_lifecycle_logs_output(qapp, stub_repository):
    window = ToolboxWindow(repository=stub_repository, launcher=ScriptLauncher())
    tool = stub_repository.load_toolsets()[0].tools[0]
    window.update_tool_info(tool)

    window.run_tool(tool)

    assert wait_until(lambda: len(window.process_list) == 0, qapp)
    log_text = window.log_text_box.toPlainText()
    assert "hello" in log_text
    assert "warn" in log_text
    assert "Process finished" in log_text

    window.close()


def test_package_table_editing_add_remove_blank_row(qapp, stub_repository):
    window = ToolboxWindow(repository=stub_repository, launcher=NoopLauncher())
    tool = stub_repository.load_toolsets()[0].tools[0]
    window.update_tool_info(tool)

    window.on_edit_clicked()
    assert window.is_editing_packages()

    initial_rows = window.packages_table.rowCount()
    last_row = initial_rows - 1
    item = window.packages_table.item(last_row, 0)
    assert item is not None
    item.setText("newpkg")
    qapp.processEvents()

    assert window.packages_table.rowCount() == initial_rows + 1

    remove_button = window.packages_table.cellWidget(0, 2)
    assert remove_button is not None
    remove_button.click()
    qapp.processEvents()

    last_row = window.packages_table.rowCount() - 1
    last_package_item = window.packages_table.item(last_row, 0)
    last_version_item = window.packages_table.item(last_row, 1)
    last_package = last_package_item.text().strip() if last_package_item is not None else ""
    last_version = last_version_item.text().strip() if last_version_item is not None else ""
    assert last_package == ""
    assert last_version == ""

    window.on_edit_clicked()
    assert stub_repository.updated is not None
    assert "newpkg" in stub_repository.updated[1]

    window.close()
