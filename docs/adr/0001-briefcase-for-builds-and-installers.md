# Briefcase for builds and installers

We package Toolbox with **Briefcase (BeeWare)** rather than the previous
PyInstaller + `build_win.bat` setup. Toolbox now targets native installers on
Windows (`.msi`), macOS (`.dmg`), and Linux (AppImage); Briefcase produces all
three from one `[tool.briefcase]` configuration and models signing/notarization
as declared config, whereas PyInstaller only builds the binary and would require
bolting on a separate per-OS installer tool (Inno Setup, create-dmg, etc.).

## Considered Options

- **PyInstaller + per-OS installer tooling** — keeps the existing working
  Windows build, but means bespoke glue per platform and no built-in signing
  story. Rejected in favour of one cross-platform tool ahead of a future public
  release.

## Consequences

- macOS `min_os_version` must be set to **13.0** to match the PySide6 6.11
  universal2 wheel floor, or Briefcase refuses to resolve the wheel.
- Signing/notarization are stubbed and guarded (builds ship unsigned) until code
  signing certs are available; enabling them is then a config change, not a
  rewrite.
