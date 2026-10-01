# Pyright with graded strictness for type checking

We type-check Toolbox with **pyright in strict mode on the logic seams**
(`model.py`, `data.py`, `settings.py`, `terminals.py`, `resources/`) and a **relaxed profile on the Qt/OS
boundary** (`ui.py`, `globalvars.py`, and the Windows-only `util.py`/`__main__.py`
paths). A dedicated, blocking `typecheck` CI job runs `uv run pyright` on one
runner. The goal is not just annotations but a domain modelled so bad states are
hard to represent — hence full strictness where the real logic lives.

## Considered Options

- **mypy** — the reference implementation, but PySide6's bundled stubs are tuned
  for it yet still under-type signals/slots and suppress their own overload
  errors; and we already run pyright implicitly through every editor. Rejected in
  favour of the checker our editors already use.
- **ty (Astral)** — fits the uv toolchain but is pre-1.0; too green to gate CI on
  today. Revisit later.
- **Uniform strict everywhere** — rejected: PySide6 6.11's stubs leave signals,
  slots and many overloads under-typed, so blanket strict on the Qt-heavy `ui.py`
  produces noise that reflects stub gaps, not our bugs, and trains readers to
  ignore the checker.

## Consequences

- The relaxation on the Qt/OS boundary is expressed as per-file `# pyright:`
  rule overrides at the top of those files, not a global lowering. A future
  reader seeing `ui.py` exempt should read this ADR: the exemption is deliberate
  and scoped to the stub-driven rules, not a blanket "types don't matter here".
- Windows-only code (`win32com`, `ctypes.windll`) is guarded with
  `sys.platform == "win32"` (which pyright narrows on) rather than
  `platform.system()` (which it does not), so the cross-platform CI runner checks
  it cleanly. `win32com` ships no stubs, so its import carries a targeted ignore.
- The config boundary (`parse_config`) is typed against a `TypedDict` describing
  the expected Config shape. Its robustness tests deliberately pass malformed
  input to prove the `KeyError` contract, so those specific call sites carry a
  targeted `reportArgumentType` ignore.
