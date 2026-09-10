# 01 — Terminal launch invocations

Type: research
Status: resolved
Blocked by: none

## Question

For each terminal offered in the *Open Shell* setting, what is the exact
invocation that opens that terminal and runs a given command inside it (so the
`rez-env … ` shell starts in a live, interactive terminal window)?

Cover, per OS:

- **macOS**: Terminal.app, iTerm2, Ghostty
- **Windows**: Windows Terminal (`wt`), `cmd`, PowerShell
- **Linux**: gnome-terminal, konsole, xterm

For each, capture the `(program, arguments)` form (Toolbox launches via
`QProcess`, which only splits on double quotes with no escaping — see
`resources.shell_command`), noting any quoting/escaping hazards. Also determine
what a **Custom** option realistically needs: is a single free-text command
enough, or is a placeholder (e.g. the rez-env command to substitute in) required?

Anchor findings against the existing `shell_command` in
`src/toolbox/resources/__init__.py` (current hardcoded forms: macOS osascript
into Terminal, Windows `cmd /K`, Linux `gnome-terminal --`). Cite primary docs
(each terminal's CLI documentation).

## Answer

Full findings: `.scratch/settings-dialog/research/terminal-launch-invocations.md`
on branch **`research/terminal-launch-invocations`** (commit `c8f18a7`) — a
throwaway research branch, not merged to master. Check it out (or
`git show research/terminal-launch-invocations:.scratch/settings-dialog/research/terminal-launch-invocations.md`)
when working ticket 04.

Key facts:

- **Constraint**: *Open Shell* uses `QProcess.start(program, arguments)` (list
  overload — Qt does no further splitting), so every terminal must be expressed
  as `(program, [args])`. Windows extra hazard: QProcess builds a
  `CommandLineToArgvW`-style line, but `cmd.exe`/batch don't follow those rules
  and need `setNativeArguments()` (not currently called) — latent quoting
  mismatch for anything routed via cmd/start/wt.
- **rez gives the interactive shell for free**: `rez-env <wants>` with no
  `-- command` spawns an interactive subshell, so the string to run in the
  window is just `rez-env <wants…>` — no `-c`/`exec bash` wrapper. The three
  current `shell_command` defaults reproduce today's behavior and become the
  per-OS defaults.
- **Per terminal** (all cited to primary CLI docs): macOS — `osascript do script`
  (Terminal.app) / iTerm2 `create window … command`; **Ghostty is the problem
  child** — `-e` isn't honored via macOS `open`, and it's single-instance; use
  its AppleScript dictionary or the bundle binary `…/Ghostty.app/Contents/MacOS/ghostty -e …`
  (**flagged for on-device verification**). Windows — `wt new-tab cmd /k …`
  (`;` is a `wt` delimiter), `cmd /C start cmd /K …` (`start`'s first quoted
  token is the window title), `powershell -NoExit -Command …` (`-Command` must be
  last). Linux — `gnome-terminal -- …`, `konsole -e …` (+`--hold`), `xterm -e …`
  (+`-hold`); `-e` must be the last option for konsole/xterm.
- **Custom option needs a placeholder**, not plain free text: the rez-env command
  is built at launch from the Tool's `rez_wants`. Recommended shape is a
  `program` + `arguments` template list with a `{command}` placeholder, and a
  documented decision on whether it substitutes as one joined token (needed for
  osascript / `-Command`) or expands into argv tokens (needed for `--`/`-e`/`wt`)
  — a decision for ticket 04.
