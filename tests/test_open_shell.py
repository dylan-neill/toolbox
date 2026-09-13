"""Open Shell command construction: the per-OS terminal registry and the
``{command}`` placeholder (ticket 02, spec §3, research note).

``shell_command`` is pure: given the rez invocation as tokens and the selected
``terminal_id`` it returns the ``(program, arguments)`` that ``QProcess.start``
runs. Returned as a tuple rather than one string because QProcess only splits on
double quotes with no escaping, so the macOS AppleScript (which embeds double
quotes) cannot survive string tokenisation.

The defaults (unset ``terminal_id``) are asserted byte-for-byte against today's
behaviour: with no ``settings.json`` an existing user's *Open Shell* is unchanged.
"""

import pytest

from toolbox import resources, terminals

# The rez invocation as tokens, as the UI now builds it: rez-env + rez_wants.
REZ = ["rez-env", "maya-2025", "site"]
JOINED = "rez-env maya-2025 site"


# --- Unset terminal_id reproduces today's default byte-for-byte --------------


def test_default_windows_is_todays_cmd_invocation() -> None:
    program, args = resources.shell_command("Windows", REZ, None)
    assert program == "cmd.exe"
    assert args == ["/C", "start", "cmd.exe", "/K", "rez-env", "maya-2025", "site"]


def test_default_linux_is_todays_gnome_terminal_invocation() -> None:
    program, args = resources.shell_command("Linux", REZ, None)
    assert program == "gnome-terminal"
    assert args == ["--", "rez-env", "maya-2025", "site"]


def test_default_macos_is_todays_terminal_via_osascript() -> None:
    program, args = resources.shell_command("Darwin", REZ, None)
    assert program == "osascript"
    # A single AppleScript argument that runs the rez env in a new Terminal — the
    # joined command spliced into the double-quoted script.
    assert args == [
        "-e",
        f'tell application "Terminal" to do script "{JOINED}"',
    ]


def test_unknown_system_falls_back_to_gnome_terminal_like_today() -> None:
    # "Linux and anything else" both opened gnome-terminal before the registry.
    program, args = resources.shell_command("FreeBSD", REZ, None)
    assert program == "gnome-terminal"
    assert args == ["--", "rez-env", "maya-2025", "site"]


# --- Each predefined terminal produces the research-note invocation ----------


def test_iterm2_creates_window_via_osascript() -> None:
    program, args = resources.shell_command("Darwin", REZ, "iterm2")
    assert program == "osascript"
    assert args == [
        "-e",
        'tell application "iTerm2" to create window with default '
        f'profile command "{JOINED}"',
    ]


def test_ghostty_runs_the_cli_binary_with_expanded_argv() -> None:
    program, args = resources.shell_command("Darwin", REZ, "ghostty")
    assert program == "/Applications/Ghostty.app/Contents/MacOS/ghostty"
    # {command} as its own element expands to argv tokens after -e.
    assert args == ["-e", "rez-env", "maya-2025", "site"]


def test_windows_terminal_opens_a_new_tab_with_expanded_argv() -> None:
    program, args = resources.shell_command("Windows", REZ, "windows-terminal")
    assert program == "wt.exe"
    assert args == ["new-tab", "cmd", "/k", "rez-env", "maya-2025", "site"]


def test_powershell_passes_the_joined_command_as_one_token() -> None:
    program, args = resources.shell_command("Windows", REZ, "powershell")
    assert program == "cmd.exe"
    # -Command takes its whole value as a single string argument.
    assert args == ["/C", "start", "powershell.exe", "-NoExit", "-Command", JOINED]


def test_konsole_expands_argv_after_dash_e() -> None:
    program, args = resources.shell_command("Linux", REZ, "konsole")
    assert program == "konsole"
    assert args == ["-e", "rez-env", "maya-2025", "site"]


def test_xterm_expands_argv_after_dash_e() -> None:
    program, args = resources.shell_command("Linux", REZ, "xterm")
    assert program == "xterm"
    assert args == ["-e", "rez-env", "maya-2025", "site"]


# --- Fallbacks: unknown id, and system is case-insensitive -------------------


def test_unknown_terminal_id_falls_back_to_os_default() -> None:
    # No install detection: an id not in the registry resolves to the default
    # rather than crashing.
    program, args = resources.shell_command("Linux", REZ, "nonesuch")
    assert program == "gnome-terminal"
    assert args == ["--", "rez-env", "maya-2025", "site"]


def test_system_is_case_insensitive() -> None:
    program, _ = resources.shell_command("darwin", REZ, "iterm2")
    assert program == "osascript"


# --- Custom: a {program, args} object, both insertion modes ------------------


def test_custom_expands_command_as_argv_tokens() -> None:
    # {command} as its own element expands to the rez tokens (spec §3).
    custom: resources.settings.TerminalCommandDict = {
        "program": "alacritty",
        "args": ["-e", "{command}"],
    }
    program, args = resources.shell_command("Linux", REZ, "custom", custom)
    assert program == "alacritty"
    assert args == ["-e", "rez-env", "maya-2025", "site"]


def test_custom_splices_joined_command_inside_a_larger_argument() -> None:
    # {command} embedded in a string splices the joined command in place.
    custom: resources.settings.TerminalCommandDict = {
        "program": "osascript",
        "args": ["-e", 'tell app "Foo" to run "{command}"'],
    }
    program, args = resources.shell_command("Darwin", REZ, "custom", custom)
    assert program == "osascript"
    assert args == ["-e", f'tell app "Foo" to run "{JOINED}"']


def test_custom_with_no_stored_command_falls_back_to_default() -> None:
    # terminal_id is "custom" but nothing was stored: don't crash, use default.
    program, args = resources.shell_command("Linux", REZ, "custom", None)
    assert program == "gnome-terminal"
    assert args == ["--", "rez-env", "maya-2025", "site"]


# --- Empty rez_wants (Open Shell on a tool that requests no packages) ---------


def test_empty_rez_wants_opens_a_bare_rez_env_shell() -> None:
    program, args = resources.shell_command("Linux", ["rez-env"], None)
    assert program == "gnome-terminal"
    assert args == ["--", "rez-env"]


# --- Registry integrity: every template splices the command somewhere ---------


@pytest.mark.parametrize(
    "system,terminal_id",
    [
        (system, terminal_id)
        for system, registry in terminals.TERMINALS.items()
        for terminal_id in registry
    ],
)
def test_every_predefined_template_carries_a_placeholder(
    system: str, terminal_id: str
) -> None:
    # A mistyped placeholder (e.g. "{comand}") would splice nothing and pass
    # through as a literal arg — a silent failure. Guard that each predefined
    # template contains a recognized placeholder, and that the built invocation
    # actually contains the rez tokens.
    args_template = terminals.TERMINALS[system][terminal_id].args
    assert any(
        terminals.COMMAND_PLACEHOLDER in element
        or terminals.COMMAND_STR_PLACEHOLDER in element
        for element in args_template
    ), f"{system}/{terminal_id} template has no command placeholder"

    _, args = resources.shell_command(system, REZ, terminal_id)
    # The command lands either as expanded argv tokens or joined into some arg
    # (standalone for -Command, embedded inside the AppleScript string).
    assert REZ == args[-len(REZ):] or any(JOINED in element for element in args)


def test_default_terminal_id_exists_in_its_registry() -> None:
    # Each OS default must name a real registry entry, or unset would KeyError.
    for system, terminal_id in terminals.DEFAULT_TERMINAL.items():
        assert terminal_id in terminals.TERMINALS[system]
