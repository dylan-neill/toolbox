"""Per-OS registry of *Open Shell* terminals (see spec §3, and the research note
on branch ``research/terminal-launch-invocations``).

Each terminal maps a ``terminal_id`` to a ``(program, args-template)`` pair — the
exact invocation that opens that terminal and runs a command inside it as a live
interactive window. The registry is plain data so the Settings dialog (ticket 04)
can list the OS's terminals from the same source that launches them.

The invocation is launched via Qt's ``QProcess.start(program, arguments)``, which
does **no** re-splitting — each list element is passed verbatim (the research
note's Qt caveats). So the templates carry the exact argv, and a placeholder marks
where the built ``rez-env <wants…>`` invocation is spliced in. Two placeholders
encode the two insertion modes the research note requires:

- ``{command}`` (``COMMAND_PLACEHOLDER``) — the rez invocation as **argv tokens**.
  As a whole element it expands into several argv entries (``rez-env A B`` → three
  list items); this is the mode for ``--`` / ``-e`` / ``wt``, and the documented
  shape for a Custom terminal's own-element placeholder (spec §3). Embedded inside
  a larger string it splices the **joined** ``rez-env A B`` in place — the mode for
  the macOS AppleScript, whose command sits inside a double-quoted script.
- ``{command_str}`` (``COMMAND_STR_PLACEHOLDER``) — always the joined
  ``rez-env A B`` as a **single token**, even standing alone. PowerShell's
  ``-Command`` needs its value as one string argument, which the position rule for
  ``{command}`` cannot express on its own. This second placeholder is a deliberate
  extension of spec §3's one-placeholder wording, forced by the research note's
  exact PowerShell invocation (``-Command "rez-env A B"``); the predefined registry
  uses it only for PowerShell.

This module imports nothing from the rest of the package **at runtime**
(``resources`` imports *it*; one-way, no cycle). A type-only import of the store's
``TerminalCommandDict`` is used purely for annotations.
"""

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    # Type-only: keeps the runtime "imports nothing from the package" guarantee.
    from .settings import TerminalCommandDict


# The ``terminal_id`` naming a Custom ``{program, args}`` invocation (spec §3),
# and the two placeholder spellings the registry templates use (see module
# docstring). Named so the load-bearing contract between the templates and
# ``substitute`` lives in one place — a mistyped literal would splice nothing.
CUSTOM_TERMINAL_ID = "custom"
COMMAND_PLACEHOLDER = "{command}"
COMMAND_STR_PLACEHOLDER = "{command_str}"


class Terminal(NamedTuple):
    """One entry in the terminal registry.

    ``label`` is the human name for the Settings dropdown (ticket 04); ``program``
    and ``args`` are the ``QProcess.start`` invocation, with ``args`` a template
    carrying a ``{command}`` / ``{command_str}`` placeholder (see module docstring).
    """

    label: str
    program: str
    args: list[str]


# Keyed by lowercased ``platform.system()`` then by ``terminal_id``. The entry per
# OS named in ``DEFAULT_TERMINAL`` reproduces today's *Open Shell* behaviour
# byte-for-byte; the rest are the added options. Exact invocations and their
# hazards are documented in the research note.
TERMINALS: dict[str, dict[str, Terminal]] = {
    "darwin": {
        "terminal": Terminal(
            "Terminal",
            "osascript",
            ["-e", 'tell application "Terminal" to do script "{command}"'],
        ),
        "iterm2": Terminal(
            "iTerm2",
            "osascript",
            [
                "-e",
                'tell application "iTerm2" to create window with default '
                'profile command "{command}"',
            ],
        ),
        # macOS Ghostty is an app bundle whose ``-e`` is only honoured by the CLI
        # binary directly (``open`` swallows it, and the app is single-instance).
        # Smoke-tested on a real install during implementation (ticket 02 / spec
        # verification task): the binary path launches a window running the command.
        "ghostty": Terminal(
            "Ghostty",
            "/Applications/Ghostty.app/Contents/MacOS/ghostty",
            ["-e", COMMAND_PLACEHOLDER],
        ),
    },
    "windows": {
        "cmd": Terminal(
            "Command Prompt",
            "cmd.exe",
            ["/C", "start", "cmd.exe", "/K", COMMAND_PLACEHOLDER],
        ),
        "windows-terminal": Terminal(
            "Windows Terminal",
            "wt.exe",
            ["new-tab", "cmd", "/k", COMMAND_PLACEHOLDER],
        ),
        # ``-Command`` takes its whole value as one string argument, so the joined
        # ``{command_str}`` (not the argv-expanding ``{command}``) is required here.
        "powershell": Terminal(
            "PowerShell",
            "cmd.exe",
            [
                "/C",
                "start",
                "powershell.exe",
                "-NoExit",
                "-Command",
                COMMAND_STR_PLACEHOLDER,
            ],
        ),
    },
    "linux": {
        "gnome-terminal": Terminal(
            "GNOME Terminal",
            "gnome-terminal",
            ["--", COMMAND_PLACEHOLDER],
        ),
        "konsole": Terminal(
            "Konsole",
            "konsole",
            ["-e", COMMAND_PLACEHOLDER],
        ),
        "xterm": Terminal(
            "XTerm",
            "xterm",
            ["-e", COMMAND_PLACEHOLDER],
        ),
    },
}


