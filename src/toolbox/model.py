from dataclasses import dataclass


@dataclass
class Tool():
    name: str
    version: str
    subtitle: str
    rez_wants: list[str]
    icon: str
    command: str

    @property
    def title(self) -> str:
        return f"{self.name} {self.version}"

@dataclass
class ToolSet():
    name: str
    description: str
    # An optional Rez context identifier for the group (see CONTEXT.md "Job").
    # None means "no job"; recorded intent only — not yet applied at launch.
    job: str | None
    _tools: list[Tool]

    @property
    def tools(self) -> list[Tool]:
        return self._tools

    def add_tool(self, tool: Tool) -> None:
        self._tools.append(tool)
