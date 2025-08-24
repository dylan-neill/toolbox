from model import Tool, ToolSet

import resources

apps = []
toolsets = []

def populate():
    """
    Populates model with data from config.json
    :return:
    """

    global toolsets, apps

    config_data = resources.load_config()

    for toolset_dict in config_data['toolsets']:
        toolset = ToolSet(toolset_dict['name'])
        toolsets.append(toolset)
        if 'job' in toolset_dict:
            toolset.job = toolset_dict['job']
        for tool_dict in toolset_dict['apps']:
            tool = Tool(tool_dict['app'], tool_dict['version'], tool_dict['desc'], tool_dict['tools'], tool_dict['icon'], tool_dict['command'])
            if tool is not None:
                toolset.add_tool(tool)
            else:
                print(f"Error: couldn't find version: {tool_dict['version']}")


def toolset_from_name(name):

    for toolset in toolsets:
        if toolset.name == name:
            return toolset

    return None

