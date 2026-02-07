from __future__ import annotations

from toolbox.model import Tool
from toolbox.services.launcher import QtProcessLauncher


def sample_tool() -> Tool:
    return Tool(
        name="Blender",
        version="2.81",
        subtitle="",
        rez_wants=["blender-2.81", "dnvfx"],
        icon="blender_icon.png",
        command="blender --factory-startup",
        tool_id="0:0",
    )


def test_build_launch_command_uses_arg_list():
    launcher = QtProcessLauncher(rez_command="rez-env")
    spec = launcher.build_launch(sample_tool(), open_shell=False, system_name="Linux")

    assert spec.program == "rez-env"
    assert spec.args[:3] == ["blender-2.81", "dnvfx", "--"]
    assert spec.args[-2:] == ["blender", "--factory-startup"]


def test_build_open_shell_windows_command():
    launcher = QtProcessLauncher(rez_command="rez-env")
    spec = launcher.build_launch(sample_tool(), open_shell=True, system_name="Windows")

    assert spec.program == "cmd.exe"
    assert spec.args[:3] == ["/C", "start", "cmd.exe"]


def test_build_open_shell_macos_command():
    launcher = QtProcessLauncher(rez_command="rez-env")
    spec = launcher.build_launch(sample_tool(), open_shell=True, system_name="Darwin")

    assert spec.program == "osascript"
    assert spec.args[0] == "-e"
    assert "Terminal" in spec.args[1]


def test_build_open_shell_linux_terminal(monkeypatch):
    launcher = QtProcessLauncher(rez_command="rez-env")
    monkeypatch.setattr(launcher, "_discover_linux_terminal", lambda: "gnome-terminal")

    spec = launcher.build_launch(sample_tool(), open_shell=True, system_name="Linux")

    assert spec.program == "gnome-terminal"
    assert spec.args[:2] == ["--", "bash"]


def test_build_open_shell_linux_xterm_fallback(monkeypatch):
    launcher = QtProcessLauncher(rez_command="rez-env")
    monkeypatch.setattr(launcher, "_discover_linux_terminal", lambda: "xterm")

    spec = launcher.build_launch(sample_tool(), open_shell=True, system_name="Linux")

    assert spec.program == "xterm"
    assert spec.args[:2] == ["-e", "bash"]
