# 03 — Settings store & Config resolution

Type: grilling
Status: resolved
Blocked by: 02

## Question

Design the Settings store and how it feeds Config selection, to the level of
detail the spec needs.

**Store schema** — the shape of `~/.config/toolbox/settings.json`. Decide the
keys and value shapes for all four in-scope settings:

- selected Config file path (file only, per the locked precedence),
- terminal choice (a predefined id + a Custom command string),
- window geometry (how Qt's `saveGeometry`/`restoreGeometry` bytes are stored in
  JSON — e.g. base64), and
- last-selected toolset (by name).

**Resolution & precedence** — wire `TOOLBOX_CONFIG` env (file or dir) › saved
Setting (file only) › default `~/.config/toolbox/config.json`. Decide how the
existing pure seam `config_path(system, environ)` in
`src/toolbox/resources/__init__.py` changes: does it take the settings-derived
path as an added pure parameter (keeping it filesystem-free and unit-testable
like today), and where does reading/writing `settings.json` live?

**Edge cases** — what happens when the saved Config path no longer exists or is
invalid (fall back to default + log? clear the setting?); does `settings.json`
need first-launch seeding/creation the way `config.json` does (the
*Not yet specified* item on the map).

**ADR** — decide whether the JSON-store-at-`~/.config` choice warrants an ADR
(it sits alongside ADR 0003 and rejects `QSettings`); if so, draft it.

Call `grilling`; consult `docs/adr/0003-user-config-location.md`.

## Answer

**Schema** — flat, all keys `NotRequired` (a missing key = that setting's
default), matching the `ConfigDict` TypedDict style:

```json
{
  "version": 1,
  "config_path": "/abs/path/to/config.json",
  "terminal_id": "iterm2",
  "terminal_command": null,
  "window_geometry": "<base64 of QMainWindow.saveGeometry()>",
  "last_toolset": "Production"
}
```

- `version` — schema version int for future migration.
- `terminal_id` + `terminal_command` — id is the dropdown choice; `terminal_command`
  holds the free-text template **only** when `terminal_id == "custom"`. The
  template's internal format is **ticket 04's** decision; the store just holds the string.
- `window_geometry` — base64 of `saveGeometry()`'s QByteArray.
- `last_toolset` — by name.

**Store module & resolution seam** — a **dedicated `src/toolbox/settings.py`**
module owns the store: a `SettingsDict` TypedDict, a pure `settings_path(system)`
(always `~/.config/toolbox/settings.json`, **unaffected by `TOOLBOX_CONFIG`**),
and `load_settings()` / `save_settings()` I/O wrappers. `config_path` stays a
pure seam in `resources/__init__.py` but gains a **third pure parameter**:
`config_path(system, environ, setting_config_path)`. Precedence stays
branch-only: **`TOOLBOX_CONFIG` env (file or dir) › `setting_config_path` (file)
› default**. `load_config` reads the setting via `settings.py` and passes the
path in (one-way `resources → settings` import; no cycle).

**Absence & invalidity** (never crash; always fall back to default config; log;
preserve saved values):

- No `settings.json` → all defaults; **not seeded** on launch (unlike
  `config.json`); written lazily on first setting change.
- Saved `config_path` gone/invalid → fall back to default config, **log to the
  log pane**, and **keep** the setting (transient network-drive absence).
- Corrupt `settings.json` → fall back to all defaults, log, don't overwrite until
  the next real save.

**ADR** — `docs/adr/0006-settings-store-as-json.md` drafted: JSON beside Config,
`QSettings` rejected for ADR-0003 single-location consistency; records the
base64-geometry cost, the no-seed rule, and the future-migration caveat.
