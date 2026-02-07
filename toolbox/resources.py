import os
import platform
import shutil
import json

# Get parent folder of the folder containing this script file (ie the app root path)
app_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
_config_file = None

def icon_path(icon):
    print("Icon path:", os.path.join(app_path, "resources", "icons", icon))
    return os.path.join(app_path, "resources", "icons", icon)


def load_config():
    """
    DEPRECATED: Use core.DataManager.load_config() instead.
    Kept for potential legacy compatibility during refactor, but should be removed eventually.
    """
    config_file = None
    result = None

    if 'TOOLBOX_CONFIG' in os.environ:
        config_file = os.path.expanduser(os.environ['TOOLBOX_CONFIG'])
        if os.path.isdir(config_file):
            config_file = os.path.join(config_file, "config.json")
    else:
        config_file = os.path.expanduser("~/.config/toolbox/config.json")

    if not os.path.isfile(config_file):
        if not os.path.exists(os.path.dirname(config_file)):
            os.makedirs(os.path.dirname(config_file))
        default_config = os.path.join(app_path, "resources", "default_config.json")
        try:
            shutil.copy(default_config, config_file)
            print(f"Default config created at: {config_file}")
        except Exception as e:
            print(f"Error copying {default_config} to {config_file}: {e}")
            return None

    with open(config_file) as file_id:
        result = json.load(file_id)
    
    return result


def config_path():
    return _config_file


def save_config(config_data):
    if _config_file is None:
        raise RuntimeError("Config path is not set. Call load_config() first.")
    with open(_config_file, "w") as file_id:
        json.dump(config_data, file_id, indent=2)
        file_id.write("\n")


def python_command():
    if platform.system().lower() == 'windows':
        return 'pythonw.exe'
    else:
        return 'python3'

def rez_command():
    return 'rez-env'
