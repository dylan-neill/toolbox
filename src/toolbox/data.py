from typing import NotRequired, TypedDict

from .model import Tool, ToolSet

from . import resources


class ToolDict(TypedDict):
    """The raw JSON shape of one Tool in the Config."""
    name: str
    version: str
    desc: str
    rez_wants: list[str]
    icon: str
    command: str


class ToolSetDict(TypedDict):
    """The raw JSON shape of one Toolset in the Config."""
    name: str
    job: NotRequired[str]
    tools: list[ToolDict]


class ConfigDict(TypedDict):
    """The raw JSON shape of the whole Config (see CONTEXT.md "Config")."""
    toolsets: list[ToolSetDict]


toolsets: list[ToolSet] = []


def parse_config(config: ConfigDict) -> list[ToolSet]:
    """Seam C: map a parsed Config dict to ToolSet/Tool models.

    Pure: no disk reads, no module-global mutation. A malformed Config (a missing
    key) raises ``KeyError`` so a bad Config fails predictably at the parse.
    """
    result: list[ToolSet] = []
    for toolset_dict in config['toolsets']:
        toolset = ToolSet(toolset_dict['name'], "", toolset_dict.get('job'), [])
        for tool_dict in toolset_dict['tools']:
            toolset.add_tool(Tool(
                tool_dict['name'],
                tool_dict['version'],
                tool_dict['desc'],
                tool_dict['rez_wants'],
                tool_dict['icon'],
                tool_dict['command'],
            ))
        result.append(toolset)
    return result


def populate() -> None:
    """
    Populates model with data from config.json
    :return:
    """

    global toolsets

    toolsets = parse_config(resources.load_config())


def toolset_from_name(name: str) -> ToolSet | None:

    for toolset in toolsets:
        if toolset.name == name:
            return toolset

    return None
