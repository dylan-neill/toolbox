# 05 — Live reload, entry points & silent persistence

Type: grilling
Status: open
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
