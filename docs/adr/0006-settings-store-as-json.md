# Settings stored as JSON beside Config

App-level **Settings** (see `CONTEXT.md` "Settings") are stored as a hand-rolled
JSON file at `~/.config/toolbox/settings.json`, beside the user's `config.json`,
rather than through Qt's `QSettings`. The file is read and written by a dedicated
`settings.py` module; the config-file selection it holds is resolved with the
precedence **`TOOLBOX_CONFIG` env (file or dir) › `settings.json` `config_path`
(file) › default `~/.config/toolbox/config.json`**. The Settings file location is
fixed and unaffected by `TOOLBOX_CONFIG`. The schema is versioned (`version: 1`)
so a future shape change can migrate rather than guess.

## Considered Options

- **`QSettings`** — idiomatic in a Qt app and plugs straight into
  `saveGeometry`/`restoreGeometry`, but writes to native per-OS stores (plist on
  macOS, registry on Windows, ini on Linux). That scatters Toolbox's user state
  across native locations and reopens ADR 0003, which deliberately keeps **all**
  Toolbox user state under `~/.config/toolbox/` on every platform.
- **Hand-rolled JSON beside Config** (chosen) — keeps everything a user owns in
  one inspectable folder, consistent with ADR 0003, and lets Settings resolution
  reuse the pure-seam testing pattern already used for `config_path`/`load_config`
  (a pure resolver plus a thin I/O wrapper).

## Consequences

- The `QMainWindow.saveGeometry()` `QByteArray` must be **base64-encoded** to live
  in JSON; `QSettings` would have stored it natively. A minor cost.
- A missing `settings.json` means **all defaults** — it is not seeded on first
  launch the way `config.json` is (Config needs example content; Settings do not).
  A corrupt or unreadable file falls back to defaults and logs, and is not
  overwritten until the next real save.
- If Toolbox later adopts `QSettings` or `platformdirs`, it must ship a migration
  that moves existing `~/.config/toolbox/settings.json`, the same caveat ADR 0003
  records for `config.json`.
