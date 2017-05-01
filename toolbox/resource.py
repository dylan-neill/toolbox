import os
import platform

# Get parent folder of the folder containing this script file (ie the app root path)
app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pipe_path = ''

def named(filename, of_type=None):
    """
    Retrieves the full path for the named file
    :param filename: File name to search for in resources
    :param of_type: Type of file to look for. Will be an enum at some point
    :return: Path string
    """

    directory = None

    if of_type == "icon":
        directory = "resources/icons"
    if of_type == "json":
        directory = "resources"

    if directory is not None:
        return "%s/%s/%s" % (app_path, directory, filename)
    else:
        return os.path.join(app_path, filename)

def python_command():
    if platform.system().lower() == 'windows':
        return 'C:\\Python27\\pythonw.exe'
    else:
        return 'python'

def get_pipe_python_root(dev=False):

    global pipe_path

    if dev:
        if platform.system().lower() == 'windows':
            pipe_path = '//fsm.int/fsm/library/assets/pipeline/users/dylan.neill/dev/pipeline/python'
        if platform.system().lower() == 'darwin':
            pipe_path = '/Volumes/library_assets/pipeline/pipeline/users/dylan.neill/dev/pipeline/python'
        if platform.system().lower() == 'linux':
            pipe_path = '/fsm.int/fsm/library/assets/pipeline/pipeline/users/dylan.neill/dev/pipeline/python'
    else:
        if platform.system().lower() == 'windows':
            pipe_path = '//fsm.int/fsm/library/assets/pipeline/python'
        if platform.system().lower() == 'darwin':
            pipe_path = '/Volumes/library_assets/pipeline/python'
        if platform.system().lower() == 'linux':
            pipe_path = '/fsm.int/fsm/library/assets/pipeline/python'

    pipe_path = os.path.realpath(pipe_path)
    return pipe_path

def get_eco_command():

    return os.path.join(pipe_path, 'ecosystem', 'main.py')
