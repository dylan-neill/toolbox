# Toolbox

A launcher for DCC (Digital Content Creation) software used in 3D animation and
VFX production. It presents configured applications as an icon grid and launches
them inside versioned [Rez](https://rez.readthedocs.io/) environments.

## Language

**DCC**:
Digital Content Creation software — the artist applications Toolbox launches
(Maya, Houdini, Nuke, Blender, etc.). Toolbox itself is not a DCC; it is the
launcher in front of them.

**Tool**:
A single launchable entry — one DCC application at a specific version, bound to
a Rez environment and a launch command. The unit shown as one icon in the grid.
_Avoid_: App, application (reserve for the DCC software itself).

**Toolset**:
A named group of Tools, used to organise launch presets by project or purpose
(e.g. Production, Testing, Development). One toolset is shown at a time.
_Avoid_: Group, category, preset.

**rez_wants**:
The list of Rez package requests for a Tool (e.g. `["maya-2025", "redshift-2025.2"]`).
Joined with the launch command to form the `rez-env … -- <command>` invocation.
_Avoid_: Packages, dependencies, requirements (those are ambiguous with Python packaging).

**Job**:
An optional Rez context identifier recorded on a Toolset, tying that group of
launches to a specific production job. Read from Config and held on the Toolset;
recorded intent only — it is not yet applied to the launch invocation.

**Config**:
The user's `config.json` defining their Toolsets and Tools. Lives in the user's
home directory (`~/.config/toolbox/`), seeded from the bundled example on first
launch, and overridable via the `TOOLBOX_CONFIG` environment variable.
_Avoid_: Settings, Preferences (those name the app-level Settings — a different
thing; Config defines what to launch, Settings configure the app itself).

**Settings**:
The app-level state Toolbox keeps for itself — including which Config to load and
the terminal it opens shells in. Distinct from Config: Settings configure the app
itself; Config defines the Toolsets and Tools the app launches. One entry is a
setting. Some settings are persisted silently, with no place in the settings UI
(e.g. window geometry and the last-selected Toolset). Stored in the Settings file
(`settings.json`) in the user's home directory (`~/.config/toolbox/`), beside the
Config.
_Avoid_: Preferences, Config.
