from .model import Tool, ToolSet

from . import resources

apps = []
toolsets = []

def parse_config(config):
    """Seam C: map a parsed Config dict to ToolSet/Tool models.

    Pure: no disk reads, no module-global mutation. A malformed Config (a missing
    key) raises ``KeyError`` so a bad Config fails predictably at the parse.
    """
    result = []
    for toolset_dict in config['toolsets']:
        toolset = ToolSet(toolset_dict['name'], "", "", [])
        if 'job' in toolset_dict:
            toolset.job = toolset_dict['job']
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


def populate():
    """
    Populates model with data from config.json
    :return:
    """

    global toolsets

    toolsets = parse_config(resources.load_config())


def toolset_from_name(name):

    for toolset in toolsets:
        if toolset.name == name:
            return toolset

    return None

