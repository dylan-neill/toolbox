import os

# The GUI tests must run without a display (locally and on CI runners), so force
# Qt's offscreen platform before any QApplication is created by pytest-qt.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolated_settings(
    request: pytest.FixtureRequest,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Point the Settings store at a throwaway file for every test.

    The main window now reads the store on construction (geometry / last
    toolset) and writes it on close (pytest-qt closes added widgets at
    teardown), so without this the suite would read and clobber the developer's
    real ``~/.config/toolbox/settings.json``. Redirecting ``settings_path`` is
    enough: ``load_settings`` / ``save_settings`` resolve through it, and tests
    that stub those two directly simply override this harmless default.

    ``test_settings`` is skipped — it unit-tests ``settings_path`` itself (so
    patching it would defeat the test) and already isolates its own file I/O.
    """
    if request.path.name == "test_settings.py":
        return

    from toolbox import settings

    target = tmp_path / "settings.json"

    def _fixed_settings_path(system: str) -> str:
        return str(target)

    monkeypatch.setattr(settings, "settings_path", _fixed_settings_path)
