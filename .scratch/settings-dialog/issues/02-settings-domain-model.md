# 02 — Settings domain model & CONTEXT.md reconciliation

Type: grilling
Status: resolved
Blocked by: none

## Question

Fix the vocabulary this feature introduces, and reconcile it with the existing
glossary, so every downstream ticket and the spec use settled terms.

`CONTEXT.md` today reserves **"Config"** for the user's toolsets file and lists
"Settings, preferences" under _Avoid_. This effort promotes **"Settings"** to a
canonical term. Resolve:

- What exactly does **"Settings"** name — the on-disk store, the concept of
  app-level state, or both? Is one entry a **"setting"**?
- How do **Settings** and **Config** relate in one sentence (Settings choose,
  among other things, *which* Config to load)?
- Terms for the two silent (no-UI) persisted values — "window geometry" and
  "last-selected toolset" — do they need glossary entries or are they self-evident?

Then update `CONTEXT.md`: add the **Settings** entry, amend the **Config** entry's
_Avoid_ line (it can no longer blanket-ban "Settings"), and keep `CONTEXT.md` a
pure glossary (no implementation detail). This is a domain-modeling pass — call
the `domain-modeling` and `grilling` skills.

## Answer

Canonical vocabulary settled and written into `CONTEXT.md`:

- **Settings** = the app-level state Toolbox keeps for *itself* (which Config to
  load, the terminal it opens shells in, and silently-persisted values with no
  UI: window geometry, last-selected Toolset). **One entry = "a setting."** The
  file is **the Settings file** (`settings.json`), beside the Config in
  `~/.config/toolbox/`.
- **Relationship**: *Settings configure the app itself — including which Config
  it loads; Config defines the Toolsets and Tools the app launches.*
- The two silent values get **no separate glossary entries** — the Settings
  entry names them as examples of no-UI persisted settings.
- **Reciprocal _Avoid_ guards**: the **Config** entry now avoids "Settings,
  Preferences (those name the app-level Settings)"; the new **Settings** entry
  avoids "Preferences, Config." **"Preferences" stays avoided** as a synonym for
  Settings ("Settings" is canonical, even though the dialog opens via a gear, not
  a Preferences menu).

`CONTEXT.md` edited: **Config** _Avoid_ line reframed and a new **Settings** entry
added (kept to a pure glossary — no dialog/precedence/implementation detail; that
lives in the spec). No ADR — a glossary reconciliation, not a hard-to-reverse
trade-off.
