# 05 — Add a blocking typecheck job to CI

Status: ready-for-agent

Add a `typecheck` job to `.github/workflows/ci.yml`: single runner
(`ubuntu-latest`, uv with Python 3.12), `uv sync`, `uv run pyright`. Type
results are OS-independent, so it does not run on the 3-OS matrix.

It runs on every push and pull request (like `test`) and is blocking — a type
error fails the workflow. Leave the existing `test` and tag-gated `build` jobs
unchanged.
