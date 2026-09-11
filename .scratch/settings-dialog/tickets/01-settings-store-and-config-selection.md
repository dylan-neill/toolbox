# 01: Settings store & config-file selection

**What to build:** Toolbox reads app-level **Settings** from a JSON store and uses
them to pick which Config file to load — so a user no longer needs the
`TOOLBOX_CONFIG` environment variable. Putting a config-file path in
`~/.config/toolbox/settings.json` makes Toolbox load that Config; `TOOLBOX_CONFIG`
still works and overrides it; a missing or invalid saved path falls back to the
default Config and surfaces a message rather than crashing. No dialog yet — the
store is hand-editable, and this delivers the core "no env var needed" win
end-to-end.

See `../spec.md` §1–§2 for the settled detail; `docs/adr/0006-settings-store-as-json.md`
for the store rationale.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] A `settings.py` module provides a versioned `SettingsDict` (all keys
  optional), a pure `settings_path()` resolving to `~/.config/toolbox/settings.json`
  (unaffected by `TOOLBOX_CONFIG`), and `load_settings()`/`save_settings()` that
  return `{}` on a missing or corrupt file and support load-modify-write.
- [ ] `config_path` gains a third pure parameter for the setting-derived path;
  precedence is `TOOLBOX_CONFIG` (file or dir) › `settings.json` `config_path`
  (file only) › default `~/.config/toolbox/config.json`.
- [ ] A saved `config_path` that is gone/invalid falls back to the default Config,
  surfaces a message, does not crash, and does not wipe the setting; a corrupt
  `settings.json` falls back to all-defaults.
- [ ] Pure-seam unit tests cover `config_path` precedence (all three cases),
  `settings_path`, and `load_settings` on missing/corrupt files; existing tests
  are updated for the new `config_path` signature.
- [ ] The README Configuration section notes selecting the Config via
  `settings.json` and that `TOOLBOX_CONFIG` overrides it.
