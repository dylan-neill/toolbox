#!/usr/bin/python3

import sys
from PySide6 import QtWidgets
import platform

import globalvars
import data
import ui

def main():

    # Set the app id in windows so we get a taskbar icon
    if platform.system().lower() == 'windows':
        import ctypes
        myappid = 'dn.toolbox.1' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    data.populate()

    QtWidgets.QApplication.setStyle('fusion')
    app = QtWidgets.QApplication(sys.argv)

    main_window = ui.ToolboxWindow()
    main_window.setPalette(globalvars.palette())
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
