#!/usr/bin/python3

# System imports
import sys, os
from optparse import OptionParser
from PySide2 import QtCore, QtGui, QtWidgets
import ctypes
import platform

# Toolbox imports
import globalvars
import resource
import data
import ui


def main(dev=False):

    # Set the app id in windows so we get a taskbar icon
    if platform.system().lower() == 'windows':
        myappid = 'dn.toolbox.1' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    data.populate()

    QtWidgets.QApplication.setStyle('fusion')
    app = QtWidgets.QApplication(sys.argv)

    main_window = ui.ToolboxWindow(dev=dev)
    main_window.setPalette(globalvars.palette())
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-d", "--dev", dest="dev", help="Enable development mode", default=False)
    (options, args) = parser.parse_args()

    pipe_python = resource.get_pipe_python_root(options.dev)

    if pipe_python not in sys.path:
        sys.path.append(pipe_python)

    main(dev=options.dev)
