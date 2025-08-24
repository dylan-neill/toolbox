from dataclasses import dataclass

@dataclass
class Tool():
    name: str
    version: str
    subtitle: str
    rez_wants: list
    icon: str
    command: str

    @property
    def title(self):
        return f"{self.name} {self.version}"

@dataclass
class ToolSet():
    name: str
    description: str
    job: str
    _tools: list

    @property
    def tools(self):
        return self._tools

    # def print_tool_names(self):
    #     for tool in self._tools:
    #         print(tool.title)

    def add_tool(self, tool):
        self._tools.append(tool)
        if self.job is not None:
            tool.job = self.job
