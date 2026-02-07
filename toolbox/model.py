from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Tool:
    name: str
    version: str
    subtitle: str
    rez_wants: list[str]
    icon: str
    command: str
    job: str = ""
    config_toolset_index: int = -1
    config_app_index: int = -1
    tool_id: str = ""

    @property
    def title(self) -> str:
        return f"{self.name} {self.version}"


@dataclass
class ToolSet:
    name: str
    description: str
    job: str
    _tools: list[Tool]

    @property
    def tools(self) -> list[Tool]:
        return self._tools

    def add_tool(self, tool: Tool) -> None:
        self._tools.append(tool)
        if self.job:
            tool.job = self.job
