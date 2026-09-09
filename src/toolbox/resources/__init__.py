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


def config_path(system, environ):
    """Seam B: resolve the user Config file path from platform + environment.

    Pure branching logic; the only filesystem touch is classifying a
    ``TOOLBOX_CONFIG`` override as a file or a directory. ``TOOLBOX_CONFIG`` (a
    file or a directory) overrides on every platform. Otherwise, per ADR 0003,
    all platforms — Windows, macOS (Darwin), and Linux — deliberately share
    ``~/.config/toolbox/``; macOS used to fall through to ``None`` here and crash
    on launch. ``system`` is part of the contract so a future native-directory
    move has a seam to branch on.
    """
    override = environ.get('TOOLBOX_CONFIG')
    if override:
        path = os.path.expanduser(override)
        if os.path.isdir(path):
            path = os.path.join(path, "config.json")
        return path

    return os.path.expanduser(os.path.join("~", ".config", "toolbox", "config.json"))


def launch_command(rez_command, rez_wants, command):
    """Seam A: build the ``rez-env <rez_wants> -- <command>`` invocation.

    Pure: takes the Rez command, a Tool's ``rez_wants`` list, and its
    ``command``, and returns the full string that starts the DCC inside its Rez
    environment. Extracted from the UI so the produced string is unit-tested.
    An empty ``rez_wants`` leaves a doubled space where the want list would
    sit, which is shell-equivalent — the output is byte-for-byte what the UI
    built before this seam existed.
    """
    return f"{rez_command} {' '.join(rez_wants)} -- {command}"


def shell_command(system, rez_command):
    """Command that opens an interactive terminal inside ``rez_command``.

    Returned as ``(program, arguments)`` rather than one string because QProcess
    only splits on double quotes with no escaping, so the macOS AppleScript
    (which embeds double quotes) cannot survive string tokenisation.
    """
    system = system.lower()
    if system == 'windows':
        return 'cmd.exe', ['/C', 'start', 'cmd.exe', '/K', *rez_command.split()]
    if system == 'darwin':
        script = f'tell application "Terminal" to do script "{rez_command}"'
        return 'osascript', ['-e', script]
    # Linux and anything else.
    return 'gnome-terminal', ['--', *rez_command.split()]


def load_config():
    config_file = config_path(platform.system(), os.environ)

    if not os.path.isfile(config_file):
        config_dir = os.path.dirname(config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(config_file, "w", encoding="utf-8") as file_id:
            file_id.write(example_config_text())
        print(f"Default config created at: {config_file}")

    with open(config_file) as file_id:
        return json.load(file_id)


def python_command():
    if platform.system().lower() == 'windows':
        return 'pythonw.exe'
    else:
        return 'python3'

def rez_command():
    return 'rez-env'
