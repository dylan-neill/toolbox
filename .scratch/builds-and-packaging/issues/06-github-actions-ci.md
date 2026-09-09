# 06: GitHub Actions CI

**What to build:** Every push and pull request runs the full test suite across Windows, macOS, and Linux, and every tagged release automatically builds the three installer artifacts — so regressions surface immediately and the maintainer never needs to keep a build machine per OS.

**Blocked by:** 04, 05

**Status:** done

- [x] A GitHub Actions workflow runs a matrix over `windows-latest`, `macos-latest`, and `ubuntu-latest`
- [x] The full pytest suite runs on every push and pull request, headless via `QT_QPA_PLATFORM=offscreen`
- [x] On a tagged release, the workflow builds the Windows `.msi`, macOS `.dmg`, and Linux AppImage and uploads them as artifacts
- [x] Signing/notarisation stays off (the guarded steps from ticket 05 are no-ops until certificates are provided)
- [x] A failing test fails the workflow

## Comments

Implemented on branch `refactor/builds-and-packaging` in `.github/workflows/ci.yml`.

Two jobs:

- **test** — matrix over the three runners, `uv sync` + `uv run pytest`, with
  `QT_QPA_PLATFORM=offscreen`. Linux installs the Qt runtime libs PySide6 dlopens
  even under the offscreen plugin (`libegl1 libgl1 libxkbcommon0 libdbus-1-3`).
  Runs on every push and pull request; a test failure fails the job.
- **build** — `needs: test`, gated on `if: startsWith(github.ref, 'refs/tags/')`,
  so installers are only built for a tagged release and only when tests pass. Each
  OS runs `uv run briefcase create/build/package` for its native format
  (`windows` → .msi, `macOS` → .dmg, `linux AppImage`) and uploads the result via
  `actions/upload-artifact@v4` with `if-no-files-found: error`.

Signing guard: macOS packages with `--adhoc-sign` (Briefcase's unsigned path)
unless a `MACOS_SIGNING_IDENTITY` secret is set, in which case it packages with
`--identity`. With no secret configured it is a no-op — enabling signing later is
adding a secret, not editing the pipeline.

Reviewed via `/code-review` (Standards + Spec axes): all ticket criteria met; only
judgement-call findings (idiomatic cross-job step duplication; test job pins Python
3.12, which ticket 06 permits since it mandates only the OS matrix).
