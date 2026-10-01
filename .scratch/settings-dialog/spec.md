# Settings & config selection

Add an app-level **Settings** store and a **Settings dialog** to Toolbox, so a
user can choose which Config file to load without setting the `TOOLBOX_CONFIG`
environment variable (awkward for GUI apps on macOS), pick the terminal used by
*Open Shell*, and have their window geometry and last-selected toolset remembered
between runs. Config changes take effect live, and a refresh control re-reads an
externally edited Config.

This spec consolidates five resolved wayfinder decisions
(`.scratch/settings-dialog/`); each section cites the ticket that owns the
decision. Terminal invocation facts live in the research note on branch
`research/terminal-launch-invocations`
(`.scratch/settings-dialog/research/terminal-launch-invocations.md`). The store
choice is recorded in
[ADR 0006](../../docs/adr/0006-settings-store-as-json.md).

## Goal

- A user can select their Config file and *Open Shell* terminal from a dialog
  opened by a gear button; `TOOLBOX_CONFIG` still works and overrides the setting.
- Window geometry and last-selected toolset persist with no UI.
- Config selection reloads live; a refresh button re-reads the current Config.
- No regression for existing users: with no `settings.json`, behaviour is
  byte-for-byte what it is today.

## Domain

Adds the term **Settings** to `CONTEXT.md` (already done, ticket *Settings domain
model & CONTEXT.md*): app-level state Toolbox keeps for itself, distinct from
**Config** (the toolsets file). One entry is a *setting*; the store is the
*Settings file* (`settings.json`). "Preferences" stays an avoided synonym.

## Decisions

### 1. The Settings store (`settings.py`)

*(ticket: Settings store & config resolution; ADR 0006)*

- A new **`src/toolbox/settings.py`** module owns the store. Hand-rolled JSON at
  **`~/.config/toolbox/settings.json`**, beside `config.json` (per ADR 0003's
  single-location convention; **not** `QSettings`).
