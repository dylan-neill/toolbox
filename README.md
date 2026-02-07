# Toolbox

Toolbox is a small Qt desktop app for launching DCC tools through Rez package environments.

## Architecture

- `toolbox/__main__.py`: canonical app entrypoint (`python -m toolbox`).
- `toolbox/ui/`: Qt UI layer.
  - `toolbox/ui/main_window.py`: main window and UI event handling.
  - `toolbox/ui/widgets/tool_widget.py`: tool-card list item widget.
- `toolbox/services/`: infrastructure and domain-adjacent services.
  - `toolbox/services/config_store.py`: config persistence interfaces and JSON file implementation.
  - `toolbox/services/tool_repository.py`: toolset loading/updating from config data.
  - `toolbox/services/launcher.py`: cross-platform launch command building and process start.
- `toolbox/resources.py`: resource paths and runtime command helpers.

## Run

```bash
python -m toolbox
```

Launcher scripts in `bin/` also call the canonical module entrypoint.

## Development Workflow

1. Create a virtual environment and install dev deps (pytest, ruff, mypy).
2. Run tests:

```bash
pytest
```

3. Run lint:

```bash
ruff check .
```

4. Run type checks:

```bash
mypy
```

## Compatibility

- Config schema remains backward-compatible with existing `config.json` files.
- Python target is `3.11+`.
