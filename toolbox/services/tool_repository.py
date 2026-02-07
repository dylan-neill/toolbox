from __future__ import annotations

from abc import ABC, abstractmethod

from ..model import Tool, ToolSet
from .config_store import ConfigStore


class ToolRepository(ABC):
    @abstractmethod
    def load_toolsets(self) -> list[ToolSet]:
        raise NotImplementedError

    @abstractmethod
    def toolset_from_name(self, name: str) -> ToolSet | None:
        raise NotImplementedError

    @abstractmethod
    def update_tool_packages(self, tool_id: str, rez_wants: list[str]) -> tuple[bool, str | None]:
        raise NotImplementedError


class InMemoryToolRepository(ToolRepository):
    def __init__(self, config_store: ConfigStore) -> None:
        self._config_store = config_store
        self._toolsets: list[ToolSet] = []
        self._config_data: dict | None = None

    @property
    def config_data(self) -> dict | None:
        return self._config_data

    def load_toolsets(self) -> list[ToolSet]:
        config_data = self._config_store.load()
        toolsets: list[ToolSet] = []

        for toolset_index, toolset_dict in enumerate(config_data.get("toolsets", [])):
            toolset = ToolSet(
                name=toolset_dict["name"],
                description="",
                job=toolset_dict.get("job", ""),
                _tools=[],
            )
            for app_index, tool_dict in enumerate(toolset_dict.get("apps", [])):
                tool = Tool(
                    name=tool_dict["app"],
                    version=tool_dict["version"],
                    subtitle=tool_dict.get("desc", ""),
                    rez_wants=list(tool_dict.get("tools", [])),
                    icon=tool_dict["icon"],
                    command=tool_dict["command"],
                    config_toolset_index=toolset_index,
                    config_app_index=app_index,
                    tool_id=f"{toolset_index}:{app_index}",
                )
                toolset.add_tool(tool)
            toolsets.append(toolset)

        self._toolsets = toolsets
        self._config_data = config_data
        return self._toolsets

    def toolset_from_name(self, name: str) -> ToolSet | None:
        for toolset in self._toolsets:
            if toolset.name == name:
                return toolset
        return None

    def update_tool_packages(self, tool_id: str, rez_wants: list[str]) -> tuple[bool, str | None]:
        if self._config_data is None:
            return False, "Config data is not loaded"

        try:
            toolset_index, app_index = [int(token) for token in tool_id.split(":", 1)]
        except (ValueError, TypeError):
            return False, "Invalid tool id"

        try:
            self._config_data["toolsets"][toolset_index]["apps"][app_index]["tools"] = list(
                rez_wants
            )
            self._config_store.save(self._config_data)
        except Exception as exc:  # noqa: BLE001
            return False, str(exc)

        for toolset in self._toolsets:
            for tool in toolset.tools:
                if tool.tool_id == tool_id:
                    tool.rez_wants = list(rez_wants)
                    return True, None

        return True, None
