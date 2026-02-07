from __future__ import annotations

import platform
import sys

from PySide6 import QtWidgets

from . import globalvars
from .services.config_store import JsonConfigStore
from .services.tool_repository import InMemoryToolRepository
from .ui.main_window import ToolboxWindow


def main() -> None:
    if platform.system().lower() == "windows":
        import ctypes

        myappid = "dn.toolbox.1"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)  # type: ignore[attr-defined]

    repository = InMemoryToolRepository(JsonConfigStore())

    QtWidgets.QApplication.setStyle("fusion")
    app = QtWidgets.QApplication(sys.argv)

    main_window = ToolboxWindow(repository=repository)
    main_window.setPalette(globalvars.palette())
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
