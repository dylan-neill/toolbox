from PySide6 import QtCore, QtGui, QtWidgets

# Toolbox imports
import globalvars
import resource
import data
import util
import platform

class ToolWidget(QtWidgets.QListWidgetItem):

    def __init__(self, tool):
        super(ToolWidget, self).__init__()

        self.tool = tool
        self.widget = QtWidgets.QWidget()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(0)
        self.widget.setLayout(self.layout)

        pix = QtGui.QPixmap(resource.icon_path(tool.icon)).scaled(64,64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
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
        #self.app_subtitle_label.setFixedSize(QtCore.QSize(90,40))
        #self.app_subtitle_label.setMinimumSize(QtCore.QSize(90,40))
        #self.app_subtitle_label.setMaximumSize(QtCore.QSize(90,40))
        #self.app_subtitle_label.setMaximumWidth(90)

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

        pix = QtGui.QPixmap(resource.icon_path('app_icon512.png'))
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
        for toolset in data.toolsets:
            items.append(toolset.name)
        if project_list is not None:
            items.extend(project_list)
        self.toolsets_combo.addItems(items)


    def update_tools(self):

        self.tools_list.clear()
        toolset_name = self.toolsets_combo.currentText()
        toolset = data.toolset_from_name(toolset_name)

        if toolset is not None:
            for tool in toolset.tools:
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
            target = resource.python_command()
            arguments = "{rez} {wants} -- {command}".format(
                rez=resource.get_rez_command(),
                wants=" ".join(tool.rez_wants),
                command=tool.command
            )
            if tool.subtitle:
                name = "{title} ({subtitle})".format(title=tool.title, subtitle=tool.subtitle)
            else:
                name = tool.title

            util.create_shortcut_on_desktop(name, target=target, arguments=arguments)


    def on_edit_clicked(self):
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
        self.set_tool_info_enabled(True)
        self.app_name_label.setText(tool.title)
        self.details_app_subtitle.setText(tool.subtitle)
        pix = QtGui.QPixmap(resource.icon_path(tool.icon))\
                .scaled(64,64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.app_icon.setPixmap(pix)

        self.packages_table.clearContents()
        self.packages_table.setRowCount(len(tool.rez_wants))
        
        '''
        not_editable_flag = QtCore.Qt.ItemFlags()
        not_editable_flag != QtCore.Qt.ItemIsEditable
        '''

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


    def update_proc_log(self, process):
        self.update_log(str(process.readAll()))


    def process_cleanup(self, process):
        self.update_log("Process finished")
        self.process_list.remove(process)


    def run_tool(self, tool, open_shell=False):

        self.update_log(f'Running: {tool.title} {tool.subtitle}...')

        rez_command = resource.rez_command()

        rez_wants = ' '.join(tool.rez_wants)

        rez_command = f'{rez_command} {rez_wants}'
        command = ''

        if open_shell:
            if platform.system().lower() == 'windows':
                command = f'cmd.exe /C start cmd.exe /K {rez_command}' # Super hack!
            else:
                command = f'gnome-terminal -- {rez_command}'
        else:
            command = f'{rez_command} -- {tool.command}'

        self.update_log(f'Command: {command}')
        process = QtCore.QProcess(self)
        process.startCommand(command)
