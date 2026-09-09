# 03: macOS runtime support

**What to build:** An artist on macOS can launch Toolbox without it crashing, their Config lives at `~/.config/toolbox/` just like on Windows and Linux, and the "Open Shell" action opens a terminal inside the selected Rez environment. This closes the gap that currently makes Toolbox unusable on macOS and is a prerequisite for a meaningful macOS installer. Config parsing (Seam C) is lifted into a pure function here as part of untangling the Config-loading path.

**Blocked by:** 01

**Status:** done

- [x] Config-path resolution has a macOS branch using `~/.config/toolbox/`; the app launches on macOS instead of crashing
- [x] `TOOLBOX_CONFIG` (file or directory) still overrides the default path on every platform
- [x] Existing Windows/Linux Config paths are unchanged (no migration of existing user Configs)
- [x] "Open Shell" has a macOS branch that opens a terminal inside the selected Rez environment
- [x] Seam B: config-path resolution is a pure function of (platform, environment), unit-tested across Windows, macOS, Linux, a `TOOLBOX_CONFIG` file, and a `TOOLBOX_CONFIG` directory
- [x] Seam C: config parsing is a pure function mapping a Config dict → ToolSet/Tool models, separated from disk reads and module-global mutation, unit-tested with well-formed and malformed input
- [x] A single temp-dir integration test covers the residual load-Config glue (read file, copy the default Config on first launch)
