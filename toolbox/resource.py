import os
import platform

# Get parent folder of the folder containing this script file (ie the app root path)
app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
        return 'pythonw.exe'
    else:
        return 'python3'


def rez_command():
    return 'rez-env'
