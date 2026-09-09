# 01: Project foundation — uv, src/ layout, test scaffolding

**What to build:** A contributor can clone the repo, run `uv sync`, and launch Toolbox with `uv run toolbox` — with dependencies managed by uv instead of the old `requirements.txt`. `uv run pytest` runs a green suite that already contains one headless smoke test proving the main window constructs. This is the foundation every other ticket builds on.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] `pyproject.toml` exists with the hatchling backend and `requires-python = ">=3.11,<3.15"`
- [ ] Runtime dependency `PySide6>=6.11.2`; `pywin32` declared with a `sys_platform == 'win32'` marker
- [ ] A `dev` dependency group carries `briefcase`, `pytest`, and `pytest-qt`
- [ ] `uv.lock` is committed; the UTF-16 `requirements.txt` is removed
- [ ] The package lives under `src/toolbox/` and the app's `main()` is in `src/toolbox/__main__.py`
- [ ] A `toolbox` GUI entry point launches the app via `uv run toolbox`
- [ ] `uv run pytest` passes, including one pytest-qt smoke test (Seam E) that constructs the main window under `QT_QPA_PLATFORM=offscreen`
- [ ] Existing launch behaviour on the current dev platform is unchanged
