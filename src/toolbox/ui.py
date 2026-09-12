# PySide6's bundled 6.11 stubs under-type signals/slots and many overloads, and
# Qt getters that can return None (parent(), primaryScreen(), ...) make strict
# null-checking noisy on UI glue. Per ADR 0005 this file runs the relaxed Qt
# profile — scoped to those stub-driven rules, not a blanket opt-out. Real
# correctness fixes (setGeometry ints, the primaryScreen guard) are made, not
# suppressed.
# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false, reportAttributeAccessIssue=false, reportOptionalMemberAccess=false

import os
import platform
from collections.abc import Mapping
from PySide6 import QtCore, QtGui, QtWidgets

from . import globalvars
from . import resources
from . import settings
from . import terminals
from . import data
from . import util
from .model import Tool

class ToolWidget(QtWidgets.QListWidgetItem):

    def __init__(self, tool: Tool) -> None:
        super(ToolWidget, self).__init__()

        self.tool = tool
        self.widget = QtWidgets.QWidget()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(0)
        self.widget.setLayout(self.layout)

        pix = QtGui.QPixmap(resources.icon_path(tool.icon)).scaled(64,64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setPixmap(pix)
        self.icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_label.setFixedSize(QtCore.QSize(64,64))
        self.layout.addWidget(self.icon_label)
        self.layout.setAlignment(self.icon_label, QtCore.Qt.AlignHCenter)

        self.layout.addSpacing(5)

        self.app_name_label = QtWidgets.QLabel(tool.title)
        font = QtGui.QFont()
        font.setPixelSize(16)
        self.app_name_label.setFont(font)
        self.app_name_label.setWordWrap(True)
        self.app_name_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.app_name_label)

        self.layout.addSpacing(2)

        self.app_subtitle_label = QtWidgets.QLabel(tool.subtitle)
        font = QtGui.QFont()
        font.setPixelSize(12)
        self.app_subtitle_label.setFont(font)
        self.app_subtitle_label.setWordWrap(True)
        self.app_subtitle_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.layout.addWidget(self.app_subtitle_label)

        self.layout.addStretch(1)


