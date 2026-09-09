# Spec: Builds and Packaging Modernisation

**Status:** ready-for-agent

## Problem Statement

Toolbox is a DCC launcher that today can only be developed and shipped as a
Windows tool. Dependencies are managed through a hand-maintained (and UTF-16
encoded) `requirements.txt`; the only build path is a one-line PyInstaller batch
file that produces a Windows `.exe`; there are no tests; and the application does
not actually run on macOS — the config-loading path has no darwin branch, so it
crashes on launch there. The maintainer wants a modern, reproducible dependency
workflow, real installers for Windows **and** macOS (with a view to a public
release later), and a test suite guarding the core logic.

## Solution

Modernise the project so that:

- Dependencies and environments are managed with **uv** (`pyproject.toml` +
  `uv.lock`), with runtime and dev/build dependencies separated.
- The application actually **runs on macOS and Linux**, not just Windows.
- The app builds to native **installers on Windows, macOS, and Linux** via
  **Briefcase**, unsigned for now but with signing/notarisation wired as guarded
  config for the eventual public release.
- A **pytest** suite covers the launcher's pure logic, backed by a headless GUI
  smoke test, and runs automatically in **GitHub Actions** alongside the
  installer builds.

The user-facing behaviour of the launcher (Toolsets, the Tool icon grid, the
Rez launch command, Open Shell) is unchanged; this work is about how Toolbox is
built, packaged, and verified.

## User Stories

1. As a maintainer, I want dependencies declared in `pyproject.toml` and locked
   in `uv.lock`, so that environments are reproducible across machines and CI.
2. As a maintainer, I want runtime dependencies separated from build/dev
   dependencies, so that an installed Toolbox does not carry PyInstaller/Briefcase
   or test tooling.
3. As a maintainer, I want `pywin32` declared only for Windows, so that macOS and
   Linux installs are not polluted by a Windows-only dependency.
4. As a maintainer, I want to run the app from source with a single command
   (`uv run toolbox`), so that onboarding a new contributor is trivial.
5. As a maintainer, I want the project to support Python 3.11 through 3.14, so
   that contributors and CI are not pinned to one interpreter.
6. As a maintainer, I want the UTF-16 `requirements.txt` removed, so that there is
   a single source of truth for dependencies.
7. As an artist on macOS, I want Toolbox to launch without crashing, so that I can
   use it at all.
8. As an artist on macOS, I want my Config stored in a predictable location
   (`~/.config/toolbox/`) consistent with other platforms, so that my Toolsets
   persist and behave the same as my colleagues' on Windows.
9. As an artist on macOS, I want the "Open Shell" action to open a terminal inside
   the selected Rez environment, so that I have the same shell access as on
   Windows and Linux.
10. As an artist, I want my existing Config at `~/.config/toolbox/` to keep working
    untouched after the upgrade, so that I do not lose my Toolsets.
11. As an artist, I want to point Toolbox at a specific Config via `TOOLBOX_CONFIG`,
    so that I can switch between configurations — exactly as before.
12. As an artist launching a Tool, I want Toolbox to build the correct
    `rez-env <rez_wants> -- <command>` invocation, so that the right DCC starts in
    the right Rez environment.
13. As a maintainer, I want the launch-command construction covered by unit tests,
    so that a regression in how Rez invocations are built is caught before release.
14. As a maintainer, I want config-path resolution covered by unit tests across all
    platforms and the `TOOLBOX_CONFIG` override, so that the macOS fix and the
    existing behaviour cannot silently regress.
15. As a maintainer, I want config parsing (dict → Toolsets/Tools) covered by unit
    tests, including malformed input, so that a bad Config fails predictably.
16. As a maintainer, I want a test proving bundled assets resolve, so that a
    packaging change that hides icons or the example Config is caught in CI rather
    than by a user.
17. As a maintainer, I want a headless smoke test that constructs the main window,
    so that gross startup breakage is caught without a display.
18. As a maintainer, I want to produce a Windows `.msi`, so that Windows users get
    a double-click install instead of a loose `.exe`.
19. As a maintainer, I want to produce a macOS `.dmg` that launches on macOS 13+,
    so that Mac artists can install and run Toolbox.
20. As a Linux artist, I want a portable AppImage, so that I can run Toolbox
    without a source checkout.
21. As a maintainer, I want the bundled app to find its icons and example Config at
    runtime whether run from source or from an installer, so that installed builds
    are not broken.
22. As a maintainer, I want installers to build unsigned today but with signing and
    notarisation as guarded, ready-to-enable steps, so that going public later is a
    configuration change rather than a re-architecture.
23. As a maintainer, I want the test suite to run on every push and pull request
    across Windows, macOS, and Linux, so that regressions surface immediately.
24. As a maintainer, I want the three installers built automatically on a tagged
    release, so that I do not need to keep build machines for each OS.

## Implementation Decisions

**Dependency management (uv).**
- Adopt `pyproject.toml` with the **hatchling** build backend and generate
  `uv.lock`. Remove `requirements.txt`.
- `requires-python = ">=3.11,<3.15"`.
- Runtime dependency: **`PySide6>=6.11.2`** (6.11 is the first series supporting
  Python 3.14 and ships a universal2 macOS wheel with a macOS 13.0 floor).
  `pywin32` declared with a `sys_platform == 'win32'` marker.
