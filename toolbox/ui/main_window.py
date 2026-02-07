from __future__ import annotations

import platform

from PySide6 import QtCore, QtGui, QtWidgets

from .. import globalvars, resources, util
from ..services.launcher import Launcher, QtProcessLauncher
from ..services.tool_repository import ToolRepository
from .widgets.tool_widget import ToolWidget


class ToolboxWindow(QtWidgets.QMainWindow):
    main_font = QtGui.QFont()
    main_font_bold = QtGui.QFont()
    main_font_bold.setBold(True)

    def __init__(self, repository: ToolRepository, launcher: Launcher | None = None):
        super().__init__()

        self.blank_pixmap = QtGui.QPixmap(64, 64)
        self.blank_pixmap.fill(QtGui.QColor(60, 60, 60))
        self.current_tool = None
        self._suppress_package_change = False
        self.repository = repository
        self.launcher = launcher or QtProcessLauncher(resources.rez_command())
        self.toolsets = self.repository.load_toolsets()

        pix = QtGui.QPixmap(resources.icon_path("app_icon512.png"))
        icon = QtGui.QIcon(pix)
        self.setWindowIcon(icon)

        self.setup_ui()
        self.setup_interaction()

    def setup_ui(self):
        app_name = globalvars.name_with_version()

        self.setWindowTitle(app_name)

        self.setMinimumWidth(600)
        self.setMinimumHeight(300)

        self.central_widget = QtWidgets.QWidget(self)

        self.main_vertical_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_columns_layout = QtWidgets.QHBoxLayout()
        self.main_vertical_layout.addLayout(self.main_columns_layout)

        self.tools_layout = QtWidgets.QVBoxLayout()

        self.toolsets_layout = QtWidgets.QFormLayout()
        self.tools_layout.addLayout(self.toolsets_layout)

        self.toolsets_combo = QtWidgets.QComboBox(self)
        self.toolsets_combo.setFixedWidth(260)
        self.toolsets_layout.addRow("Toolsets", self.toolsets_combo)

        self.tools_list = QtWidgets.QListWidget()
        self.tools_list.setFlow(QtWidgets.QListView.LeftToRight)
        self.tools_list.setWrapping(True)
        self.tools_list.setResizeMode(QtWidgets.QListView.Adjust)
        self.tools_layout.addWidget(self.tools_list)

        self.main_columns_layout.addLayout(self.tools_layout)
        self.main_columns_layout.addSpacing(20)

        self.details_layout = QtWidgets.QVBoxLayout()
        self.main_columns_layout.addLayout(self.details_layout)

        self.icon_layout = QtWidgets.QHBoxLayout()
        self.details_layout.addLayout(self.icon_layout)

        self.app_icon = QtWidgets.QLabel()
        self.app_icon.setPixmap(self.blank_pixmap)
        self.icon_layout.addWidget(self.app_icon)
        self.icon_layout.setAlignment(self.app_icon, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.app_name_layout = QtWidgets.QVBoxLayout()
        self.app_name_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.icon_layout.addLayout(self.app_name_layout)

        self.app_name_label = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPixelSize(18)
        font.setBold(True)
        self.app_name_label.setFont(font)
        self.app_name_label.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop | QtCore.Qt.AlignLeading
        )
        self.app_name_label.setFixedWidth(160)
        self.app_name_label.setWordWrap(True)
        self.app_name_layout.addWidget(self.app_name_label)

        self.details_app_subtitle = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPixelSize(14)
        self.details_app_subtitle.setFont(font)
        self.details_app_subtitle.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop | QtCore.Qt.AlignLeading
        )
        self.details_app_subtitle.setWordWrap(True)
        self.details_app_subtitle.setFixedWidth(160)
        self.app_name_layout.addWidget(self.details_app_subtitle)

        self.menu_button = QtWidgets.QPushButton()
        self.menu_button.setFixedSize(23, 23)
        self.context_menu = QtWidgets.QMenu()

        self.context_edit_action = QtGui.QAction("Edit...", self)
        self.context_edit_action.triggered.connect(self.on_edit_clicked)
        self.context_menu.addAction(self.context_edit_action)

        self.context_duplicate_action = QtGui.QAction("Duplicate", self)
        self.context_menu.addAction(self.context_duplicate_action)

        self.context_shortcut_action = QtGui.QAction("Create Desktop Shortcut", self)
        self.context_shortcut_action.triggered.connect(self.on_shortcut_clicked)
        self.context_menu.addAction(self.context_shortcut_action)

        self.context_delete_action = QtGui.QAction("Delete", self)
        self.context_menu.addAction(self.context_delete_action)

        self.menu_button.setMenu(self.context_menu)
        self.menu_button.setEnabled(False)
        self.icon_layout.addWidget(self.menu_button)
        self.icon_layout.setAlignment(self.menu_button, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        self.packages_label = QtWidgets.QLabel()
        self.packages_label.setText("Packages")
        self.packages_label.setEnabled(False)
        self.details_layout.addWidget(self.packages_label)

        self.packages_table = QtWidgets.QTableWidget()
        self.packages_table.setFixedWidth(260)
        self.packages_table.setColumnCount(3)
        self.packages_table.setRowCount(0)
        self.packages_table.setHorizontalHeaderLabels(["Package", "Version", ""])
        self.packages_table.verticalHeader().setVisible(False)
        self.packages_table.setColumnWidth(0, 120)
        self.packages_table.setColumnWidth(1, 100)
        self.packages_table.setColumnWidth(2, 30)
        self.packages_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(65, 65, 65))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(60, 60, 60))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

        self.packages_table.setEnabled(False)
        self.details_layout.addWidget(self.packages_table)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.details_layout.addLayout(self.buttons_layout)

        self.edit_button = QtWidgets.QPushButton()
        self.edit_button.setText("Edit...")
        self.edit_button.setFixedWidth(52)
        self.edit_button.setEnabled(False)
        self.buttons_layout.addWidget(self.edit_button)

        self.shell_button = QtWidgets.QPushButton()
        self.shell_button.setText("Open Shell")
        self.shell_button.setFixedWidth(80)
        self.shell_button.setEnabled(False)
        self.buttons_layout.addWidget(self.shell_button)

        self.launch_button = QtWidgets.QPushButton()
        font = QtGui.QFont()
        font.setBold(True)
        self.launch_button.setFont(font)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(55, 155, 93))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Button, brush)
        self.launch_button.setPalette(palette)
        self.launch_button.setText("Launch")
        self.launch_button.setEnabled(False)
        self.buttons_layout.addWidget(self.launch_button)

        self.log_layout = QtWidgets.QHBoxLayout()
        self.main_vertical_layout.addLayout(self.log_layout)
        self.log_text_box = QtWidgets.QTextEdit()
        self.log_layout.addWidget(self.log_text_box)
        self.log_text_box.setReadOnly(True)
        self.log_text_box.setFixedHeight(64)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(65, 65, 65))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(60, 60, 60))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        self.log_text_box.setPalette(palette)
        self.log_text_box.setText(app_name + " ready...")

        self.setCentralWidget(self.central_widget)

        self.process_list: list[QtCore.QProcess] = []

        self.set_defaults()
        self.update_toolset_list()
        self.update_tools()

    def update_log(self, text: str):
        cursor = self.log_text_box.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText("\n" + text.rstrip("\n"))
        sb = self.log_text_box.verticalScrollBar()
        sb.setValue(sb.maximum())

    def setup_interaction(self):
        self.tools_list.itemClicked.connect(self.on_item_clicked)
        self.tools_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.toolsets_combo.currentIndexChanged.connect(self.update_tools)
        self.launch_button.clicked.connect(self.on_launch_clicked)
        self.shell_button.clicked.connect(self.on_open_shell_clicked)
        self.edit_button.clicked.connect(self.on_edit_clicked)
        self.packages_table.itemChanged.connect(self.on_package_item_changed)

    def set_defaults(self):
        screen_rect = QtWidgets.QApplication.primaryScreen().geometry()
        width = 845
        height = 460
        pos_x = int((screen_rect.width() - width) / 2)
        pos_y = int((screen_rect.height() - height) / 2)

        self.setGeometry(pos_x, pos_y, width, height)
        self.toolsets_combo.setCurrentIndex(0)

    def update_toolset_list(self, project_list=None):
        self.toolsets_combo.clear()

        items = [toolset.name for toolset in self.toolsets]
        if project_list is not None:
            items.extend(project_list)
        self.toolsets_combo.addItems(items)

    def update_tools(self):
        self.tools_list.clear()
        toolset_name = self.toolsets_combo.currentText()
        toolset = self.repository.toolset_from_name(toolset_name)

        if toolset is not None:
            for tool in toolset.tools:
                list_item = ToolWidget(tool)
                list_item.setSizeHint(QtCore.QSize(128, 160))
                self.tools_list.addItem(list_item)
                self.tools_list.setItemWidget(list_item, list_item.widget)

    def on_item_clicked(self, item):
        self.update_tool_info(item.tool)

    def on_item_double_clicked(self, item):
        self.run_tool(item.tool)

    def on_launch_clicked(self):
        items = self.tools_list.selectedItems()
        if items:
            self.run_tool(items[0].tool)

    def on_open_shell_clicked(self):
        items = self.tools_list.selectedItems()
        if items:
            self.run_tool(items[0].tool, open_shell=True)

    def on_shortcut_clicked(self):
        if platform.system().lower() != "windows":
            self.update_log("Error: Creating desktop shortcuts is only supported on Windows")
            return
        items = self.tools_list.selectedItems()
        if items:
            tool = items[0].tool
            target = resources.python_command()
            arguments = f"{resources.rez_command()} {' '.join(tool.rez_wants)} -- {tool.command}"
            if tool.subtitle:
                name = f"{tool.title} ({tool.subtitle})"
            else:
                name = tool.title

            util.create_shortcut_on_desktop(name, target=target, arguments=arguments)

    def on_edit_clicked(self):
        if self.packages_table.editTriggers() == QtWidgets.QTableWidget.NoEditTriggers:
            self.packages_table.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
            self.edit_button.setText("Save")
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(155, 25, 25))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Button, brush)
            self.edit_button.setPalette(palette)
            if self.current_tool is not None:
                self.populate_packages_table(self.current_tool, editing=True)
        else:
            if self.current_tool is None:
                self.update_log("Error: No tool selected")
                return

            rez_wants = self.read_packages_table()
            success, error_message = self.repository.update_tool_packages(
                self.current_tool.tool_id, rez_wants
            )
            if not success:
                self.update_log(f"Error saving packages: {error_message}")
                return

            self.packages_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.edit_button.setText("Edit...")
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(80, 80, 80))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Button, brush)
            self.edit_button.setPalette(palette)
            self.populate_packages_table(self.current_tool, editing=False)
            self.update_log("Packages saved")
        self.update()

    def set_tool_info_enabled(self, enabled):
        if not enabled:
            self.packages_table.clearContents()

        self.app_name_label.setEnabled(enabled)
        self.details_app_subtitle.setEnabled(enabled)
        self.menu_button.setEnabled(enabled)
        self.packages_label.setEnabled(enabled)
        self.packages_table.setEnabled(enabled)
        self.edit_button.setEnabled(enabled)
        self.shell_button.setEnabled(enabled)
        self.launch_button.setEnabled(enabled)

    def update_tool_info(self, tool):
        self.current_tool = tool
        self.set_tool_info_enabled(True)
        self.app_name_label.setText(tool.title)
        self.details_app_subtitle.setText(tool.subtitle)
        pix = QtGui.QPixmap(resources.icon_path(tool.icon)).scaled(
            64, 64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )
        self.app_icon.setPixmap(pix)

        self.populate_packages_table(tool, editing=False)

    def is_editing_packages(self):
        return self.packages_table.editTriggers() != QtWidgets.QTableWidget.NoEditTriggers

    def populate_packages_table(self, tool, editing=False):
        self._suppress_package_change = True
        self.packages_table.blockSignals(True)
        self.packages_table.setColumnHidden(2, not editing)
        self.packages_table.clearContents()
        self.packages_table.setRowCount(0)

        for want in tool.rez_wants:
            tokens = want.split("-")
            row = self.packages_table.rowCount()
            self.packages_table.insertRow(row)

            item = QtWidgets.QTableWidgetItem()
            item.setText(tokens[0])
            self.packages_table.setItem(row, 0, item)

            if len(tokens) > 0:
                item = QtWidgets.QTableWidgetItem()
                item.setText("-".join(tokens[1:]))
                self.packages_table.setItem(row, 1, item)

            if editing:
                self.add_remove_button(row)

        if editing:
            self.add_blank_package_row()
        else:
            self.clear_remove_buttons()

        self.packages_table.blockSignals(False)
        self._suppress_package_change = False

    def add_blank_package_row(self):
        row = self.packages_table.rowCount()
        self.packages_table.insertRow(row)
        self.packages_table.setItem(row, 0, QtWidgets.QTableWidgetItem())
        self.packages_table.setItem(row, 1, QtWidgets.QTableWidgetItem())
        self.add_remove_button(row)

    def add_remove_button(self, row):
        button = QtWidgets.QPushButton("-")
        button.setFixedSize(22, 20)
        button.clicked.connect(self.on_remove_row_clicked)
        self.packages_table.setCellWidget(row, 2, button)

    def clear_remove_buttons(self):
        for row in range(self.packages_table.rowCount()):
            self.packages_table.setCellWidget(row, 2, None)

    def ensure_blank_row(self):
        if not self.is_editing_packages():
            return

        if self.packages_table.rowCount() == 0:
            self.add_blank_package_row()
            return

        last_row = self.packages_table.rowCount() - 1
        package_item = self.packages_table.item(last_row, 0)
        version_item = self.packages_table.item(last_row, 1)
        package = package_item.text().strip() if package_item is not None else ""
        version = version_item.text().strip() if version_item is not None else ""

        if package == "" and version == "":
            return

        self.add_blank_package_row()

    def read_packages_table(self):
        rez_wants = []
        for row in range(self.packages_table.rowCount()):
            package_item = self.packages_table.item(row, 0)
            version_item = self.packages_table.item(row, 1)
            package = package_item.text().strip() if package_item is not None else ""
            version = version_item.text().strip() if version_item is not None else ""

            if package == "":
                continue

            if version == "":
                rez_wants.append(package)
            else:
                rez_wants.append(f"{package}-{version}")

        return rez_wants

    def on_remove_row_clicked(self):
        if not self.is_editing_packages():
            self.update_log("Enable Edit to remove packages")
            return

        button = self.sender()
        if button is None:
            return

        for row in range(self.packages_table.rowCount()):
            if self.packages_table.cellWidget(row, 2) is button:
                self.packages_table.removeRow(row)
                self.ensure_blank_row()
                return

    def on_package_item_changed(self, item):
        if self._suppress_package_change or not self.is_editing_packages():
            return

        last_row = self.packages_table.rowCount() - 1
        if item.row() != last_row:
            return

        package_item = self.packages_table.item(last_row, 0)
        version_item = self.packages_table.item(last_row, 1)
        package = package_item.text().strip() if package_item is not None else ""
        version = version_item.text().strip() if version_item is not None else ""

        if package == "" and version == "":
            return

        self._suppress_package_change = True
        self.add_blank_package_row()
        self._suppress_package_change = False

    def update_proc_log(self, process):
        stdout = bytes(process.readAllStandardOutput()).decode("utf-8", errors="replace").strip()
        stderr = bytes(process.readAllStandardError()).decode("utf-8", errors="replace").strip()
        if stdout:
            self.update_log(stdout)
        if stderr:
            self.update_log(stderr)

    def process_cleanup(self, process, *_args):
        self.update_log("Process finished")
        if process in self.process_list:
            self.process_list.remove(process)

    def run_tool(self, tool, open_shell=False):
        self.update_log(f"Running: {tool.title} {tool.subtitle}...")

        try:
            process, spec = self.launcher.start(tool, open_shell=open_shell, parent=self)
        except Exception as exc:  # noqa: BLE001
            self.update_log(f"Error: {exc}")
            return

        self.update_log(f"Command: {spec.display_command}")

        process.readyReadStandardOutput.connect(lambda: self.update_proc_log(process))
        process.readyReadStandardError.connect(lambda: self.update_proc_log(process))
        process.finished.connect(lambda *args: self.process_cleanup(process, *args))
        process.errorOccurred.connect(lambda err: self.update_log(f"Process error: {err}"))
        self.process_list.append(process)