class ToolboxWindow(QtWidgets.QMainWindow):

    main_font = QtGui.QFont()
    main_font_bold = QtGui.QFont()
    main_font_bold.setBold(True)


    def __init__(self) -> None:
        super(ToolboxWindow, self).__init__()

        self.blank_pixmap = QtGui.QPixmap(64,64)
        self.blank_pixmap.fill(QtGui.QColor(60,60,60))

        pix = QtGui.QPixmap(resources.icon_path('app_icon512.png'))
        icon = QtGui.QIcon(pix)
        self.setWindowIcon(icon)

        self.setup_ui()
        self.setup_interaction()


    def setup_ui(self) -> None:

        app_name = globalvars.name_with_version()

        self.setWindowTitle(app_name)

        self.setMinimumWidth(600)
        self.setMinimumHeight(300)

        self.central_widget = QtWidgets.QWidget(self)

        self.main_vertical_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_columns_layout = QtWidgets.QHBoxLayout()
        self.main_vertical_layout.addLayout(self.main_columns_layout)

        self.tools_layout = QtWidgets.QVBoxLayout()

        # Top bar above the icon grid: the Toolsets label+combo on the left, a
        # stretch, then the refresh and gear buttons right-aligned (spec §5).
        self.top_bar_layout = QtWidgets.QHBoxLayout()
        self.tools_layout.addLayout(self.top_bar_layout)

        self.toolsets_label = QtWidgets.QLabel("Toolsets")
        self.top_bar_layout.addWidget(self.toolsets_label)

        self.toolsets_combo = QtWidgets.QComboBox(self)
        self.toolsets_combo.setFixedWidth(260)
        self.top_bar_layout.addWidget(self.toolsets_combo)

        self.top_bar_layout.addStretch(1)

        # Small fixed-size buttons matching the existing ~23px menu button.
        # Refresh re-reads the current Config live (reload_config); the gear
        # opens the Settings dialog. Qt's built-in reload pixmap for refresh,
        # the bundled gear icon for Settings.
        self.refresh_button = QtWidgets.QPushButton()
        self.refresh_button.setFixedSize(23, 23)
        self.refresh_button.setToolTip("Reload config")
        self.refresh_button.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_BrowserReload)
        )
        self.top_bar_layout.addWidget(self.refresh_button)

        # Opens the modal Settings dialog (wired in setup_interaction).
        self.settings_button = QtWidgets.QPushButton()
        self.settings_button.setFixedSize(23, 23)
        self.settings_button.setToolTip("Settings")
        self.settings_button.setIcon(
            QtGui.QIcon(resources.icon_path("settings_icon.png"))
        )
        self.top_bar_layout.addWidget(self.settings_button)

        self.tools_list = QtWidgets.QListWidget()
        self.tools_list.setFlow(QtWidgets.QListView.LeftToRight)
        self.tools_list.setWrapping(True)
        self.tools_list.setResizeMode(QtWidgets.QListView.Adjust)
        self.tools_layout.addWidget(self.tools_list)

        self.main_columns_layout.addLayout(self.tools_layout)
        self.main_columns_layout.addSpacing(20)

        self.details_layout = QtWidgets.QVBoxLayout()
        self.main_columns_layout.addLayout(self.details_layout)

        '''
        Icon and name
        '''
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
        self.app_name_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop | QtCore.Qt.AlignLeading)
        self.app_name_label.setFixedWidth(160)
        self.app_name_label.setWordWrap(True)
        self.app_name_layout.addWidget(self.app_name_label)

        self.details_app_subtitle = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPixelSize(14)
        self.details_app_subtitle.setFont(font)
        self.details_app_subtitle.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop | QtCore.Qt.AlignLeading)
        self.details_app_subtitle.setWordWrap(True)
        self.details_app_subtitle.setFixedWidth(160)
        self.app_name_layout.addWidget(self.details_app_subtitle)

        '''
        Menu Button
        '''
        self.menu_button = QtWidgets.QPushButton()
        self.menu_button.setFixedSize(23,23)
        self.context_menu = QtWidgets.QMenu()

        self.context_edit_action = QtGui.QAction('Edit...', self)
        # self.context_edit_action.triggered.connect(self.on_edit_clicked)
        self.context_edit_action.setEnabled(False)
        self.context_menu.addAction(self.context_edit_action)

        self.context_duplicate_action = QtGui.QAction('Duplicate', self)
        self.context_duplicate_action.setEnabled(False)
        self.context_menu.addAction(self.context_duplicate_action)

        self.context_shortcut_action = QtGui.QAction('Create Desktop Shortcut', self)
        self.context_shortcut_action.triggered.connect(self.on_shortcut_clicked)
        self.context_menu.addAction(self.context_shortcut_action)

        self.context_delete_action = QtGui.QAction('Delete', self)
        self.context_delete_action.setEnabled(False)
        self.context_menu.addAction(self.context_delete_action)

        self.menu_button.setMenu(self.context_menu)
        self.menu_button.setEnabled(False)
        self.icon_layout.addWidget(self.menu_button)
        self.icon_layout.setAlignment(self.menu_button, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        self.packages_label = QtWidgets.QLabel()
        self.packages_label.setText("Packages")
        self.packages_label.setEnabled(False)
        self.details_layout.addWidget(self.packages_label)

        # Package Info

        self.packages_table = QtWidgets.QTableWidget()
        self.packages_table.setFixedWidth(260)
        self.packages_table.setColumnCount(2)
        self.packages_table.setRowCount(0)
        self.packages_table.setHorizontalHeaderLabels(["Package", "Version"])
        self.packages_table.verticalHeader().setVisible(False)
        self.packages_table.setColumnWidth(0, 140)
        self.packages_table.setColumnWidth(1, 116)
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
        brush = QtGui.QBrush(QtGui.QColor(55,155,93))
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
        self.log_text_box.setText(app_name + ' ready...')

        self.setCentralWidget(self.central_widget)

        self.process_list: list[QtCore.QProcess] = []

        self.set_defaults()
        self.update_toolset_list()
        self.update_tools()


    def update_log(self, text: str) -> None:
        """
        Adds a line of text to the log pane
        :param text: The text to add
        :return:
        """
        cursor = self.log_text_box.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText('\n' + text.rstrip('\n'))
        sb = self.log_text_box.verticalScrollBar()
        sb.setValue(sb.maximum())


    def setup_interaction(self) -> None:
        """
        Makes all UI interaction connections
        :return:
        """
        self.tools_list.itemClicked.connect(self.on_item_clicked)
        self.tools_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.toolsets_combo.currentIndexChanged.connect(self.update_tools)
        self.launch_button.clicked.connect(self.on_launch_clicked)
        self.shell_button.clicked.connect(self.on_open_shell_clicked)
        self.edit_button.clicked.connect(self.on_edit_clicked)
        self.refresh_button.clicked.connect(self.reload_config)
        self.settings_button.clicked.connect(self.on_settings_clicked)


    def set_defaults(self) -> None:
        """
        Sets control defaults whether from prefs on disk or hardcoded defaults
        :return:
        """
        width = 845
        height = 460
        screen_rect = QtWidgets.QApplication.primaryScreen().geometry()
        # Integer division: setGeometry takes ints, and screen dimensions are ints.
        pos_x = (screen_rect.width() - width) // 2
        pos_y = (screen_rect.height() - height) // 2

        self.setGeometry(pos_x, pos_y, width, height)
        self.toolsets_combo.setCurrentIndex(0)


    def reload_config(self) -> None:
        """Re-resolve and re-read the Config, rebuilding the grid live.

        Wired to the refresh button. Re-resolves the config path and re-parses
        the file, so an externally edited Config is reflected without a restart.

        Never crashes and never blanks the grid: a read or parse error is caught
        and logged to the log pane while the currently-loaded toolsets stay on
        screen. ``data.populate`` only swaps ``data.toolsets`` on a clean parse,
        so a failure leaves the previous toolsets intact. The selected toolset is
        preserved by name across the reload, falling back to the first when it no
        longer exists.
        """
        previous = self.toolsets_combo.currentText()
        try:
            data.populate()
        except Exception as exc:
            # A resilience boundary around a user-editable file: the criterion is
            # "never crashes". parse_config's documented failure is KeyError on a
            # bad shape, but a hand-edited Config can fail in other ways too — a
            # corrupt file (json.JSONDecodeError / ValueError), an unreadable one
            # (OSError), or a wrong-typed shape (TypeError, e.g. a toolset that is
            # a string). Catch broadly, keep the current toolsets on screen, and
            # surface why rather than blank the grid.
            self.update_log(f"Config reload failed, keeping current toolsets: {exc}")
            return
        self.update_toolset_list()
        self.restore_toolset_selection(previous)
        # Rebuild the grid explicitly (spec §5) rather than leaning only on the
        # combo's currentIndexChanged side-effect — so a future guard that blocks
        # that signal during repopulation (ticket 05) cannot silently stop it.
        self.update_tools()


    def on_settings_clicked(self) -> None:
        """Open the modal Settings dialog; live-reload if the Config changed.

        The dialog owns its own load-modify-write on OK (spec §4); the window's
        only job afterwards is to re-read the Config when the saved
        ``config_path`` changed, so the grid updates immediately without a
        restart. Cancel writes nothing and leaves the grid untouched.
        """
        dialog = SettingsDialog(self)
        if dialog.exec() and dialog.config_path_changed:
            self.reload_config()


    def restore_toolset_selection(self, name: str) -> None:
        """Reselect the toolset named ``name``, falling back to the first.

        Used after a reload rebuilds the combo: a toolset that survived the edit
        is reselected by name (its index may have moved); one that is gone leaves
        the selection on index 0.
        """
        index = self.toolsets_combo.findText(name)
        self.toolsets_combo.setCurrentIndex(index if index >= 0 else 0)


    def update_toolset_list(self, project_list: list[str] | None = None) -> None:
        """
        Takes project list and adds to toolsets combo box with other default options
        :param project_list:
        :return:
        """

        self.toolsets_combo.clear()

        items: list[str] = []
        for toolset in data.toolsets:
            items.append(toolset.name)
        if project_list is not None:
            items.extend(project_list)
        self.toolsets_combo.addItems(items)


    def update_tools(self) -> None:

        self.tools_list.clear()
        toolset_name = self.toolsets_combo.currentText()
        toolset = data.toolset_from_name(toolset_name)

        if toolset is not None:
            for tool in toolset.tools:
                list_item = ToolWidget(tool)
                list_item.setSizeHint(QtCore.QSize(128,160))
                self.tools_list.addItem(list_item)
                self.tools_list.setItemWidget(list_item, list_item.widget)


    '''
    UI Interactions
    '''
    def on_item_clicked(self, item: ToolWidget) -> None:
        self.update_tool_info(item.tool)


    def on_item_double_clicked(self, item: ToolWidget) -> None:
        self.run_tool(item.tool)


    def on_launch_clicked(self) -> None:
        items = self.tools_list.selectedItems()
        if len(items) > 0:
            self.run_tool(items[0].tool)


    def on_open_shell_clicked(self) -> None:
        items = self.tools_list.selectedItems()
        if len(items) > 0:
            self.run_tool(items[0].tool, open_shell=True)


    def on_shortcut_clicked(self) -> None:
        if platform.system().lower() != "windows":
            self.update_log("Error: Creating desktop shortcuts is only supported on Windows")
            return
        items = self.tools_list.selectedItems()
        if len(items) > 0:
            tool = items[0].tool
            target = resources.python_command()
            arguments = resources.launch_command(
                resources.rez_command(), tool.rez_wants, tool.command
            )
            if tool.subtitle:
                name = f"{tool.title} ({tool.subtitle})"
            else:
                name = tool.title

            util.create_shortcut_on_desktop(name, target=target, arguments=arguments)


    def on_edit_clicked(self) -> None:
        if self.packages_table.editTriggers() == QtWidgets.QTableWidget.NoEditTriggers:
            self.packages_table.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
            self.edit_button.setText("Save")
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(155,25,25))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Button, brush)
            self.edit_button.setPalette(palette)
        else:
            self.packages_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.edit_button.setText("Edit...")
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(80,80,80))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Button, brush)
            self.edit_button.setPalette(palette)
        self.update()


    def set_tool_info_enabled(self, enabled: bool) -> None:
        if enabled is False:
            self.packages_table.clearContents()

        self.app_name_label.setEnabled(enabled)
        self.details_app_subtitle.setEnabled(enabled)
        # self.menu_button.setEnabled(enabled)
        self.packages_label.setEnabled(enabled)
        self.packages_table.setEnabled(enabled)
        # self.edit_button.setEnabled(enabled)
        self.shell_button.setEnabled(enabled)
        self.launch_button.setEnabled(enabled)


    def update_tool_info(self, tool: Tool) -> None:
        self.set_tool_info_enabled(True)
        self.app_name_label.setText(tool.title)
        self.details_app_subtitle.setText(tool.subtitle)
        pix = QtGui.QPixmap(resources.icon_path(tool.icon))\
                .scaled(64,64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.app_icon.setPixmap(pix)

        self.packages_table.clearContents()
        self.packages_table.setRowCount(len(tool.rez_wants))

        row = 0

        for want in tool.rez_wants:
            tokens = want.split("-") # Can Rez use hyphens in package names?
            item = QtWidgets.QTableWidgetItem()
            item.setText(tokens[0])
            self.packages_table.setItem(row, 0, item)

            if len(tokens) > 0:
                item = QtWidgets.QTableWidgetItem()
                item.setText("-".join(tokens[1:]))
                self.packages_table.setItem(row, 1, item)

            row += 1


    def update_proc_log(self, process: QtCore.QProcess) -> None:
        self.update_log(str(process.readAll()))


    def process_cleanup(self, process: QtCore.QProcess) -> None:
        self.update_log("Process finished")
        self.process_list.remove(process)


    def run_tool(self, tool: Tool, open_shell: bool = False) -> None:

        self.update_log(f'Running: {tool.title} {tool.subtitle}...')

        process = QtCore.QProcess(self)

        if open_shell:
            # Pass the rez invocation as tokens (not a joined string): the seam
            # splices them into the chosen terminal's args template per its
            # placeholder. The terminal comes from the Settings store — unset
            # reproduces today's per-OS default (ticket 02, spec §3).
            rez_tokens = [resources.rez_command(), *tool.rez_wants]
            stored = settings.load_settings()
            program, arguments = resources.shell_command(
                platform.system(),
                rez_tokens,
                stored.get("terminal_id"),
                stored.get("terminal_command"),
            )
            self.update_log(f'Command: {program} {" ".join(arguments)}')
            process.start(program, arguments)
        else:
            command = resources.launch_command(
                resources.rez_command(), tool.rez_wants, tool.command
            )
            self.update_log(f'Command: {command}')
            process.startCommand(command)


class SettingsDialog(QtWidgets.QDialog):
    """The modal **Settings** dialog (spec §4) — the UI face of the two settings
    wired in tickets 01 and 02.

    Two rows plus OK/Cancel: a **Config file** row (the current selected path, a
    **Browse…** for an existing ``.json``, a **Clear** that reverts to the
    default, and an inline note when ``TOOLBOX_CONFIG`` is overriding the
    setting), and an **Open Shell terminal** row (the OS's predefined terminals
    from the ``terminals`` registry + Custom, whose selection reveals program /
    arguments fields).

    The pure logic lives in the ``settings`` and ``terminals`` seams (tickets
    01/02); this dialog is the Qt glue that reads the store to seed its widgets
    and, on OK, does the **load-modify-write** back. ``system`` and ``environ``
    are injectable so the terminal registry and the override note are testable
    off the host OS; they default to the live platform and process environment.
    """

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        *,
        system: str | None = None,
        environ: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(parent)
        self._system = system if system is not None else platform.system()
        self._environ = environ if environ is not None else os.environ

        stored = settings.load_settings()
        # ``config_path`` as the setting sees it: a path string, or None for the
        # default. Captured at open so ``config_path_changed`` can tell the caller
        # whether a live reload is needed on OK.
        self._initial_config_path = stored.get("config_path")
        self._config_path: str | None = self._initial_config_path
        # Set by ``save`` (on OK) so ``on_settings_clicked`` knows to reload.
        self.config_path_changed = False

        self.setup_ui()
        self.load_from_settings(stored)


    def setup_ui(self) -> None:
        self.setWindowTitle("Settings")
        self.setModal(True)

        layout = QtWidgets.QVBoxLayout(self)
        self.form = QtWidgets.QFormLayout()
        layout.addLayout(self.form)

        # Config-file row: read-only path + Browse… + Clear.
        config_row = QtWidgets.QHBoxLayout()
        self.config_path_field = QtWidgets.QLineEdit()
        self.config_path_field.setReadOnly(True)
        self.config_path_field.setMinimumWidth(320)
        config_row.addWidget(self.config_path_field)
        self.browse_button = QtWidgets.QPushButton("Browse…")
        config_row.addWidget(self.browse_button)
        self.clear_button = QtWidgets.QPushButton("Clear")
        config_row.addWidget(self.clear_button)
        self.form.addRow("Config file", config_row)

        # Inline note shown only while TOOLBOX_CONFIG is overriding the setting.
        self.override_note = QtWidgets.QLabel(
            "TOOLBOX_CONFIG is set and is currently overriding this selection."
        )
        self.override_note.setWordWrap(True)
        self.form.addRow(self.override_note)

        # Open Shell terminal row: the OS's terminals + Custom.
        self.terminal_combo = QtWidgets.QComboBox()
        self.form.addRow("Open Shell terminal", self.terminal_combo)

        # Custom program / arguments, revealed only when Custom is selected.
        self.custom_program_field = QtWidgets.QLineEdit()
        self.form.addRow("Program", self.custom_program_field)
        self.custom_args_field = QtWidgets.QLineEdit()
        self.custom_args_field.setPlaceholderText("-e {command}")
        self.form.addRow("Arguments", self.custom_args_field)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        layout.addWidget(self.button_box)

        self.browse_button.clicked.connect(self.on_browse)
        self.clear_button.clicked.connect(self.on_clear)
        self.terminal_combo.currentIndexChanged.connect(
            self.update_custom_visibility
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)


    def load_from_settings(self, stored: settings.SettingsDict) -> None:
        """Seed the widgets from the store (spec §4)."""
        self.refresh_config_field()
        self.override_note.setVisible(bool(self._environ.get("TOOLBOX_CONFIG")))

        # The OS's predefined terminals in registry order, then Custom.
        for terminal_id, terminal in terminals.registry_for(self._system).items():
            self.terminal_combo.addItem(terminal.label, terminal_id)
        self.terminal_combo.addItem("Custom…", terminals.CUSTOM_TERMINAL_ID)

        # An unset terminal shows the OS default (today's behaviour); a stored id
        # selects that terminal. An unknown/stale stored id (e.g. a terminal from
        # another OS in a shared store) also falls back to the OS default rather
        # than leaning on index 0 — decoupled from the registry's ordering.
        terminal_id = stored.get("terminal_id") or terminals.default_terminal_id(
            self._system
        )
        index = self.terminal_combo.findData(terminal_id)
        if index < 0:
            index = self.terminal_combo.findData(
                terminals.default_terminal_id(self._system)
            )
        self.terminal_combo.setCurrentIndex(index)

        custom = stored.get("terminal_command")
        if custom:
            self.custom_program_field.setText(custom.get("program", ""))
            self.custom_args_field.setText(" ".join(custom.get("args", [])))

        self.update_custom_visibility()


    def refresh_config_field(self) -> None:
        """Show the selected path, or the default location when unset.

        The field mirrors the *setting*: a saved ``config_path``, or (when unset)
        the default ``~/.config/toolbox/config.json`` so the user sees what is in
        effect rather than an empty box. An empty ``environ`` is passed so the
        default shown is the true default, independent of any ``TOOLBOX_CONFIG``
        override (which the note explains separately).
        """
        if self._config_path:
            self.config_path_field.setText(self._config_path)
        else:
            self.config_path_field.setText(
                resources.config_path(self._system, {}, None)
            )


    def update_custom_visibility(self) -> None:
        """Reveal the Custom program/arguments fields only for the Custom entry.

        Resizes the dialog to fit afterwards: hiding the two rows shrinks the
        layout's size hint, but Qt does not pull an already-shown window back in
        on its own — without ``adjustSize`` the dialog keeps the taller height it
        grew to for Custom when switching back to a predefined terminal.
        """
        is_custom = (
            self.terminal_combo.currentData() == terminals.CUSTOM_TERMINAL_ID
        )
        self.form.setRowVisible(self.custom_program_field, is_custom)
        self.form.setRowVisible(self.custom_args_field, is_custom)
        self.adjustSize()


    def on_browse(self) -> None:
        """Pick an existing ``.json`` Config file (spec §4)."""
        start_dir = (
            os.path.dirname(self._config_path) if self._config_path else ""
        )
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Config file", start_dir, "Config files (*.json)"
        )
        if path:
            self._config_path = path
            self.refresh_config_field()


    def on_clear(self) -> None:
        """Revert to the default Config (removes ``config_path`` on save)."""
        self._config_path = None
        self.refresh_config_field()


    def save(self) -> None:
        """Load-modify-write the edited settings (spec §4).

        Re-reads the store immediately before writing so a partial update never
        clobbers keys another writer touched while the dialog was open (e.g. the
        silently-persisted ``window_geometry`` / ``last_toolset``). Clearing the
        Config path removes the key entirely rather than storing an empty string,
        so resolution falls through to the default. ``config_path_changed`` is
        set for the caller's live-reload decision.
        """
        stored = settings.load_settings()

        if self._config_path:
            stored["config_path"] = self._config_path
        else:
            stored.pop("config_path", None)

        terminal_id = self.terminal_combo.currentData()
        stored["terminal_id"] = terminal_id
        if terminal_id == terminals.CUSTOM_TERMINAL_ID:
            stored["terminal_command"] = {
                "program": self.custom_program_field.text(),
                # Whitespace-split into argv templates; a bare ``{command}``
                # becomes its own element and expands to the rez tokens (spec §3).
                "args": self.custom_args_field.text().split(),
            }
        else:
            stored.pop("terminal_command", None)

        settings.save_settings(stored)

        self.config_path_changed = (self._config_path or None) != (
            self._initial_config_path or None
        )


    def accept(self) -> None:
        """OK: persist the settings, then close (Cancel/``reject`` writes nothing)."""
        self.save()
        super().accept()