- **Schema** — a `SettingsDict` `TypedDict`, all keys `NotRequired` (a missing key
  = that setting's default):

  ```json
  {
    "version": 1,
    "config_path": "/abs/path/to/config.json",
    "terminal_id": "iterm2",
    "terminal_command": { "program": "…", "args": ["…", "{command}"] },
    "window_geometry": "<base64 of QMainWindow.saveGeometry()>",
    "last_toolset": "Production"
  }
  ```

  `version` is a schema version int for future migration. `terminal_command` is
  populated only when `terminal_id == "custom"` (see §3).
- **API** (mirrors the `config_path`/`load_config` seam pattern):
  - `settings_path(system: str) -> str` — pure; always `~/.config/toolbox/settings.json`,
    **unaffected by `TOOLBOX_CONFIG`**.
  - `load_settings() -> SettingsDict` — reads/parses; returns `{}` on a missing or
    corrupt file (never raises to the caller).
  - `save_settings(settings: SettingsDict) -> None` — writes the file
    (creating the dir if needed). Callers do **load-modify-write** so partial
    updates never clobber other keys.
- **Import direction**: `resources` may import `settings` (one-way; no cycle with
  `data`).

### 2. Config-file selection & resolution

*(tickets: Settings store & config resolution; Settings domain model)*

- **Precedence**: `TOOLBOX_CONFIG` env (file **or** dir, as today) ›
  `settings.json` `config_path` (**file only**) › default
  `~/.config/toolbox/config.json`.
- **Seam change**: `config_path` gains a third **pure** parameter —
  `config_path(system, environ, setting_config_path)` — keeping it
  filesystem-light and unit-tested. `load_config` reads the setting via
  `settings.load_settings()` and passes the resolved path in.
- **Fallback** (never crash; always fall back to default Config; log; preserve
  saved values):
  - No `settings.json` → all defaults; **not seeded** on first launch (unlike
    `config.json`); written lazily on the first setting change.
  - Saved `config_path` gone/invalid → fall back to the default Config, **log to
    the log pane**, and **keep** the setting (a network drive may be transiently
    absent).
  - Corrupt `settings.json` → all defaults, log, don't overwrite until the next
    real save.

### 3. Terminal selection & *Open Shell* wiring

*(tickets: Terminal launch invocations; Terminal setting → Open Shell wiring)*

- A **data-driven registry** (keyed by `terminal_id`, grouped per OS) maps each
  terminal to a `(program, args-template)` pair. Lives with the terminal logic
  (`settings.py` or a small `terminals.py`).
- **Seam change**: `shell_command` becomes
  `shell_command(system, rez_tokens, terminal_id, custom_command=None)`, pure,
  returning `(program, list[str])`. It takes the rez invocation as **tokens**
  (`["rez-env", "A", "B"]`), not a pre-joined string.
- **`{command}` placeholder**, two insertion modes the template encodes:
  **joined single token** (osascript, PowerShell `-Command`) vs **expanded argv
  tokens** (`--`, `-e`, `wt`).
- **Predefined terminals** (exact `(program, args)` and hazards in the research
  note): macOS Terminal / iTerm2 / Ghostty; Windows Windows Terminal / cmd /
  PowerShell; Linux gnome-terminal / konsole / xterm.
- **Custom** = a `{program, args}` object (args is a list of argv templates;
  `{command}` as its own element expands to the rez tokens) — **not** a single
  free-text line (sidesteps QProcess's quote-only tokeniser).
- **Default when `terminal_id` unset** → today's per-OS default **byte-for-byte**
  (macOS Terminal via osascript, Windows `cmd /C start … /K`, Linux
  `gnome-terminal --`).
- **No install detection** — the full list + Custom is always offered; an
  uninstalled pick fails and logs like any bad command. **No `--hold` flags** —
  windows close on shell exit, matching current behaviour.

### 4. The Settings dialog

*(entry point from ticket: Live reload…; layout specified here, no prototype)*

- A **modal `QDialog`** titled "Settings", opened by the gear button (§5). Two
  rows plus OK/Cancel:
  - **Config file** — a read-only field showing the current selected path, a
    **Browse…** button (`QFileDialog`, existing `.json` file only), and a
    **Clear** button that reverts to the default (removes `config_path` from the
    store). If `TOOLBOX_CONFIG` is set, show an inline note that the environment
    variable is currently overriding this setting.
  - **Open Shell terminal** — a `QComboBox` of the OS's predefined terminals +
    "Custom…". Selecting Custom reveals a **program** field and an **arguments**
    field (whitespace-separated, `{command}` placeholder), stored as the
    `{program, args}` object.
- **On OK**: load-modify-write `config_path`, `terminal_id`, `terminal_command`;
  if `config_path` changed, call `reload_config()` (§5). **On Cancel**: no writes.

### 5. Main-window changes

*(ticket: Live reload, entry points & persistence)*

- **Top bar** above the icon grid (`tools_list`): a `QHBoxLayout` with the
  Toolsets label+combo on the left, a stretch, then **refresh** and **gear**
  buttons right-aligned. Refresh uses Qt's `SP_BrowserReload`; the gear uses a
  bundled `resources/icons/settings_icon.png`. Small fixed-size buttons matching
  the existing ~23px style; tooltips "Reload config" / "Settings".
- **`reload_config()`** on `ToolboxWindow`: re-resolves the config path,
  re-reads/parses, rebuilds the grid (`update_toolset_list()` + `update_tools()`).
  Called by the refresh button and after a dialog save. **Must not crash**: it
  catches read/parse errors (`parse_config` raises `KeyError` on a bad shape),
  **logs to the log pane, and keeps the currently-loaded toolsets** — the grid
  never blanks on a bad reload. Refresh does a full re-read (picks up external
  edits).
- **Selection preservation**: on reload, capture the current toolset **by name**;
  reselect if it still exists, else fall back to index 0.
- **Persistence lifecycle**:
  - **Restore on launch** — `set_defaults()` reads saved `window_geometry`
    (falling back to the current centered 845×460 default) and `last_toolset`,
    replacing the hardcoded geometry and `setCurrentIndex(0)`. Launch restores the
    saved `last_toolset`; in-session reloads preserve the *current* selection.
    Restoring the toolset must be **guarded** so it doesn't count as a user change.
  - **Save `window_geometry` on `closeEvent`** (base64 of `saveGeometry()`).
  - **Save `last_toolset` on change** (`currentIndexChanged`) — **guarded** with a
    signal-block / re-entrancy flag so programmatic repopulation (reload, launch
    restore) does not persist spurious values. Only genuine user changes write.
  - Both saves are **load-modify-write**, so they never clobber
    `config_path`/`terminal`.

### 6. Assets, docs, tests

- Bundle `settings_icon.png` under `src/toolbox/resources/icons/` (package data,
  resolves in source and Briefcase builds alike).
- Update the README **Configuration** section: document the Settings dialog and
  that `TOOLBOX_CONFIG` overrides the saved `config_path`.
- Tests, following the existing pure-seam pattern: `config_path` with the new
  third param and full precedence; `settings_path`; `load_settings` on
  missing/corrupt files; `shell_command` for each `terminal_id` (defaults
  byte-for-byte equal to today) and the Custom placeholder in both insertion
  modes. The headless GUI smoke test must still pass.

## Scope

**In scope**: `settings.py` store + schema; `config_path`/`load_config`
resolution changes; `shell_command` terminal registry + Custom; the Settings
dialog; the top-bar gear/refresh; `reload_config()`; geometry/last-toolset
persistence; the bundled gear icon; README + tests; ADR 0006 and the CONTEXT.md
term (already written).

**Out of scope** (from the map): a rez-env command/path setting; a theme setting;
`QSettings`/native storage; a menu bar (⌘, Settings item). `--hold`/keep-open
terminal flags are deliberately omitted (easy later addition).

**Verification task** (carried from ticket *Terminal setting → Open Shell
wiring*): **Ghostty on macOS is unverified** — `-e` fails via `open` and it is
single-instance. Ship it via the direct CLI binary
(`…/Ghostty.app/Contents/MacOS/ghostty -e …`) but **smoke-test on a real install
during implementation**; fall back to its AppleScript route if the binary path
misbehaves.

## Done when

`settings.json` selects the Config file (with `TOOLBOX_CONFIG` overriding it), the
Settings dialog edits config + terminal, the gear/refresh controls and live
reload work, geometry + last toolset persist across runs, a missing/corrupt store
or config falls back without crashing, `uv run pytest` is green on all three OSes
(new seam tests included), and the README documents the feature.
