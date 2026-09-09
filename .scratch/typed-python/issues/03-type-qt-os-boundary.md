# 03 — Type the Qt/OS boundary and apply graded relaxation

Status: ready-for-agent

Annotate `ui.py`, `globalvars.py`, `__main__.py`, `util.py`. Apply the relaxed
profile as per-file `# pyright:` header comments (only the rules PySide6's stubs
force — e.g. `reportUnknownMemberType`, `reportUnknownArgumentType`,
`reportAttributeAccessIssue`), keeping the exemption scoped and visible per
[ADR 0005](../../docs/adr/0005-pyright-graded-strict-typing.md).

Correctness fixes the checker surfaces (do not paper over with ignores):

- `ui.py` `set_defaults`: `setGeometry` takes ints — wrap the centred `pos_x`/
  `pos_y` in `int(...)`.
- Remove `update_packages` (unconnected, and broken: Python-2 `.iteritems()`;
  superseded by the inline table build in `update_tool_info`).
- `__main__.py` / `util.py`: guard Windows-only code (`ctypes.windll`,
  `win32com`) with `sys.platform == "win32"` so pyright narrows it; targeted
  ignore on the stub-less `win32com` import.

Keep `update_proc_log` / `process_cleanup` (unwired scaffolding) — typed, not
removed.
