from __future__ import annotations

import os

import pytest

from toolbox.model import Tool, ToolSet

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


class StubRepository:
    def __init__(self) -> None:
        self._tool = Tool(
            name="Blender",
            version="2.81",
            subtitle="",
            rez_wants=["blender-2.81", "dnvfx"],
            icon="blender_icon.png",
            command="blender",
            tool_id="0:0",
        )
        self._toolset = ToolSet(name="Production", description="", job="", _tools=[self._tool])
        self.updated: tuple[str, list[str]] | None = None

    def load_toolsets(self) -> list[ToolSet]:
        return [self._toolset]

    def toolset_from_name(self, name: str) -> ToolSet | None:
        if name == self._toolset.name:
            return self._toolset
        return None

    def update_tool_packages(self, tool_id: str, rez_wants: list[str]):
        self.updated = (tool_id, list(rez_wants))
        if tool_id == self._tool.tool_id:
            self._tool.rez_wants = list(rez_wants)
        return True, None


@pytest.fixture(scope="session")
def qapp():
    pytest.importorskip("PySide6")
    from PySide6 import QtWidgets

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    return app


@pytest.fixture
def stub_repository() -> StubRepository:
    return StubRepository()
