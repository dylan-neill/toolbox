# importlib.resources for bundled assets

Bundled assets (icons and the example config) live **inside the package** at
`src/toolbox/resources/` and are loaded through `importlib.resources`, replacing
the previous filesystem walk (`app_path = dirname(dirname(__file__))` then
reading `resources/…` relative to the source tree).

The old approach only works when running from a source checkout. Inside a
Briefcase `.app`/`.msi`/AppImage the source-relative `resources/` directory does
not exist, so the app would build but fail to find its icons and default config
at launch. Loading assets as package data is the portable way to locate them in
both source and frozen installs.

## Consequences

- This is distinct from **user** data: the user's `config.json` remains in
  `~/.config/toolbox/` (overridable via `TOOLBOX_CONFIG`) and is unaffected. Only
  the read-only bundled seed/icons moved into the package.
