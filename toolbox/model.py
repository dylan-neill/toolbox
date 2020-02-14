__author__ = 'dylan.neill'


class Tool():

    def __init__(self, name='', version='', subtitle='', rez_wants=None, icon='', command=''):
        self.name = name
        self.version = version
        self.subtitle = subtitle
        if rez_wants is None:
            rez_wants = []
        self.rez_wants = rez_wants
        self.job = None
        self.icon = icon
        self.command = command

    @property
    def title(self):
        return "{0} {1}".format(self.name, self.version)


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
            print(tool.title)

    def add_tool(self, tool):
        self._tools.append(tool)
        if self.job is not None:
            tool.job = self.job
