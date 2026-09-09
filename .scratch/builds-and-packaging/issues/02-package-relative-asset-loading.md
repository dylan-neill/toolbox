# 02: Package-relative asset loading

**What to build:** Toolbox finds its bundled assets — the application icons and the example Config — whether it is run from a source checkout or from a frozen installer. Today assets are located by walking up from the source file, which does not exist inside a packaged app; switching to package-relative loading is the prerequisite that keeps the installers (ticket 05) from launching into missing icons and a missing default Config.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] Bundled assets (icons + example Config) live inside the package and load via `importlib.resources`
- [ ] The source-tree-relative `__file__` asset lookup is gone
- [ ] Running from source still resolves every icon and the example Config
- [ ] Seam D: a test asserts that a known bundled asset (an icon and the example Config) resolves
- [ ] The user's Config in `~/.config/toolbox/` is unaffected — only read-only bundled data moved
