# 05: Briefcase packaging → installers

**What to build:** Toolbox builds to native, double-click installers on all three platforms — a Windows `.msi`, a macOS `.dmg` (running on macOS 13+), and a Linux AppImage — using Briefcase. Each installed build launches and finds its bundled assets. Builds ship unsigned for now, with signing and notarisation present as guarded, ready-to-enable steps for the eventual public release.

**Blocked by:** 02, 03

**Status:** ready-for-agent

- [ ] `[tool.briefcase]` configuration with bundle identifier `co.brkpt.toolbox`, author Dylan Neill, MIT license, and macOS `min_os_version = "13.0"`
- [ ] A macOS `.icns` is generated from the existing 512px PNG icon
- [ ] `briefcase package` produces a Windows `.msi`, a macOS `.dmg`, and a Linux AppImage
- [ ] Each installed build launches and finds its icons and example Config (relies on ticket 02)
- [ ] The macOS build launches successfully (relies on ticket 03)
- [ ] Signing/notarisation steps exist but are guarded/skipped so builds succeed unsigned without certificates
