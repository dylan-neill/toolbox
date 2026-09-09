"""Verify a packaged macOS Toolbox.app renders .svg icons from its trimmed bundle.

ADR 0004 (ticket 07) trims the macOS bundle down to the Qt stack Toolbox actually
loads. A missing image-format plugin (``qsvg``) or the QtSvg framework would not
crash a launch — the icon would just render blank — so this asserts that a real
``.svg`` rasterises to visible pixels. Imports and Qt plugins are resolved against
the *bundle* (not the ambient environment) so the check exercises exactly what
ships.

Usage:
    python bin/verify_macos_bundle.py <path-to-Toolbox.app> <path-to-svg-icon>

Exits non-zero (failing CI) if the icon does not render.
"""

import os
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "usage: python bin/verify_macos_bundle.py <path-to-Toolbox.app> <path-to-svg-icon>",
            file=sys.stderr,
        )
        return 2
    app_path = Path(sys.argv[1])
    icon_path = sys.argv[2]
    pkg = app_path / "Contents" / "Resources" / "app_packages"
    plugins = pkg / "PySide6" / "Qt" / "plugins"

    # Resolve PySide6 and its Qt plugins against the trimmed bundle, before any
    # QApplication is constructed (Qt reads QT_PLUGIN_PATH as it loads plugins).
    sys.path.insert(0, str(pkg))
    os.environ["QT_PLUGIN_PATH"] = str(plugins)
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    import PySide6

    # The whole point is to exercise the bundle, so make sure PySide6 really
    # came from it and not from some ambient install on PATH.
    if not Path(PySide6.__file__).is_relative_to(pkg):
        print(f"FAIL: PySide6 resolved from {PySide6.__file__}, not {pkg}", file=sys.stderr)
        return 1

    from PySide6 import QtCore, QtGui, QtWidgets

    app = QtWidgets.QApplication([])  # held so it is not GC'd mid-render
    pixmap = QtGui.QIcon(icon_path).pixmap(QtCore.QSize(64, 64))
    image = pixmap.toImage()
    visible = not pixmap.isNull() and any(
        QtGui.qAlpha(image.pixel(x, y))
        for x in range(0, image.width(), 4)
        for y in range(0, image.height(), 4)
    )
    if not visible:
        print(f"FAIL: {icon_path} did not render from {app_path}", file=sys.stderr)
        return 1
    print(f"OK: {app_path.name} renders .svg icons from its trimmed bundle")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
