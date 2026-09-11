![readme-screenshot](https://github.com/user-attachments/assets/40c68a23-2694-47b1-b7f5-fd3f1dc1eab3)

# Toolbox

Toolbox is a DCC software launcher aimed at 3D animation and visual effects production. It uses industry standard Rez packages for environment and version configurations

## Features

- Toolset picker for grouping launch presets by project or purpose (ie testing, development etc).
- Straightfoward icon grid of configured applications.
- Detail panel showing Rez package configuration.
- Open Shell button for opening a command prompt with the select Rez environment.
- Windows desktop shortcut creation for Rez environments.
- Builds to native installers on Windows, macOS, and Linux with Briefcase.

## Requirements

- Windows, macOS, or Linux. The launcher runs on all three from source.
- Python 3.11 through 3.14.
- [uv](https://docs.astral.sh/uv/) for dependency management and running.
- Rez installed and available on `PATH` as `rez-env`.

Dependencies are declared in `pyproject.toml` and locked in `uv.lock`; `uv` installs everything (including a matching Python) from those — there is no `requirements.txt`.

## Running from source

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then from the repository root:

```bash
uv sync
uv run toolbox
```

`uv sync` creates a virtual environment and installs the locked dependencies; `uv run toolbox` launches the app (equivalent to `python -m toolbox`).

## Configuration

On first launch, Toolbox creates a config file at (`~` is `%USERPROFILE%` on Windows):

```text
~/.config/toolbox/config.json
```

The default config is seeded from the bundled `example_config.json` (shipped as package data inside `src/toolbox/resources/`, so it resolves from a source checkout and from an installed build alike).

You can point Toolbox at a specific config file or config directory with the `TOOLBOX_CONFIG` environment variable:

```bash
TOOLBOX_CONFIG=/path/to/config.json uv run toolbox
```

```powershell
$env:TOOLBOX_CONFIG = "C:\path\to\config.json"
uv run toolbox
```

If `TOOLBOX_CONFIG` points to a directory, Toolbox will look for `config.json` inside that directory.

### Selecting the config file without an environment variable

Toolbox also reads an app-level **settings** file at (`~` is `%USERPROFILE%` on Windows):

```text
~/.config/toolbox/settings.json
```

Set its `config_path` to select which config file to load — no `TOOLBOX_CONFIG` needed:

```json
{
  "version": 1,
  "config_path": "/abs/path/to/config.json"
}
```

Resolution precedence is: the `TOOLBOX_CONFIG` environment variable (which **overrides** the saved `config_path`) → the `settings.json` `config_path` → the default `~/.config/toolbox/config.json`. If the saved `config_path` points at a file that no longer exists, Toolbox falls back to the default config, reports it, and leaves the setting in place (a network drive may be transiently absent). The settings file is optional — with none present, Toolbox behaves exactly as before — and is not created until a setting is saved.

### Config format

Each config file contains `toolsets`. Each toolset contains a list of `tools` ie Rez environments with launchable applications. The bundled `src/toolbox/resources/example_config.json` file contains more example tool setups.

```json
{
  "toolsets": [
    {
      "name": "Production",
      "tools": [
        {
          "name": "Maya",
          "version": "2025",
          "desc": "Redshift 2025.2",
          "rez_wants": ["maya-2025", "redshift-2025.2", "site_tools", "site_ocio"],
          "command": "maya",
          "icon": "maya_icon.png"
        }
      ]
    }
  ]
}
```

Toolbox builds the launch command from the `rez_wants` and `command` fields:

```text
rez-env maya-2025 redshift-2025.2 site_tools site_ocio -- maya
```

The `icon` field names a file bundled under `src/toolbox/resources/icons`.

## Testing

The test suite covers the launcher's pure logic (launch-command construction, config-path resolution, config parsing, asset resolution) plus a headless GUI smoke test. Run it with:

```bash
uv run pytest
```

The GUI test runs headless via `QT_QPA_PLATFORM=offscreen`, so no display is required. GitHub Actions runs the full suite on Windows, macOS, and Linux for every push and pull request.

## Building installers

Toolbox is packaged with [Briefcase](https://briefcase.readthedocs.io/), which produces a native installer for the platform you build on: a Windows `.msi`, a macOS `.dmg` (macOS 13+), or a Linux AppImage. All three are configured under `[tool.briefcase]` in `pyproject.toml`. Build on the target OS:

```bash
uv run briefcase create
uv run briefcase build
uv run briefcase package
```

The installer is written to `dist/`. On a tagged release, GitHub Actions builds all three automatically and uploads them as artifacts.

The macOS build is **Apple-silicon only** (arm64) and trims Qt down to the modules Toolbox actually uses, so the installer is ~50 MB rather than ~420 MB (see `docs/adr/0004-macos-bundle-size-reduction.md`). Intel Macs are no longer a build target; flip `universal_build = true` in `pyproject.toml` to restore a universal2 build.

Builds currently ship **unsigned**. On macOS, package with an ad-hoc identity so the build succeeds without a code-signing certificate:

```bash
uv run briefcase package macOS --adhoc-sign
```

Signing and notarisation are otherwise left to CLI/CI flags (an `--identity`, an Apple team id) — enabling them later is a configuration change, not a rebuild of the packaging setup.

The macOS app icon (`src/toolbox/resources/icons/app_icon.icns`) is generated from the 512px master PNG by `bin/make_icns.sh` (macOS only).

An installed Toolbox still depends on the workstation environment for Rez and the configured application commands: make sure `rez-env` and any launched tools are available from the environment where Toolbox is started.

## Project Layout

```text
src/toolbox/__main__.py       Application entry point (uv run toolbox)
src/toolbox/ui.py             PySide6 user interface and launch actions
src/toolbox/data.py           Config parsing into Tool/ToolSet models (seam C)
src/toolbox/settings.py       App-level settings store (settings.json; ADR 0006)
src/toolbox/model.py          Tool and ToolSet dataclasses
src/toolbox/util.py           Windows desktop-shortcut creation
src/toolbox/globalvars.py     App name and version
src/toolbox/resources/        Bundled assets + pure seams: config_path (seam B),
                              launch_command (seam A), shell_command (Open Shell),
                              asset accessors (seam D)
src/toolbox/resources/example_config.json  Default toolset config (seed for a new user Config)
src/toolbox/resources/icons   Application and Toolbox icons
tests/                        pytest suite (pure-logic tests + headless smoke test)
bin/make_icns.sh              Regenerate the macOS .icns from the master PNG
bin/verify_macos_bundle.py    CI check that a trimmed macOS bundle renders icons
pyproject.toml                Project metadata, dependencies, Briefcase config
.github/workflows/ci.yml      Test matrix + tagged-release installer builds
```

## Notes

There are multiple UI elements that are disabled which are placeholders for future features.
