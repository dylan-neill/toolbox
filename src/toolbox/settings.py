"""App-level **Settings** store (see CONTEXT.md "Settings", ADR 0006).

Hand-rolled JSON at ``~/.config/toolbox/settings.json``, beside the user's
``config.json`` — deliberately *not* ``QSettings`` (ADR 0006), so all Toolbox
user state lives in one inspectable folder on every platform (ADR 0003).

The shape mirrors the ``config_path``/``load_config`` seam pattern: a pure
``settings_path`` resolver plus tolerant I/O wrappers. ``load_settings`` never
raises to its caller — a missing or corrupt file is all-defaults (``{}``), so a
fresh or mangled install does not crash Toolbox on launch. This module imports
nothing from the rest of the package (``resources`` may import *it*; one-way, no
cycle with ``data``).
"""

import json
import os
import platform
from typing import NotRequired, TypedDict, cast


class TerminalCommandDict(TypedDict):
    """A Custom terminal invocation, stored when ``terminal_id == "custom"``.

    ``args`` is a list of argv templates; a ``{command}`` element expands to the
    rez invocation tokens (see spec §3).
    """

    program: str
    args: list[str]


class SettingsDict(TypedDict):
    """The raw JSON shape of the Settings file (see spec §1).

    Every key is ``NotRequired``: a missing key means that setting's default, so
    an empty ``{}`` is the all-defaults store. ``version`` is a schema version
    int reserved for a future migration.
    """

    version: NotRequired[int]
    config_path: NotRequired[str]
    terminal_id: NotRequired[str]
    terminal_command: NotRequired[TerminalCommandDict]
    window_geometry: NotRequired[str]
    last_toolset: NotRequired[str]


def settings_path(system: str) -> str:
    """Resolve the Settings file path — pure, and always the fixed location.

    Unlike ``config_path``, this is **unaffected by ``TOOLBOX_CONFIG``**: the
    Settings file never moves. ``system`` is part of the contract (mirroring
    ``config_path``) so a future native-directory move has a seam to branch on;
    today every platform shares ``~/.config/toolbox/`` per ADR 0003.
    """
    return os.path.expanduser(
        os.path.join("~", ".config", "toolbox", "settings.json")
    )


def load_settings() -> SettingsDict:
    """Read and parse the Settings file; return ``{}`` if it is missing or bad.

    Never raises to the caller: a missing file, an unreadable one, invalid JSON,
    or a top-level value that is not a JSON object all yield the all-defaults
    store. The file is *not* seeded on first launch (unlike ``config.json``) — a
    missing store is simply all defaults, and is written lazily on the first
    setting change.
    """
    path = settings_path(platform.system())
    try:
        with open(path, encoding="utf-8") as file_id:
            data = json.load(file_id)
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict):
        # Valid JSON but the wrong top-level shape (e.g. a list) — treat as
        # corrupt rather than crash a caller expecting a mapping.
        return {}
    return cast(SettingsDict, data)


def save_settings(settings_dict: SettingsDict) -> None:
    """Write the Settings file, creating ``~/.config/toolbox/`` if needed.

    A faithful serializer: it writes exactly what it is given. Callers do
    **load-modify-write** (``load_settings`` → mutate one key → ``save_settings``)
    so a partial update never clobbers the other keys. (The parameter is
    ``settings_dict``, not ``settings``, to avoid shadowing the module name that
    ``resources`` imports this module under.)
    """
    path = settings_path(platform.system())
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file_id:
        json.dump(settings_dict, file_id, indent=2)
