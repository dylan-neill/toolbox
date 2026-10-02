# PySide6's bundled 6.11 stubs under-type signals/slots and many overloads.
# Per ADR 0005 this file runs the relaxed Qt profile — scoped to those
# stub-driven rules, not a blanket opt-out.
# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false, reportAttributeAccessIssue=false, reportOptionalMemberAccess=false

from PySide6 import QtCore, QtGui, QtWidgets

from .. import resources
from ..model import Tool


class ToolDetailsPanel(QtWidgets.QWidget):
    """The right-hand column: the selected Tool's icon, name, packages and actions.

    Shows whichever Tool it is given via ``show_tool`` and owns its own widgets'
    state. The actions it cannot perform itself — launching, opening a shell,
    creating a desktop shortcut — are emitted as signals for the window to act
    on against its current selection.
    """

    launch_requested = QtCore.Signal()
    shell_requested = QtCore.Signal()
    shortcut_requested = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.blank_pixmap = QtGui.QPixmap(64,64)
        self.blank_pixmap.fill(QtGui.QColor(60,60,60))

        self.setup_ui()


    def setup_ui(self) -> None:
        self.details_layout = QtWidgets.QVBoxLayout(self)
        self.details_layout.setContentsMargins(0, 0, 0, 0)
        # Stay at the width of the fixed-size contents and leave the spare
        # horizontal space to the tool grid, as the bare layout used to.
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred
        )

        # Icon, name and subtitle, with the menu button to the right.
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
        self.context_shortcut_action.triggered.connect(self.shortcut_requested)
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

        self.packages_table = QtWidgets.QTableWidget()
        self.packages_table.setFixedWidth(260)
        self.packages_table.setColumnCount(2)
        self.packages_table.setRowCount(0)
        self.packages_table.setHorizontalHeaderLabels(["Package", "Version"])
        self.packages_table.verticalHeader().setVisible(False)
        self.packages_table.setColumnWidth(0, 140)
        self.packages_table.setColumnWidth(1, 116)
        self.packages_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.packages_table.setEnabled(False)
        self.details_layout.addWidget(self.packages_table)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.details_layout.addLayout(self.buttons_layout)

        self.edit_button = QtWidgets.QPushButton()
        self.edit_button.setText("Edit...")
        self.edit_button.setFixedWidth(52)
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.on_edit_clicked)
        self.buttons_layout.addWidget(self.edit_button)

        self.shell_button = QtWidgets.QPushButton()
        self.shell_button.setText("Open Shell")
        self.shell_button.setFixedWidth(80)
        self.shell_button.setEnabled(False)
        self.shell_button.clicked.connect(self.shell_requested)
        self.buttons_layout.addWidget(self.shell_button)

        self.launch_button = QtWidgets.QPushButton()
        font = QtGui.QFont()
        font.setBold(True)
        self.launch_button.setFont(font)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(55, 155, 93))
        self.launch_button.setPalette(palette)
        self.launch_button.setText("Launch")
        self.launch_button.setEnabled(False)
        self.launch_button.clicked.connect(self.launch_requested)
        self.buttons_layout.addWidget(self.launch_button)


    def on_edit_clicked(self) -> None:
        if self.packages_table.editTriggers() == QtWidgets.QTableWidget.NoEditTriggers:
            self.packages_table.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
            self.edit_button.setText("Save")
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Button, QtGui.QColor(155, 25, 25))
            self.edit_button.setPalette(palette)
        else:
            self.packages_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.edit_button.setText("Edit...")
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Button, QtGui.QColor(80, 80, 80))
            self.edit_button.setPalette(palette)
        self.update()


    def set_enabled(self, enabled: bool) -> None:
        if not enabled:
            self.packages_table.clearContents()

        self.app_name_label.setEnabled(enabled)
        self.details_app_subtitle.setEnabled(enabled)
        # self.menu_button.setEnabled(enabled)
        self.packages_label.setEnabled(enabled)
        self.packages_table.setEnabled(enabled)
        # self.edit_button.setEnabled(enabled)
        self.shell_button.setEnabled(enabled)
        self.launch_button.setEnabled(enabled)


    def show_tool(self, tool: Tool) -> None:
        self.set_enabled(True)
        self.app_name_label.setText(tool.title)
        self.details_app_subtitle.setText(tool.subtitle)
        pix = QtGui.QPixmap(resources.icon_path(tool.icon))\
                .scaled(64,64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.app_icon.setPixmap(pix)

        self.packages_table.clearContents()
        self.packages_table.setRowCount(len(tool.packages))
        for row, (package, version) in enumerate(tool.packages):
            self.packages_table.setItem(row, 0, QtWidgets.QTableWidgetItem(package))
            self.packages_table.setItem(row, 1, QtWidgets.QTableWidgetItem(version))
