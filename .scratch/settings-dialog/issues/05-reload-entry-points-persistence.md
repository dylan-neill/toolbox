# 05 — Live reload, entry points & silent persistence

Type: grilling
Status: resolved
Blocked by: 03

## Question

Specify the main-window behavior around Settings and Config reload.

**Entry points** — a **gear icon** (opens the Settings dialog) and a **refresh
button**, placed top-right above the icon grid (no menu bar). Decide their exact
placement in the existing `setup_ui` layout, iconography, and tooltips.

**Live reload** — when the Config selection is saved in the dialog, and when the
refresh button is pressed, the toolset grid repopulates by re-reading the Config
(today `data.populate()` runs once at startup — `__main__.py`). Decide how
populate + grid refresh become a re-callable action, and what the refresh button
means when the Config file is edited externally.

**Selection preservation** — across a reload, if the previously selected toolset
still exists (by name), keep it selected; otherwise fall back. Define the rule.

**Silent persistence lifecycle** — window geometry and last-selected toolset are
persisted with no UI (into the store from ticket 03). Decide *when* each is
written (on close / on change) and *when* restored (on launch, replacing the
hardcoded `set_defaults` geometry and toolset index 0 — note the existing
"prefs on disk or hardcoded defaults" placeholder there).

Call `grilling`.

## Answer

**Entry points** — turn the top of the left column into a **top bar**
(`QHBoxLayout`): Toolsets label+combo on the left, a stretch, then **refresh** and
**gear** buttons right-aligned, directly above `tools_list`. Icons: Qt built-in
**`SP_BrowserReload`** for refresh; a **bundled `settings_icon.png`** (in
`resources/icons`) for the gear (Qt has no standard gear pixmap). Small fixed-size
buttons in the existing ~23px style; tooltips "Reload config" / "Settings". The
gear opens the Settings dialog (dialog layout is ticket 06).

**Reload action** — one **`reload_config()`** on `ToolboxWindow` that re-resolves
the config path, re-reads/parses, and rebuilds the grid (`update_toolset_list()` +
`update_tools()`); called by the refresh button and after the dialog saves a new
`config_path`. **Must not crash the running app**: it **catches read/parse errors**
(`parse_config` raises `KeyError` on a bad shape; the file may be mid-edit),
**logs to the log pane, and keeps the currently-loaded toolsets** — the grid never
blanks on a bad reload. Refresh always does a full re-read, so it picks up an
externally-edited Config.

**Selection preservation** — on reload, capture the current toolset **by name**
before rebuilding; reselect it if it still exists, else fall back to index 0.
Distinct from the setting: **launch restores the `last_toolset` setting; an
in-session reload preserves the current selection**, not the saved one.

**Silent persistence** — restore on launch (`set_defaults()` reads saved geometry,
falling back to the centered 845×460 default, and the `last_toolset`, replacing the
hardcoded geometry + `setCurrentIndex(0)`). **Window geometry saves on `closeEvent`**
(base64 of `saveGeometry()`). **`last_toolset` saves on change** (per user
decision — more crash-safe than close-time). Both use **load-modify-write**
(`load_settings()` → update the one key → `save_settings()`) so neither clobbers
`config_path`/`terminal`.

**Nuance from the on-change choice**: `currentIndexChanged` also fires during
programmatic repopulation (reload) and launch restore, so the on-change save must
be **guarded** (block the combo's signal / a re-entrancy flag during programmatic
selection) to persist only genuine user changes. Flagged for the spec + build.