# The ``terminal_id`` used when the setting is unset — today's per-OS default.
DEFAULT_TERMINAL: dict[str, str] = {
    "darwin": "terminal",
    "windows": "cmd",
    "linux": "gnome-terminal",
}

# Unknown platforms fall through to this OS, mirroring today's ``shell_command``
# where "Linux and anything else" both open gnome-terminal.
_FALLBACK_OS = "linux"


def registry_for(system: str) -> dict[str, Terminal]:
    """The terminal registry for ``system`` (lowercased), Linux for anything else."""
    return TERMINALS.get(system.lower(), TERMINALS[_FALLBACK_OS])


def default_terminal_id(system: str) -> str:
    """The ``terminal_id`` an unset setting resolves to on ``system``."""
    return DEFAULT_TERMINAL.get(system.lower(), DEFAULT_TERMINAL[_FALLBACK_OS])


def resolve(
    system: str,
    terminal_id: str | None,
    custom_command: "TerminalCommandDict | None" = None,
) -> tuple[str, list[str]]:
    """Resolve a selection to a ``(program, args-template)`` pair — pure.

    ``terminal_id`` unset (``None``) or unknown resolves to the OS default;
    ``"custom"`` uses ``custom_command`` (a ``{program, args}`` object), falling
    back to the default if none was stored. There is no install detection: a known
    but uninstalled id still resolves (it fails at launch and logs like any bad
    command, per spec §3). The returned ``args`` is a fresh list, ready for
    ``substitute`` to fill its placeholder.
    """
    if terminal_id == CUSTOM_TERMINAL_ID and custom_command:
        return custom_command["program"], list(custom_command["args"])
    registry = registry_for(system)
    if terminal_id not in registry:
        # Unset, unknown, or "custom" with no stored command → the default.
        terminal_id = default_terminal_id(system)
    terminal = registry[terminal_id]
    return terminal.program, list(terminal.args)


def substitute(
    program: str, args_template: list[str], rez_tokens: list[str]
) -> tuple[str, list[str]]:
    """Splice ``rez_tokens`` into an args template, honouring both insertion modes.

    Pure. Walks the template element by element: a lone ``{command}`` expands into
    the rez argv tokens; a ``{command}`` embedded in a larger string splices the
    joined command in place; ``{command_str}`` always yields the joined command as
    a single token (see module docstring). ``program`` is returned unchanged so a
    single call produces the whole ``QProcess.start`` invocation.
    """
    joined = " ".join(rez_tokens)
    arguments: list[str] = []
    for element in args_template:
        if element == COMMAND_PLACEHOLDER:
            arguments.extend(rez_tokens)
        elif COMMAND_PLACEHOLDER in element:
            arguments.append(element.replace(COMMAND_PLACEHOLDER, joined))
        elif COMMAND_STR_PLACEHOLDER in element:
            arguments.append(element.replace(COMMAND_STR_PLACEHOLDER, joined))
        else:
            arguments.append(element)
    return program, arguments
