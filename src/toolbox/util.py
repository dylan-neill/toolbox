import os
import sys


def create_shortcut_on_desktop(
    name: str,
    target: str = '',
    arguments: str = '',
    working_dir: str = '',
    icon: str = '',
) -> None:
    # Windows-only: pywin32 ships no type stubs, and the win32com import only
    # exists on Windows. The sys.platform guard lets pyright narrow the rest of
    # the body to Windows, and doubles as a runtime guard if ever mis-called.
    if sys.platform != "win32":
        raise RuntimeError("Creating desktop shortcuts is only supported on Windows")

    from win32com.client import Dispatch  # pyright: ignore[reportMissingImports]

    path = os.path.join(os.path.expanduser('~'), 'Desktop', name + '.lnk')
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = working_dir
    if icon == '':
        pass
    else:
        shortcut.IconLocation = icon
    shortcut.save()
