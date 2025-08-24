import os
import platform
import shutil
import json

# Get parent folder of the folder containing this script file (ie the app root path)
app_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def icon_path(icon):
    print("Icon path:", os.path.join(app_path, "resources", "icons", icon))
    return os.path.join(app_path, "resources", "icons", icon)


def load_config():
    
    config_file = None
    result = None

    if 'TOOLBOX_CONFIG' in os.environ:
        config_file = os.path.expanduser(os.environ['TOOLBOX_CONFIG'])
        if os.path.isdir(config_file):
            config_file = os.path.join(config_file, "config.json")
    else:
        if platform.system().lower() == 'linux':
            config_file = os.path.expanduser("~/.config/toolbox/config.json")
        elif platform.system().lower() == 'windows':
            config_file = os.path.expanduser("~/.config/toolbox/config.json")

    if not os.path.isfile(config_file):
        if not os.path.exists(os.path.dirname(config_file)):
            os.makedirs(os.path.dirname(config_file))
        default_config = os.path.join(app_path, "resources", "default_config.json")
        shutil.copy(default_config, config_file)
        if not os.path.isfile(config_file):
            print(f"Error copying {default_config} to {config_file}")
            return None
        else:
            print(f"Default config created at: {config_file}")

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
