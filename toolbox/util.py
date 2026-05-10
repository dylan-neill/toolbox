import os
import platform

# For making windows shortcuts we need the windows extensions for Python
if platform.system().lower() == "windows":
    from win32com.client import Dispatch

def create_shortcut_on_desktop(name, target='', arguments='', working_dir='', icon=''):
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
