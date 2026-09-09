# User config location stays at ~/.config

The user's `config.json` lives at `~/.config/toolbox/config.json` on **all**
platforms, including Windows and macOS, rather than the OS-native locations
(`%APPDATA%` on Windows, `~/Library/Application Support` on macOS). Adding macOS
support meant filling in the missing darwin branch; we deliberately used
`~/.config` there too for consistency.

Existing internal users already have their configs at `~/.config` on Windows,
so switching to native directories would strip their setup. Keeping one
convention is non-breaking and keeps the path logic simple.

## Consequences

- If Toolbox later adopts `platformdirs` for native per-OS locations, it must
  ship a migration that moves existing `~/.config/toolbox/` configs, not just
  change the path.
