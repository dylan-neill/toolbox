import json

from model import App, Tool, ToolSet, AppVersion

import resource

apps = []
toolsets = []

def populate():
    """
    Populates with data (temp data for the time being)
    :return:
    """

    global toolsets, apps

    # production_toolset = ToolSet("Production")
    # testing_toolset = ToolSet("Testing")

    maya_app = App('Maya')
    maya_app.package = 'maya'
    maya_app.command = 'maya'
    maya_app.add_versions(version_list=['2014', '2015', '2016', '2016.5', '2017'], icon="maya_icon.png")
    apps.append(maya_app)

    houdini_app = App('Houdini')
    houdini_app.package = 'houdini'
    houdini_app.command = 'houdinifx'
    houdini_app.add_versions(version_list=['15.0'], icon="houdini_icon.png")
    apps.append(houdini_app)

    mari_app = App('Mari')
    mari_app.package = 'mari'
    mari_app.command = 'mari'
    mari_app.add_versions(version_list=['2.6v5', '3.0v2', '3.0v3'], icon="mari_icon.png")
    apps.append(mari_app)

    nukex_app = App('NukeX')
    nukex_app.package = 'nuke'
    nukex_app.command = 'nukex'
    nukex_app.add_versions(version_list=['6.3v4', '9.0v5', '9.0v8'], icon="nuke_icon.png")
    apps.append(nukex_app)

    nukestudio_app = App('Nuke Studio')
    nukestudio_app.package = 'nuke'
    nukestudio_app.command = 'nukestudio'
    nukestudio_app.add_versions(version_list=['9.0v5', '9.0v8'], icon="nuke_icon.png")
    apps.append(nukestudio_app)

    config_file = resource.named('config.json', of_type='json')
    with open(config_file) as file_id:
        config_data = json.load(file_id)

    for toolset_dict in config_data['toolsets']:
        toolset = ToolSet(toolset_dict['name'])
        toolsets.append(toolset)
        if 'job' in toolset_dict:
            toolset.job = toolset_dict['job']
        for tool_dict in toolset_dict['apps']:
            app_obj = None
            for app in apps:
                if app.name == tool_dict['app']:
                    app_obj = app
                    break
            if app_obj is not None:
                tool = create_tool(app_obj, tool_dict['version'], tool_dict['desc'], tool_dict['tools'], icon=tool_dict['icon'])
                if tool is not None:
                    toolset.add_tool(tool)
                else:
                    print "Error: couldn't find version: {0}".format(tool_dict['version'])
            else:
                print "Error: couldn't find app: {0}".format(tool_dict['app'])

def toolset_from_name(name):

    for toolset in toolsets:
        if toolset.name == name:
            return toolset

    return None


def create_tool(app, version, subtitle, eco_wants=None, icon=''):

    app_version = app.get_app_version(version)
    #assert isinstance(app_version, AppVersion)

    if app_version is not None:
        new_tool = Tool(app_version, subtitle=subtitle, eco_wants=eco_wants, icon=icon)
        return new_tool
    else:
        # print "Couldn't find an app version for string: %s" % version
        return None
