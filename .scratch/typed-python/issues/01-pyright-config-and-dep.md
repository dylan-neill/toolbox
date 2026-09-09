# 01 — Add pyright as a dev dependency and configure it

Status: ready-for-agent

Add `pyright` to `[dependency-groups].dev` in `pyproject.toml` (pinned) so
`uv run pyright` is identical locally and in CI.

Add a `[tool.pyright]` table: `include = ["src", "tests"]`,
`pythonVersion = "3.11"` (the `requires-python` floor), `typeCheckingMode =
"strict"`. The Qt/OS-boundary relaxations are applied as per-file `# pyright:`
comments in issue 03, not here — this table sets the strict baseline.
