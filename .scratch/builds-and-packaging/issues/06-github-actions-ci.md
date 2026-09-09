# 06: GitHub Actions CI

**What to build:** Every push and pull request runs the full test suite across Windows, macOS, and Linux, and every tagged release automatically builds the three installer artifacts — so regressions surface immediately and the maintainer never needs to keep a build machine per OS.

**Blocked by:** 04, 05

**Status:** ready-for-agent

- [ ] A GitHub Actions workflow runs a matrix over `windows-latest`, `macos-latest`, and `ubuntu-latest`
- [ ] The full pytest suite runs on every push and pull request, headless via `QT_QPA_PLATFORM=offscreen`
- [ ] On a tagged release, the workflow builds the Windows `.msi`, macOS `.dmg`, and Linux AppImage and uploads them as artifacts
- [ ] Signing/notarisation stays off (the guarded steps from ticket 05 are no-ops until certificates are provided)
- [ ] A failing test fails the workflow
