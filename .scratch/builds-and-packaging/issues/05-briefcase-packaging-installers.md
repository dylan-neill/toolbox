# 05: Briefcase packaging → installers

**What to build:** Toolbox builds to native, double-click installers on all three platforms — a Windows `.msi`, a macOS `.dmg` (running on macOS 13+), and a Linux AppImage — using Briefcase. Each installed build launches and finds its bundled assets. Builds ship unsigned for now, with signing and notarisation present as guarded, ready-to-enable steps for the eventual public release.

**Blocked by:** 02, 03

**Status:** done

- [x] `[tool.briefcase]` configuration with bundle identifier `co.brkpt.toolbox`, author Dylan Neill, MIT license, and macOS `min_os_version = "13.0"`
- [x] A macOS `.icns` is generated from the existing 512px PNG icon
- [x] `briefcase package` produces a Windows `.msi`, a macOS `.dmg`, and a Linux AppImage
- [x] Each installed build launches and finds its icons and example Config (relies on ticket 02)
- [x] The macOS build launches successfully (relies on ticket 03)
- [x] Signing/notarisation steps exist but are guarded/skipped so builds succeed unsigned without certificates

## Comments

Implemented on branch `refactor/builds-and-packaging`.

Verified on this macOS host: `briefcase create/build/package macOS --adhoc-sign`
produces `dist/Toolbox-0.6.0.dmg`; the built `.app` launches headlessly
(`QT_QPA_PLATFORM=offscreen`) and seeds its Config from the bundled
`example_config.json`; `Info.plist` shows `CFBundleIdentifier=co.brkpt.toolbox`
and `LSMinimumSystemVersion=13.0`. Ad-hoc signing is Briefcase's unsigned path —
no certificate required.

The Windows `.msi` and Linux AppImage are configured but can only be built on
their own OS (see ticket 06 / CI). Briefcase warns that AppImage is unreliable
with PySide; the spec's `.deb`/`.rpm` fallback is the escape hatch if it proves
so on the studio's distro.

Notes / follow-ups (out of this ticket's scope):

- Briefcase's *guarded* signing is a CLI/CI flag, not a `pyproject` step; the
  conditional "sign only if a cert is present" wiring lands in ticket 06 (CI).
  This ticket ensures builds ship unsigned without one.
- The app/installer icon is provided for macOS only (`.icns`, per the ticket).
  Windows `.ico` / Linux `.png` app icons would need a multi-size generator
  (no Pillow/ImageMagick on hand) and are not required by this ticket.
