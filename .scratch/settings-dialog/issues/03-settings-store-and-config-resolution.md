# 03 — Settings store & Config resolution

Type: grilling
Status: open
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
