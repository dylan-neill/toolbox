<img width="1270" height="734" alt="readme-screenshot" src="https://github.com/user-attachments/assets/40c68a23-2694-47b1-b7f5-fd3f1dc1eab3" />

# Toolbox

Toolbox is a DCC software launcher aimed at 3D animation and visual effects production. It uses industry standard Rez packages for environment and version configurations

## Features

- Toolset picker for grouping launch presets by project or purpose (ie testing, development etc).
- Straightfoward icon grid of configured applications.
- Detail panel showing Rez package configuration.
- Open Shell button for opening a command prompt with the select Rez environment.
- Windows desktop shortcut creation for Rez environments.
- Can be built to a standalone .exe with PyInstaller

## Requirements

- Windows 10 or newer.
- Python 3.10 or newer.
- Rez installed and available on `PATH` as `rez-env`.
- Linux and MacOS should work but haven't been tested recently (but no build support).

Python package requirements are listed in `requirements.txt`.

## Installation on Windows

Open PowerShell in the repository root and create a virtual environment:

```powershell
py -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation scripts, allow scripts for the current user and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Install the Python dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run Toolbox from source:

```powershell
python toolbox.py
```

## Configuration

On first launch, Toolbox creates a config file at:

```text
%USERPROFILE%\.config\toolbox\config.json
```

The default config is copied from:

```text
resources\example_config.json
```

You can also point Toolbox at a specific config file or config directory with the `TOOLBOX_CONFIG` environment variable:

```powershell
$env:TOOLBOX_CONFIG = "C:\path\to\config.json"
python toolbox.py
```

If `TOOLBOX_CONFIG` points to a directory, Toolbox will look for `config.json` inside that directory.

### Config format

Each config file contains `toolsets`. Each toolset contains a list of `tools` ie Rez environments with launchable applications. The `resources/config_example.json` file contains more example tool setups.

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

Icons are loaded from:

```text
resources\icons
```

## Building a Windows EXE

Make sure the virtual environment is active and dependencies are installed:

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Build the executable with the included batch file:

```powershell
.\build_win.bat
```

This runs PyInstaller with the application icon and bundled `resources` folder:

```powershell
pyinstaller --add-data=".\resources;resources" --windowed --onefile --icon="resources/icons/app_icon48.ico" toolbox.py
```

After a successful build, the executable is created at:

```text
dist\toolbox.exe
```

You can run it directly:

```powershell
.\dist\toolbox.exe
```

The generated `.exe` still depends on your workstation environment for Rez and the configured application commands. Make sure `rez-env` and any launched tools are available from the environment where Toolbox is started.

## Project Layout

```text
toolbox.py                    Application entry point
toolbox\ui.py                 PySide6 user interface and launch actions
toolbox\data.py               Config loading into tool/toolset models
toolbox\model.py              Tool and ToolSet dataclasses
toolbox\resources.py          Config, icon, and command path helpers
resources\default_config.json Default toolset config
resources\icons               Application and Toolbox icons
build_win.bat                 Windows PyInstaller build command
toolbox.spec                  PyInstaller spec file
```

## Notes

There are a bunch of UI elements included that are disabled because they aren't implemented yet or haven't been maintained
