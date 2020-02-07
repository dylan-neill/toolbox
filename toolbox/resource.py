import os
import platform
import shutil
import json

# Get parent folder of the folder containing this script file (ie the app root path)
app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def icon_path(icon):
    return os.path.join(app_path, "resources", "icons", icon)


def load_config():
    
    config_file = None
    result = None

    if platform.system().lower() == 'linux':
        config_file = os.path.expanduser("~/.config/toolbox/config.json")

    if not os.path.isfile(config_file):
        if not os.path.exists(os.path.dirname(config_file)):
            os.makedirs(os.path.dirname(config_file))
        default_config = os.path.join(app_path, "resources", "default_config.json")
        shutil.copy(default_config, config_file)
        if not os.path.isfile(config_file):
            print("Error copying {0} to {1}".format(default_config, config_file))
            return None
        else:
            print("Default config created at: {0}".format(config_file))
    
    with open(config_file) as file_id:
        result = json.load(file_id)
    
    return result


def python_command():
    if platform.system().lower() == 'windows':
        return 'pythonw.exe'
    else:
        return 'python3'


def rez_command():
    return 'rez-env'
