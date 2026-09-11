# 02: Terminal selection & Open Shell wiring

**What to build:** *Open Shell* opens the terminal the user chose in Settings. A
`terminal_id` in `settings.json` selects among the per-OS terminals; leaving it
unset reproduces today's terminal exactly (zero change for existing users); a
Custom entry runs a user-provided command template. No dialog yet — driven by the
hand-edited store; the dropdown that exposes this arrives in ticket 04.

See `../spec.md` §3 and the research note on branch
`research/terminal-launch-invocations` (exact per-terminal `(program, args)` and
hazards).

**Blocked by:** 01 (needs the `settings.py` store)

**Status:** done

- [x] A data-driven per-OS registry maps `terminal_id` to a `(program,
  args-template)` pair; `shell_command` takes the rez invocation as **tokens** +
  `terminal_id` (+ optional `custom_command`) and returns `(program, args)`.
  (`src/toolbox/terminals.py` registry; `resources.shell_command` seam.)
- [x] Unset `terminal_id` reproduces today's *Open Shell* command **byte-for-byte**
  on each OS (regression-tested against the current behaviour).
  (`tests/test_open_shell.py` default-* cases.)
- [x] Each predefined terminal produces the invocation from the research note
  (macOS Terminal/iTerm2/Ghostty; Windows Windows Terminal/cmd/PowerShell; Linux
  gnome-terminal/konsole/xterm); the `{command}` placeholder inserts as a joined
  single token or expanded argv tokens per the template. (`{command}` = argv
  tokens / joined-when-embedded; `{command_str}` = joined single token for
  PowerShell's `-Command`.)
- [x] Custom (a `{program, args}` object) substitutes `{command}` correctly; tests
  cover both insertion modes.
- [x] **Ghostty on macOS is smoke-tested on a real install**: the CLI-binary
  `-e` route (`…/Ghostty.app/Contents/MacOS/ghostty -e …`) opens a window and
  runs the command; no AppleScript fallback needed. Verified 2026-09-11.
