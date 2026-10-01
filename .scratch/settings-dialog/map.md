# Settings dialog & config selection

<!-- wayfinder:map -->

## Destination

A spec at `.scratch/settings-dialog/spec.md` (plus the decisions it rests on),
ready to hand to an implementation session. The spec describes a **Settings**
feature for Toolbox: a persisted app-level settings store and a settings dialog
that lets the user pick which Config file to load (so setting the
`TOOLBOX_CONFIG` env var is no longer required on GUI-only machines), choose the
terminal used by *Open Shell*, with window geometry and last-selected toolset
persisted silently (no UI), live Config reload, and a gear + refresh control in
the main window.

Planning only: this map produces the spec and the decisions behind it. The build
is the next session, not part of this map.

## Notes

**Domain**: single-context repo — `CONTEXT.md` + `docs/adr/` at root. The glossary
currently reserves **"Config"** for the toolsets file and lists "Settings,
preferences" under _Avoid_; this effort deliberately promotes **"Settings"** to a
canonical term for app-level state, so the glossary must be reconciled (see the
domain ticket).

**Skills every session should consult**: `grilling` + `domain-modeling` for the
HITL decision tickets; `research` for the terminal ticket. Read `CONTEXT.md` and
`docs/adr/0003-user-config-location.md` before touching config-path logic.

**Framing decisions already locked (during charting, before any ticket):**

- Destination is a **spec handoff**, not a build.
- Canonical term for app-level state is **"Settings"** (dialog = "Settings").
- **In scope**: (1) Config-file selection [UI], (2) terminal for *Open Shell*
  [UI, OS-dependent dropdown + Custom], (3) window geometry [persisted, no UI],
  (4) last-selected toolset [persisted, no UI].
- **Store**: hand-rolled **JSON at `~/.config/toolbox/settings.json`**, beside
  `config.json`, honoring ADR 0003 (one location on every OS). Not `QSettings`.
- **Precedence**: `TOOLBOX_CONFIG` env (file or dir) › saved Setting (file only)
  › default `~/.config/toolbox/config.json`.
- **Reload**: live repopulate when the Config selection is saved, **and** a
  refresh control for re-reading an externally edited Config.
- **Entry points**: a **gear icon** (opens Settings) and a **refresh button**,
  top-right above the icon grid. **No menu bar** for now.
- **Terminal lists**: macOS = Terminal, iTerm2, Ghostty; Windows = Windows
  Terminal, cmd, PowerShell; Linux = gnome-terminal, konsole, xterm; plus a
  **Custom** free-text command on every OS.

## Decisions so far

<!-- index: one line per resolved ticket, gist + link; detail lives in the ticket -->

- [Author the Settings spec](issues/06-author-settings-spec.md): the destination
  — `spec.md` written, consolidating all five decisions (store, config
  resolution, terminal wiring, dialog, main-window, docs/tests) with scope and a
  Ghostty verification task. **Map complete; ready to hand off for
  implementation.**
- [Live reload, entry points & persistence](issues/05-reload-entry-points-persistence.md):
  a top bar above the grid holds the Toolsets combo + refresh (`SP_BrowserReload`)
  + gear (bundled icon) buttons; one `reload_config()` (refresh + post-save) that
  catches errors, logs, and keeps the current grid rather than crashing; reload
  preserves the current toolset by name (launch restores the `last_toolset`
  setting); geometry saved on `closeEvent`, `last_toolset` saved on change (both
  load-modify-write; guard the on-change save against programmatic combo updates).
- [Terminal setting → Open Shell wiring](issues/04-terminal-setting-open-shell-wiring.md):
  a data-driven per-OS terminal registry maps `terminal_id` → `(program,
  args-template)`; `shell_command` becomes
  `shell_command(system, rez_tokens, terminal_id, custom_command=None)`, pure,
  with a `{command}` placeholder inserted joined or expanded per template. Custom
  = a `{program, args}` object (refines 03's `terminal_command` shape). Unset =
  today's per-OS default byte-for-byte; full list + Custom offered, no install
  detection; Ghostty kept via CLI binary (**verify on-device** — spec task); no
  keep-open flags.
- [Settings store & config resolution](issues/03-settings-store-and-config-resolution.md):
  flat versioned `settings.json` (`config_path`, `terminal_id`/`terminal_command`,
  base64 `window_geometry`, `last_toolset`; all keys optional); a dedicated
  `settings.py` module owns it; `config_path` gains a pure third param
  `setting_config_path` with precedence env › setting (file) › default; missing
  file = defaults (no seed), invalid config path falls back + logs + keeps the
  setting. ADR 0006 records the JSON-not-QSettings choice.
- [Settings domain model & CONTEXT.md](issues/02-settings-domain-model.md):
  **Settings** = app-level state (which Config to load, the terminal it opens
  shells in, + silent no-UI values: window geometry, last Toolset); one entry =
  "a setting"; stored in `settings.json` beside the Config. *Settings configure
  the app; Config defines what to launch.* "Preferences" stays avoided.
  `CONTEXT.md` updated with the new entry + reciprocal Avoid guards.
- [Terminal launch invocations](issues/01-terminal-launch-invocations.md): the
  `(program, [args])` form for each terminal (macOS Terminal/iTerm2/Ghostty,
  Windows wt/cmd/PowerShell, Linux gnome-terminal/konsole/xterm); rez-env alone
  gives the interactive shell (no wrapper); Ghostty on macOS needs its
  AppleScript route or bundle binary (`-e` via `open` fails — verify on-device);
  Custom needs a `{command}` placeholder, not free text. Full findings on branch
  `research/terminal-launch-invocations`.

## Not yet specified

<!-- in-scope fog too dim to ticket yet; graduates as the frontier advances -->

_(none — the seeding/migration question was answered within Settings store &
config resolution: no seed, lazy write; migration caveat recorded in ADR 0006.)_

## Out of scope

<!-- ruled beyond the destination; never graduates -->

- **rez-env command/path as a setting** — a launch-behavior change; its own effort.
- **Theme / appearance setting** — a visual overhaul, not app plumbing.
- **`QSettings` / native per-OS storage** — reopens ADR 0003; rejected in favor
  of the single `~/.config/toolbox/` JSON store.
- **Menu bar (with a standard Settings item / ⌘,)** — deferred; entry is the
  gear + refresh controls instead. May return as a later effort.
