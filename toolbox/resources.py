from __future__ import annotations

import os
import platform

# Get parent folder of the folder containing this script file (ie the app root path)
app_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def icon_path(icon: str) -> str:
    return os.path.join(app_path, "resources", "icons", icon)


def python_command() -> str:
    if platform.system().lower() == "windows":
        return "pythonw.exe"
    return "python3"


def rez_command() -> str:
    return os.environ.get("TOOLBOX_REZ_COMMAND", "rez-env")
