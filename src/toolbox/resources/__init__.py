import importlib.resources
import json
import os
import platform

# Bundled, read-only assets (icons + the example Config) ship as package data
# inside this subpackage, so they resolve the same way from a source checkout and
# from a frozen Briefcase installer. This is distinct from the user's Config in
# ~/.config/toolbox/, which is writable user data and unaffected by this module.
_assets = importlib.resources.files(__name__)


def icon_path(icon):
    # Briefcase and source installs both lay package data out as real files, and
    # QPixmap needs a filesystem path (a string), not bytes — so a plain path is
    # what callers get.
    return str(_assets.joinpath("icons", icon))


def example_config_text():
    """The bundled example Config as JSON text — the seed for a new user Config."""
    return _assets.joinpath("example_config.json").read_text(encoding="utf-8")


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
        config_dir = os.path.dirname(config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(config_file, "w", encoding="utf-8") as file_id:
            file_id.write(example_config_text())
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
