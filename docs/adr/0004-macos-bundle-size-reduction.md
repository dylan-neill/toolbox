# macOS bundle size reduction: Essentials, trimmed Qt, arm64-only

The macOS `.dmg` produced by Briefcase was **421 MB** (a 1.3 GB `.app`), because
the full **PySide6** metapackage bundles all of Qt — including a ~590 MB
QtWebEngine (an embedded Chromium), plus QML/Quick, Qt3D, Charts, and the Qt
developer tools — and every binary carried both `x86_64` and `arm64` slices.
Toolbox imports only **QtCore/QtGui/QtWidgets** and renders `.svg` icons.

We cut the macOS bundle to a **50 MB `.dmg`** (188 MB `.app`), ~8×, with three
changes:

- **Depend on `PySide6-Essentials`, not `PySide6`.** Drops the `PySide6-Addons`
  wheel wholesale (QtWebEngine, Charts, Qt3D, Graphs) — the single largest win.
- **Trim the rest of Qt with Briefcase `cleanup_paths`.** Essentials still ships
  the QML/Quick stack and the developer tools; keep only the widgets stack
  Toolbox loads — QtCore, QtGui, QtWidgets, **QtSvg** (with the `qsvg` image
  plugin, for `.svg` icons) and QtDBus — and strip the rest.
- **Build arm64-only** (`universal_build = false`), halving every remaining
  binary.

## Considered Options

- **Keep the full universal2 PySide6 build.** Simplest, and the only option that
  runs on Intel Macs, but ships a ~421 MB installer dominated by a browser engine
  the app never loads. Rejected: the size is user-visible and almost entirely
  waste.
- **Essentials + trim, but stay universal2.** Keeps Intel support at ~100 MB
  `.dmg`. Rejected because the studio's Mac fleet is Apple silicon; the x86_64
  slice is pure overhead.

## Consequences

- **Intel Macs are no longer a macOS target.** This revises ADR 0001, whose
  "macOS `.dmg`" targeted universal2 (Intel + Apple silicon). Reversing it is a
  one-line change (`universal_build = true`), so the door is not closed.
- `min_os_version = "13.0"` still holds (it matches the PySide6 6.11 wheel floor,
  arm64 or universal2 alike), so ADR 0001's floor is unchanged.
- **`cleanup_paths` is coupled to Qt's bundle layout.** A PySide6 upgrade could
  move a framework or add a load-bearing dependency edge and silently break the
  trim; a missing framework surfaces only at runtime, not at build time. CI must
  therefore **launch the packaged bundle**, not just build it, so a bad trim
  fails the pipeline (see the builds-and-packaging effort, ticket 07).
- Windows and Linux are untouched: they still install the full runtime declared
  in `[project].dependencies`, and their bundle size is out of this ADR's scope.
