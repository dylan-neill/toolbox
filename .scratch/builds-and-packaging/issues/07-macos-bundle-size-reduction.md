# 07: macOS bundle size reduction

**What to build:** The macOS installer ships the Qt that Toolbox actually uses
instead of the whole framework, so the `.dmg` is a ~50 MB download rather than
~420 MB. Toolbox imports only QtCore/QtGui/QtWidgets and renders `.svg` icons, so
the bundle keeps that widgets stack (plus QtSvg + the `qsvg` image plugin and
QtDBus) and strips the rest — QtWebEngine's Chromium, QML/Quick, the Qt developer
tools — and builds arm64-only. Because the trim is coupled to Qt's bundle layout,
CI must launch the packaged app, not just build it, so a broken trim fails the
pipeline. See ADR 0004.

**Blocked by:** 05, 06

**Status:** done

- [x] Runtime dependency is `PySide6-Essentials` (the `PySide6-Addons` wheel — QtWebEngine, Charts, Qt3D, Graphs — is no longer bundled)
- [x] Briefcase `cleanup_paths` strips the QML/Quick stack, the Qt developer tools, and unused frameworks/bindings, keeping QtCore/QtGui/QtWidgets/QtSvg/QtDBus
- [x] `.svg` icons still render in the packaged bundle (a blank icon does not crash a launch, so this is verified by rendering, not just a clean start)
- [x] The macOS build is arm64-only (`universal_build = false`); Intel is no longer a target (ADR 0004)
- [x] The macOS `.app`/`.dmg` are materially smaller: 188 MB `.app` / 50 MB `.dmg`, down from 1.3 GB / 421 MB. A 300 MB `.app` ceiling in CI guards against reinflation.
- [x] The CI `build` job smoke-launches the built macOS `.app` headless (`QT_QPA_PLATFORM=offscreen`) so a trim that hides a needed framework fails the workflow (see limitation note below)
- [x] ADR 0004 records the decision and its revision of ADR 0001's universal2 stance

## Comments

Known limitation (by design, not a gap to fix here): the bundle smoke-test and
size ceiling live in the CI `build` job, which ticket 06 gates to tagged releases
(`if: startsWith(github.ref, 'refs/tags/')`). So a pull request that regresses
`cleanup_paths` is not caught until a release is cut, not at PR time. Moving the
guard earlier would mean building the macOS bundle on every PR (a multi-minute
`briefcase create` that downloads the Qt support package), which contradicts
ticket 06's deliberate "installers build only on a tagged release" decision.
Revisit if trim regressions actually slip through: a cheaper PR-time guard could
run `briefcase create macOS` (which applies `cleanup_paths`) + the render check
without the full `build`/`package`.

Local-env gotcha: swapping the full `PySide6` metapackage for `PySide6-Essentials`
*in place* leaves the venv broken — `uv` deletes `PySide6/__init__.py` (owned by
both wheels) when it uninstalls the metapackage, so `PySide6.__version__`
disappears and pytest-qt errors on collection. Fix locally with
`uv sync --reinstall-package pyside6-essentials`. A clean install (as CI does)
is unaffected.

The smoke-test launches the *built* `.app` (before `briefcase package`) rather
than the packaged `.dmg`. `cleanup_paths` is applied at `briefcase create`, so
the trim is already present in the built bundle; testing there fails faster
(before packaging) and is equivalent for what this guards.
