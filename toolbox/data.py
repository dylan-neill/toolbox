from .model import Tool, ToolSet

from . import resources

apps = []
toolsets = []
config_data = None

def populate():
    """
    Populates model with data from config.json
    :return:
    """

    global toolsets, apps

    global config_data
    config_data = resources.load_config()

    for toolset_index, toolset_dict in enumerate(config_data['toolsets']):
        toolset = ToolSet(toolset_dict['name'], "", "", [])
        toolsets.append(toolset)
        if 'job' in toolset_dict:
            toolset.job = toolset_dict['job']
        for app_index, tool_dict in enumerate(toolset_dict['apps']):
            tool = Tool(tool_dict['app'], tool_dict['version'], tool_dict['desc'], tool_dict['tools'], tool_dict['icon'], tool_dict['command'])
            if tool is not None:
                tool.config_toolset_index = toolset_index
                tool.config_app_index = app_index
                toolset.add_tool(tool)
            else:
                print(f"Error: couldn't find version: {tool_dict['version']}")


def toolset_from_name(name):

    for toolset in toolsets:
        if toolset.name == name:
            return toolset

    return None


def update_tool_packages(tool, rez_wants):
    """
    Updates a tool's rez packages in memory and persists to config file.
    :param tool: Tool instance
    :param rez_wants: list of rez package strings
    :return: (success: bool, error_message: str | None)
    """
    global config_data

    tool.rez_wants = rez_wants

    if config_data is None:
        return False, "Config data is not loaded"

    toolset_index = getattr(tool, "config_toolset_index", -1)
    app_index = getattr(tool, "config_app_index", -1)

    if toolset_index < 0 or app_index < 0:
        return False, "Tool is missing config indices"

    try:
        config_data['toolsets'][toolset_index]['apps'][app_index]['tools'] = rez_wants
        resources.save_config(config_data)
    except Exception as exc:
        return False, str(exc)

    return True, None
