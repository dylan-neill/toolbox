# 04 — Terminal setting → Open Shell wiring

Type: grilling
Status: resolved
Blocked by: 01, 03

## Question

Decide how the chosen terminal setting turns into the *Open Shell* invocation.

Given the invocation facts from **Terminal launch invocations** (ticket 01) and
the terminal key in the store schema (ticket 03), specify:

- How the predefined choice (per-OS dropdown) and the **Custom** free-text option
  each resolve into `shell_command`'s `(program, arguments)` return.
- The **default** terminal per OS when the setting is unset — must reproduce
  today's behavior byte-for-byte (macOS Terminal via osascript, Windows `cmd /K`,
  Linux `gnome-terminal --`) so existing users see no change.
- Where the mapping lives: does `shell_command(system, rez_command)` gain the
  terminal choice as a parameter (staying a pure, unit-tested seam), and how is
  the Custom command templated with the rez-env command.
- The dropdown's contents are OS-specific — confirm the presented list per OS and
  how an unavailable/uninstalled terminal is handled (offer anyway vs detect).

Call `grilling`. This ticket decides behavior only; the dialog row that exposes
the dropdown is described in the spec (ticket 06).

## Answer

Grounded in the research findings (branch `research/terminal-launch-invocations`).

**Registry + seam** — a **data-driven registry** (table keyed by `terminal_id`,
grouped per OS) maps each terminal to a `(program, args-template)` pair; it lives
with the terminal logic (`settings.py` or a small `terminals.py`).
`shell_command` stays a **pure seam** but its signature changes to
`shell_command(system, rez_tokens, terminal_id, custom_command=None)` and returns
`(program, [args])` from the table. It takes the rez invocation as **tokens**
(`["rez-env", "A", "B"]`), not today's pre-joined string, so a template can
insert them either way (below).

**Substitution model** — a **`{command}` placeholder** with two insertion modes
the template encodes: **joined single token** (osascript, PowerShell `-Command`)
vs **expanded argv tokens** (`--`, `-e`, `wt`). Covers every predefined terminal.

**Custom option** — stored as a small **`{program, args}` object** (args is a
list of argv-template elements; `{command}` as its own element expands to the rez
tokens), **not** a single free-text line — sidesteps QProcess's quote-only
tokeniser and matches the predefined entries' shape. This **refines ticket 03's
schema**: `terminal_command` holds this object (JSON) when `terminal_id ==
"custom"`, rather than a plain string.

**Defaults / contents / detection** — unset `terminal_id` → **today's per-OS
default, byte-for-byte** (macOS Terminal via osascript, Windows `cmd /C start …
/K`, Linux `gnome-terminal --`): zero change for existing users. Dropdown offers
the **full predefined list + Custom** with **no install detection** (an
uninstalled pick just fails and logs). Lists: macOS Terminal/iTerm2/Ghostty,
Windows Windows Terminal/cmd/PowerShell, Linux gnome-terminal/konsole/xterm.

**Ghostty & keep-open** — keep **Ghostty** in (requested at charting) via the
**direct CLI binary** (`…/Ghostty.app/Contents/MacOS/ghostty -e …`); the spec
must carry an **on-device verification task** — it's the one entry the research
couldn't confirm (`-e` fails via macOS `open`; single-instance focusing). **No
`--hold`/`-hold` flags** — windows close on shell exit, consistent with the
current defaults; note it as an easy later addition.
