#!/usr/bin/python3

import sys
from PySide6 import QtWidgets

from . import globalvars
from . import data
from . import ui

def main() -> None:

    # Set the app id in windows so we get a taskbar icon. sys.platform (not
    # platform.system()) so pyright narrows the ctypes.windll access to Windows.
    if sys.platform == "win32":
        import ctypes
        myappid = 'dn.toolbox.1' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    data.populate()

    QtWidgets.QApplication.setStyle('fusion')
    app = QtWidgets.QApplication(sys.argv)

    main_window = ui.ToolboxWindow()
    main_window.setPalette(globalvars.palette())
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
