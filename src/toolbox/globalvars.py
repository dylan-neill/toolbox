# Builds a QPalette entirely from Qt enum members (QPalette.ColorGroup /
# ColorRole). PySide6 6.11's stubs expose these only as scoped enums, so the
# flat getattr access this file uses (valid at runtime) trips the stub-driven
# rules. Per ADR 0005 this Qt-boundary file runs the relaxed profile.
# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false, reportAttributeAccessIssue=false

from importlib.metadata import version

from PySide6 import QtGui

app_name: str = 'Toolbox'
name_with_version: str = f'{app_name} v{version("toolbox")}'

# Colour per QPalette role, shared by the Active and Inactive groups.
_ROLES: dict[str, tuple[int, int, int]] = {
    'WindowText': (255, 255, 255),
    'Button': (80, 80, 80),
    'Light': (75, 75, 75),
    'Midlight': (62, 62, 62),
    'Dark': (25, 25, 25),
    'Mid': (33, 33, 33),
    'Text': (245, 245, 245),
    'BrightText': (255, 255, 255),
    'ButtonText': (255, 255, 255),
    'Base': (100, 100, 100),
    'Window': (50, 50, 50),
    'Shadow': (0, 0, 0),
    'Highlight': (247, 147, 30),
    'AlternateBase': (25, 25, 25),
    'ToolTipBase': (255, 255, 220),
    'ToolTipText': (0, 0, 0),
    'PlaceholderText': (200, 200, 200),
}

# The Disabled group differs only in these roles.
_DISABLED_ROLES = {
    **_ROLES,
    'WindowText': (25, 25, 25),
    'Text': (25, 25, 25),
    'ButtonText': (25, 25, 25),
    'Base': (50, 50, 50),
    'Highlight': (174, 174, 174),
    'AlternateBase': (50, 50, 50),
    'PlaceholderText': (120, 120, 120),
}


def palette() -> QtGui.QPalette:
    palette = QtGui.QPalette()
    for group, roles in (
        (QtGui.QPalette.Active, _ROLES),
        (QtGui.QPalette.Inactive, _ROLES),
        (QtGui.QPalette.Disabled, _DISABLED_ROLES),
    ):
        for role, rgb in roles.items():
            palette.setColor(group, getattr(QtGui.QPalette, role), QtGui.QColor(*rgb))
    return palette
