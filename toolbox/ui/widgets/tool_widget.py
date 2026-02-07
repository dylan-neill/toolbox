from __future__ import annotations

from PySide6 import QtCore, QtGui, QtWidgets

from ... import resources


class ToolWidget(QtWidgets.QListWidgetItem):
    def __init__(self, tool) -> None:
        super().__init__()

        self.tool = tool
        self.widget = QtWidgets.QWidget()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(0)
        self.widget.setLayout(self.layout)

        pix = QtGui.QPixmap(resources.icon_path(tool.icon)).scaled(
            64,
            64,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setPixmap(pix)
        self.icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setFixedSize(QtCore.QSize(64, 64))
        self.layout.addWidget(self.icon_label)
        self.layout.setAlignment(self.icon_label, QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.layout.addSpacing(5)

        self.app_name_label = QtWidgets.QLabel(tool.title)
        font = QtGui.QFont()
        font.setPixelSize(16)
        self.app_name_label.setFont(font)
        self.app_name_label.setWordWrap(True)
        self.app_name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.app_name_label)

        self.layout.addSpacing(2)

        self.app_subtitle_label = QtWidgets.QLabel(tool.subtitle)
        font = QtGui.QFont()
        font.setPixelSize(12)
        self.app_subtitle_label.setFont(font)
        self.app_subtitle_label.setWordWrap(True)
        self.app_subtitle_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )

        self.layout.addWidget(self.app_subtitle_label)

        self.layout.addStretch(1)
