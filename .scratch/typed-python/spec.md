# Typed Python conversion

Convert Toolbox from effectively-untyped Python to a strictly type-checked
codebase, with a green type checker enforced in CI, and use the annotation pass
to tighten the domain model so bad states are hard to represent.

## Goal

- A type checker passes with **zero errors** and runs as a **blocking CI gate**.
- The annotation pass is also a modelling pass: overloaded primitives become
  precise types, and dead/half-built concepts are removed or made honest.

Decisions were reached in a grilling session; the rationale for the checker and
strictness choice is recorded in
[ADR 0005](../../docs/adr/0005-pyright-graded-strict-typing.md).

## Decisions

- **Checker: pyright.** Strongest on PySide6 (55% of the code), and what our
  editors already run. mypy is the fallback; ty is too pre-1.0 to gate CI on.
- **Strictness: graded.** Strict on the logic seams (`model.py`, `data.py`,
  `resources/`); a relaxed per-file profile on the Qt/OS boundary (`ui.py`,
  `globalvars.py`, and the Windows-only paths) for PySide6's under-typed
  signals/slots/overloads.
- **Config boundary: `TypedDict`.** Type the raw JSON Config shape as a
  `TypedDict`; keep the existing index-based parse and `KeyError` failure mode.
  No runtime-validation dependency.
- **`Job`: kept as recorded state.** `tool.job` (write-only dead code) is
  removed; `ToolSet.job` stays as `str | None`; the glossary is corrected to stop
  claiming launch behaviour the code never had.
- **Dead code:** the unused module global `apps` and the broken, superseded
  `update_packages` method are removed.
- **CI: separate blocking `typecheck` job**, one runner (Ubuntu, 3.12), parallel
  to `test`. Type results are OS-independent, so it does not run on the matrix.
- **Delivery: one green PR.**

## Scope

In scope: type annotations across `src/` and `tests/`; `TypedDict` config
schema; `job`/`apps`/`update_packages` cleanup; correctness fixes the checker
surfaces (`setGeometry` float→int, `sys.platform` guards); pyright config; CI
job; ADR + glossary.

Out of scope: wiring `Job` into the launch invocation (a feature); adding a
linter; refactoring the Qt UI beyond what typing requires. `update_proc_log` and
`process_cleanup` are unwired process-output scaffolding — typed and kept, not
built out.

## Done when

`uv run pyright` is clean, `uv run pytest` is green on all three OSes, and both
run in CI with typecheck blocking.
