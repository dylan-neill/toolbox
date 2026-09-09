"""Open Shell command construction, per platform.

Returned as (program, args) rather than one string because QProcess only splits
on double quotes with no escaping, so the macOS AppleScript (which embeds double
quotes) cannot survive string tokenisation.
"""

from toolbox import resources

REZ = "rez-env maya-2025 site"


def test_windows_opens_cmd_in_rez_env():
    program, args = resources.shell_command("Windows", REZ)
    assert program == "cmd.exe"
    # The rez invocation is passed through to the new shell.
    assert args[-3:] == ["rez-env", "maya-2025", "site"]


def test_linux_opens_gnome_terminal_in_rez_env():
    program, args = resources.shell_command("Linux", REZ)
    assert program == "gnome-terminal"
    assert args == ["--", "rez-env", "maya-2025", "site"]


def test_macos_opens_terminal_via_osascript():
    program, args = resources.shell_command("Darwin", REZ)
    assert program == "osascript"
    assert args[0] == "-e"
    # A single AppleScript argument that runs the rez env in a new Terminal.
    assert args[1] == 'tell application "Terminal" to do script "rez-env maya-2025 site"'
    assert len(args) == 2