- A `dev` dependency group carries `briefcase`, `pytest`, and `pytest-qt`.

**Project layout (revised from a flat layout because Briefcase is the chosen
tool — see ADR 0001).**
- Move the package to `src/toolbox/`; move the `main()` currently in the
  top-level entry module into `src/toolbox/__main__.py`.
- Expose a `toolbox` GUI entry point so `uv run toolbox` launches the app.

**Cross-platform runtime.**
- Config-path resolution grows a **macOS branch using `~/.config`** (consistent
  with the other platforms and non-breaking for existing Windows users — see
  ADR 0003). `TOOLBOX_CONFIG` (file or directory) behaviour is preserved.
- The "Open Shell" action grows a **macOS branch** that opens a terminal inside
  the selected Rez environment (via `osascript` / `open -a Terminal`), matching
  the existing Windows and Linux behaviour.

**Bundled assets (see ADR 0002).**
- Relocate `resources/` (icons + example Config) **into the package** and load
  them via **`importlib.resources`**, replacing the source-tree-relative
  `__file__` walk that breaks inside a frozen installer. This is read-only
  bundled data and is distinct from the user's Config in `~/.config`.

**Testability seams (pure functions lifted out of tangled code).**
- **Seam A — launch-command construction:** a pure function taking the Rez
  command, a Tool's `rez_wants`, and the Tool's `command`, returning the full
  `rez-env <rez_wants> -- <command>` string. Extracted out of the UI.
- **Seam B — config-path resolution:** a pure function mapping (platform,
  environment) → the Config file path, isolating the `TOOLBOX_CONFIG` / Windows /
  macOS / Linux branching from filesystem I/O.
- **Seam C — config parsing:** a pure function mapping a parsed Config dict →
  `ToolSet`/`Tool` models, separated from disk reads and module-global mutation.
- **Seam D — bundled-asset resolution:** the `importlib.resources` accessor for
  bundled assets.
- The thin I/O glue that remains between B, C, and D (read file, copy the default
  Config) is left to a single temp-dir integration test.

**Packaging (Briefcase — see ADR 0001).**
- `[tool.briefcase]` configuration: bundle identifier **`co.brkpt.toolbox`**,
  author **Dylan Neill**, license **MIT**, macOS **`min_os_version = "13.0"`**.
- Generate a macOS `.icns` from the existing 512px PNG icon.
- Targets: Windows `.msi`, macOS `.dmg`, Linux AppImage (built on a glibc
  2.34+ base).
- Signing and notarisation steps are present but **guarded/skipped** (builds ship
  unsigned) until code-signing certificates exist.

**Continuous integration (GitHub Actions).**
- Matrix over `windows-latest`, `macos-latest`, `ubuntu-latest`.
- Run the full pytest suite (with `QT_QPA_PLATFORM=offscreen`) on every push and
  pull request.
- Build the three installer artifacts on a tagged release. Signing stays off (the
  guarded steps are no-ops until certs are provided).

## Testing Decisions

- **Test external behaviour, not implementation.** Assert the produced launch
  string, the resolved Config path, the parsed models, and that a named asset
  resolves — never internal call sequences or private state.
- **Modules under test:** the four pure seams (A launch-command construction,
  B config-path resolution, C config parsing, D asset resolution), one temp-dir
  integration test for the residual load-Config glue, and one pytest-qt smoke
  test (E) that constructs the main window headlessly.
- **Config-path tests** cover every branch: Windows, macOS, Linux, a
  `TOOLBOX_CONFIG` file, and a `TOOLBOX_CONFIG` directory — with platform and
  environment injected, not mocked at the OS level.
- **Config-parsing tests** include a well-formed Config and malformed input
  (missing keys, empty Toolsets).
- **Prior art:** there are no existing tests; this suite establishes the pattern.
  It is the reference for future tests, so keep it plain pytest with fixtures for
  temp dirs and injected platform/env.
- The GUI smoke test runs headless via `QT_QPA_PLATFORM=offscreen` so it works on
  CI runners without a display.

## Out of Scope

- Deep GUI interaction testing (clicking through the icon grid, detail panel,
  desktop-shortcut creation). Only the construction smoke test is in scope.
- Real code signing and notarisation. The hooks are wired and guarded, but no
  certificates are obtained and no signed artifacts are produced here.
- Migrating the user Config to OS-native locations (`%APPDATA%`,
  `~/Library/Application Support`). The `~/.config` convention is retained on all
  platforms (ADR 0003); a future `platformdirs` migration would need its own move
  step.
- The disabled/unimplemented UI elements noted in the README. Not touched.
- Reworking the Rez integration itself, the Config schema, or any launcher
  feature behaviour.
- Publishing to any store or distribution channel.

## Further Notes

- macOS PySide6 wheels are universal2 (Apple Silicon + Intel) with a macOS 13.0
  minimum; the Briefcase `min_os_version` must match or wheel resolution fails.
- Linux AppImage builds require glibc 2.34+ (`ubuntu-latest` satisfies this); if
  the studio's Linux boxes turn out to be a specific distro, a `.deb`/`.rpm`
  target can replace the AppImage later.
- The macOS runtime fixes (config path + Open Shell) are prerequisites for a
  meaningful macOS installer — a `.dmg` that cannot launch is not a deliverable,
  which is why the packaging work depends on them.
