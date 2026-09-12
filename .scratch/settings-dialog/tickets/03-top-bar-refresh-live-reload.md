# 03: Top bar, refresh & live config reload

**What to build:** The main window gains a top bar above the icon grid holding the
Toolsets selector plus a **refresh** button and a **gear** button. Refresh
re-reads the current Config live — picking up an externally edited file — and
rebuilds the grid without a restart. A broken Config on reload logs a message and
leaves the current grid intact rather than blanking or crashing, and the selected
toolset is preserved across a reload. The gear button is present here but opens
the Settings dialog built in ticket 04 (inert until then).

See `../spec.md` §5 (entry points, reload action, selection preservation).

**Blocked by:** 01 (reload re-resolves the config path via the store/resolution)

**Status:** done

- [x] A top bar sits above the icon grid: Toolsets combo on the left, refresh and
  gear buttons right-aligned, with a bundled gear icon (`resources/icons`), Qt's
  reload pixmap for refresh, and "Reload config" / "Settings" tooltips.
- [x] Refresh calls a `reload_config()` that re-resolves and re-reads the Config
  and rebuilds the grid; an external edit is reflected without restarting.
- [x] A read/parse error during reload is caught, logged to the log pane, and
  leaves the currently-loaded toolsets displayed — the grid never blanks and the
  app never crashes.
- [x] The selected toolset is preserved by name across a reload; if it no longer
  exists, selection falls back to the first toolset.
