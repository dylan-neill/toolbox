__author__ = 'dylan.neill'

class App():

    def __init__(self, name):
        self.name = name
        self.package = ''
        self.command = ''
        self.versions = []

    def add_versions(self, version_list, icon=None):
        if isinstance(version_list, list):
            for version in version_list:
                self.add_version(version, icon=icon)
        else:
            raise ValueError('Add Versions: Input not a list')

    def add_version(self, version, icon=None):
        new_version = AppVersion(version, self)
        if icon is not None:
            new_version.icon = icon
        self.versions.append(new_version)

    def get_app_version(self, version):
        for appver in self.versions:
            if appver.name == version:
                return appver

        return None

class AppVersion():

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.icon = None

class Tool():

    def __init__(self, app_version, subtitle='', eco_wants=None, icon=''):
        if app_version is None or not isinstance(app_version, AppVersion):
            raise ValueError('AppVersion object must be specified')
        self.app_version = app_version
        self.subtitle = subtitle
        if eco_wants is None:
            eco_wants = []
        self.eco_wants = eco_wants
        self.job = None
        self._icon = icon

    @property
    def title(self):
        return "%s %s" % (self.app_version.parent.name, self.app_version.name)

    @property
    def icon(self):
        if self._icon == '':
            return self.app_version.icon
        else:
            return  self._icon

    @property
    def command(self):
        return self.app_version.parent.command

class ToolSet():

    def __init__(self, name):
        self.name = name
        self.description = ''
        self.job = None
        self._tools = []

    @property
    def tools(self):
        return self._tools

    def print_tool_names(self):
        for tool in self._tools:
            print tool.title

    def add_tool(self, tool):
        self._tools.append(tool)
        if self.job is not None:
            tool.job = self.job
