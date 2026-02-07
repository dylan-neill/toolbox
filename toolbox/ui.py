import platform
from PySide6 import QtCore, QtGui, QtWidgets

from . import resources
from . import core
from . import util

def get_palette():
    palette = QtGui.QPalette()

    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(80, 80, 80))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(75, 75, 75))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(62, 62, 62))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(33, 33, 33))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(245, 245, 245))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(100, 100, 100))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(247, 147, 30))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
    
    # Inactive
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(80, 80, 80))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(75, 75, 75))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(62, 62, 62))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(33, 33, 33))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(245, 245, 245))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(100, 100, 100))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(247, 147, 30))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
    
    # Disabled
    brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(80, 80, 80))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(75, 75, 75))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(62, 62, 62))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(33, 33, 33))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(174, 174, 174))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
    
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
    
    return palette

class ToolWidget(QtWidgets.QListWidgetItem):

    def __init__(self, tool):
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


    def __init__(self):
        super(ToolboxWindow, self).__init__()

        self.blank_pixmap = QtGui.QPixmap(64,64)
        self.blank_pixmap.fill(QtGui.QColor(60,60,60))
        self.current_tool = None
        self._suppress_package_change = False

        self.controller = core.ToolboxController()

        pix = QtGui.QPixmap(resources.icon_path('app_icon512.png'))
        icon = QtGui.QIcon(pix)
        self.setWindowIcon(icon)

        self.setup_ui()
        self.setup_interaction()


    def setup_ui(self):

        app_name = self.controller.get_app_title()

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
        self.context_edit_action.triggered.connect(self.on_edit_clicked)
        self.context_menu.addAction(self.context_edit_action)

        self.context_duplicate_action = QtGui.QAction('Duplicate', self)
        self.context_menu.addAction(self.context_duplicate_action)

        self.context_shortcut_action = QtGui.QAction('Create Desktop Shortcut', self)
        self.context_shortcut_action.triggered.connect(self.on_shortcut_clicked)
        self.context_menu.addAction(self.context_shortcut_action)

        self.context_delete_action = QtGui.QAction('Delete', self)
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

        self.process_list = []

        self.set_defaults()
        self.update_toolset_list()
        self.update_tools()


    def update_log(self, text):
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


    def setup_interaction(self):
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
        self.packages_table.itemChanged.connect(self.on_package_item_changed)


    def set_defaults(self):
        """
        Sets control defaults whether from prefs on disk or hardcoded defaults
        :return:
        """
        screen_rect = QtWidgets.QApplication.primaryScreen().geometry()
        width = 845
        height = 460
        pos_x = (screen_rect.width()-width)/2
        pos_y = (screen_rect.height()-height)/2
        
        self.setGeometry(pos_x, pos_y, width, height)
        self.toolsets_combo.setCurrentIndex(0)


    def update_toolset_list(self, project_list=None):
        """
        Takes project list and adds to toolsets combo box with other default options
        :param project_list:
        :return:
        """

        self.toolsets_combo.clear()

        items = []
        for toolset in self.controller.get_toolsets():
            items.append(toolset.name)
        if project_list is not None:
            items.extend(project_list)
        self.toolsets_combo.addItems(items)


    def update_tools(self):

        self.tools_list.clear()
        toolset_name = self.toolsets_combo.currentText()
        tools = self.controller.get_tools_for_toolset(toolset_name)
        
        for tool in tools:
            list_item = ToolWidget(tool)
            list_item.setSizeHint(QtCore.QSize(128,160))
            self.tools_list.addItem(list_item)
            self.tools_list.setItemWidget(list_item, list_item.widget)


    def update_packages(self, tool):
        package_dict = {}

        row = 0
        self.packages_table.clearContents()
        self.packages_table.setRowCount(len(package_dict.items()))

        for package, version in package_dict.iteritems():
            new_item = QtWidgets.QTableWidgetItem()
            new_item.setText(package)
            new_item.setFlags(~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
            self.packages_table.setItem(row, 0, new_item)
            new_item = QtWidgets.QTableWidgetItem()
            new_item.setText(version)
            new_item.setFlags(~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
            self.packages_table.setItem(row, 1, new_item)
            row += 1

        self.packages_table.repaint()


    '''
    UI Interactions
    '''
    def on_item_clicked(self, item):
        self.update_tool_info(item.tool)
        #self.update_packages(item.tool)


    def on_item_double_clicked(self, item):
        self.run_tool(item.tool)


    def on_launch_clicked(self):
        items = self.tools_list.selectedItems()
        if len(items) > 0:
            self.run_tool(items[0].tool)


    def on_open_shell_clicked(self):
        items = self.tools_list.selectedItems()
        if len(items) > 0:
            self.run_tool(items[0].tool, open_shell=True)


    def on_shortcut_clicked(self):
        items = self.tools_list.selectedItems()
        if len(items) > 0:
            tool = items[0].tool
            success, message = self.controller.create_desktop_shortcut(tool)
            self.update_log(message)


    def on_edit_clicked(self):
        if self.packages_table.editTriggers() == QtWidgets.QTableWidget.NoEditTriggers:
            self.packages_table.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)
            self.edit_button.setText("Save")
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(155,25,25))
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
            success, error_message = self.controller.update_tool_packages(self.current_tool, rez_wants)
            if not success:
               self.update_log(f"Error saving packages: {error_message}")
               return

            self.packages_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.edit_button.setText("Edit...")
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(80,80,80))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Button, brush)
            self.edit_button.setPalette(palette)
            self.populate_packages_table(self.current_tool, editing=False)
            self.update_log("Packages saved")
        self.update()


    def set_tool_info_enabled(self, enabled):
        if enabled is False:
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
        pix = QtGui.QPixmap(resources.icon_path(tool.icon))\
                .scaled(64,64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
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
            tokens = want.split("-") # Can Rez use hyphens in package names?
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
        self.update_log(str(process.readAll()))


    def process_cleanup(self, process):
        self.update_log("Process finished")
        self.process_list.remove(process)


    def run_tool(self, tool, open_shell=False):

        self.update_log(f'Running: {tool.title} {tool.subtitle}...')
        
        command, process = self.controller.launch_tool(tool, open_shell)

        self.update_log(f'Command: {command}')


