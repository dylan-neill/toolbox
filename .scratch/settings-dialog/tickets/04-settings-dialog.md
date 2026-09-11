# 04: Settings dialog

**What to build:** Clicking the gear opens a modal **Settings** dialog. It has a
Config-file row (shows the current path, **Browse** to pick an existing `.json`,
**Clear** to revert to the default, and a note when `TOOLBOX_CONFIG` is currently
overriding the selection) and an **Open Shell terminal** row (a dropdown of the
OS's terminals plus **Custom**, which reveals program/arguments fields). **OK**
saves the settings and, if the Config path changed, live-reloads the grid;
**Cancel** discards. This is the UI face of the two settings wired in tickets 01
and 02.

See `../spec.md` §4 (dialog layout).

**Blocked by:** 02 (terminal registry for the dropdown + save), 03 (gear button +
`reload_config()`)

**Status:** ready-for-agent

- [ ] The gear opens a modal "Settings" dialog with a Config-file row (current
  path, Browse for an existing `.json`, Clear to default) and an Open Shell
  terminal row (predefined dropdown + Custom program/arguments fields).
- [ ] When `TOOLBOX_CONFIG` is set, the dialog shows a note that the environment
  variable is overriding the config selection.
- [ ] OK writes `config_path`, `terminal_id`, and `terminal_command` via
  load-modify-write; if `config_path` changed, `reload_config()` runs so the grid
  updates immediately. Cancel writes nothing.
- [ ] The README Configuration section documents the Settings dialog.
