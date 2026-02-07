
import platform
import sys
from PySide6 import QtCore, QtGui, QtWidgets

from . import resources
from . import model
from . import util

# Moved from globalvars.py
APP_NAME = 'Toolbox'
VERSION = (0, 7, 0)

def version_string():
    return f'v{VERSION[0]}.{VERSION[1]}.{VERSION[2]}'

def name_with_version():
    return f'{APP_NAME} {version_string()}'


class DataManager:
    """
    Manages the application state and data persistence.
    Replaces the global state in data.py.
    """
    def __init__(self):
        self.config_data = {}
        self.toolsets = []
        self.apps = []

    def load_config(self):
        """
        Loads configuration from disk and populates the model.
        """
        self.config_data = resources.load_config()
        self.toolsets = []
        
        if not self.config_data:
            return

        for toolset_index, toolset_dict in enumerate(self.config_data.get('toolsets', [])):
            toolset = model.ToolSet(toolset_dict['name'], "", "", [])
            self.toolsets.append(toolset)
            
            if 'job' in toolset_dict:
                toolset.job = toolset_dict['job']
            
            for app_index, tool_dict in enumerate(toolset_dict.get('apps', [])):
                tool = model.Tool(
                    tool_dict['app'], 
                    tool_dict['version'], 
                    tool_dict.get('desc', ''), 
                    tool_dict.get('tools', []), 
                    tool_dict.get('icon', ''), 
                    tool_dict.get('command', '')
                )
                if tool is not None:
                    tool.config_toolset_index = toolset_index
                    tool.config_app_index = app_index
                    toolset.add_tool(tool)
                else:
                    print(f"Error: couldn't find version: {tool_dict['version']}")

    def save_config(self):
        """
        Persists the current config data to disk.
        """
        if self.config_data is None:
             raise RuntimeError("Config data is not loaded")
        resources.save_config(self.config_data)

    def update_tool_packages(self, tool, rez_wants):
        """
        Updates a tool's rez packages in memory and persists to config file.
        :param tool: Tool instance
        :param rez_wants: list of rez package strings
        :return: (success: bool, error_message: str | None)
        """
        tool.rez_wants = rez_wants

        toolset_index = getattr(tool, "config_toolset_index", -1)
        app_index = getattr(tool, "config_app_index", -1)

        if toolset_index < 0 or app_index < 0:
            return False, "Tool is missing config indices"

        try:
            self.config_data['toolsets'][toolset_index]['apps'][app_index]['tools'] = rez_wants
            self.save_config()
        except Exception as exc:
            return False, str(exc)

        return True, None

    def get_toolsets(self):
        return self.toolsets

    def get_toolset_by_name(self, name):
        for toolset in self.toolsets:
            if toolset.name == name:
                return toolset
        return None

class ToolboxController(QtCore.QObject):
    """
    Handles business logic and interaction between UI and Data.
    """
    
    # Signals can be added here if needed for async updates
    
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.data_manager.load_config()

    def get_app_title(self):
        return name_with_version()

    def get_toolsets(self):
        return self.data_manager.get_toolsets()

    def get_toolset_names(self):
        return [ts.name for ts in self.data_manager.get_toolsets()]

    def get_tools_for_toolset(self, toolset_name):
        toolset = self.data_manager.get_toolset_by_name(toolset_name)
        if toolset:
            return toolset.tools
        return []

    def update_tool_packages(self, tool, rez_wants):
        return self.data_manager.update_tool_packages(tool, rez_wants)
    
    def launch_tool(self, tool, open_shell=False):
        """
        Constructs and executes the command to launch a tool.
        Returns the constructed command string and the QProcess.
        """
        rez_command = resources.rez_command()
        rez_wants = ' '.join(tool.rez_wants)
        
        full_command = ''
        
        # Determine the command structure based on platform and request
        if open_shell:
            if platform.system().lower() == 'windows':
                # Super hack for Windows to keep window open
                full_command = f'cmd.exe /C start cmd.exe /K {rez_command} {rez_wants}'
            else:
                 # Standard terminal for linux/mac
                 # Note: This might need adjustment based on specific terminal emulators available
                full_command = f'gnome-terminal -- {rez_command} {rez_wants}'
        else:
             full_command = f'{rez_command} {rez_wants} -- {tool.command}'
        
        # Execute
        process = QtCore.QProcess(self)
        process.startCommand(full_command)
        
        return full_command, process

    def create_desktop_shortcut(self, tool):
        if platform.system().lower() != "windows":
            return False, "Error: Creating desktop shortcuts is only supported on Windows"
            
        target = resources.python_command()
        arguments = f"{resources.rez_command()} {tool.rez_wants} -- {tool.command}"
        
        if tool.subtitle:
            name = f"{tool.title} ({tool.subtitle})"
        else:
            name = tool.title

        try:
            util.create_shortcut_on_desktop(name, target=target, arguments=arguments)
            return True, "Shortcut created successfully"
        except Exception as e:
            return False, f"Failed to create shortcut: {str(e)}"
