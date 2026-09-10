# 04 — Terminal setting → Open Shell wiring

Type: grilling
Status: open
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
