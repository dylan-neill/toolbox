# 06 — Author the Settings spec

Type: task
Status: resolved
Blocked by: 01, 02, 03, 04, 05

## Question

Consolidate every resolved decision into `.scratch/settings-dialog/spec.md` — the
destination artifact, ready to hand to an implementation session.

Not a fresh decision: this ticket assembles the answers from tickets 01–05 into
one coherent spec. It is blocked until all of them resolve. The spec should cover:

- The Settings concept and store (schema, location, precedence, edge cases) —
  from tickets 02 and 03.
- The Settings dialog: the Config-file picker row and the terminal dropdown
  (+ Custom) row, OK/Cancel behavior — layout described in prose (no prototype).
- *Open Shell* terminal wiring and per-OS defaults — from tickets 01 and 04.
- Main-window gear + refresh controls, live Config reload, selection
  preservation, and silent geometry / last-toolset persistence — from ticket 05.
- Any ADR(s) drafted along the way, and the CONTEXT.md changes.
- Out-of-scope reminders (rez command, theme, QSettings, menu bar) so the
  implementer doesn't wander past the destination.

Match the repo's existing spec shape (see `.scratch/typed-python/spec.md` and
`.scratch/builds-and-packaging/spec.md`).

## Answer

Spec authored at `.scratch/settings-dialog/spec.md`, consolidating all five
resolved decisions (Goal / Domain / Decisions in six areas — store, config
resolution, terminal wiring, dialog, main-window, assets+docs+tests / Scope /
Done when). Matches the repo's spec shape; links ADR 0006 and the research branch.
Carries the Ghostty-on-macOS on-device verification task into the Scope section
for the implementer. The map is now decision-complete and the destination reached
— hand `spec.md` to an implementation session.
