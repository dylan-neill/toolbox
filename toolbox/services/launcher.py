from __future__ import annotations

import platform
import shlex
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass

from PySide6 import QtCore


@dataclass
class LaunchSpec:
    program: str
    args: list[str]
    display_command: str


class Launcher(ABC):
    @abstractmethod
    def build_launch(
        self,
        tool,
        open_shell: bool = False,
        system_name: str | None = None,
    ) -> LaunchSpec:
        raise NotImplementedError

    @abstractmethod
    def start(
        self,
        tool,
        open_shell: bool = False,
        parent: QtCore.QObject | None = None,
    ) -> tuple[QtCore.QProcess, LaunchSpec]:
        raise NotImplementedError


class QtProcessLauncher(Launcher):
    def __init__(self, rez_command: str = "rez-env") -> None:
        self._rez_command = rez_command

    def build_launch(
        self,
        tool,
        open_shell: bool = False,
        system_name: str | None = None,
    ) -> LaunchSpec:
        system = (system_name or platform.system()).lower()
        rez_prefix = [self._rez_command, *tool.rez_wants]
        rez_shell_command = shlex.join(rez_prefix)

        if not open_shell:
            command_tokens = [*rez_prefix, "--", *shlex.split(tool.command)]
            return LaunchSpec(
                program=command_tokens[0],
                args=command_tokens[1:],
                display_command=shlex.join(command_tokens),
            )

        if system == "windows":
            args = ["/C", "start", "cmd.exe", "/K", rez_shell_command]
            return LaunchSpec("cmd.exe", args, "cmd.exe " + shlex.join(args))

        if system == "darwin":
            escaped_command = rez_shell_command.replace('"', '\\"')
            apple_script = f'tell application "Terminal" to do script "{escaped_command}"'
            args = ["-e", apple_script]
            return LaunchSpec("osascript", args, "osascript " + shlex.join(args))

        terminal = self._discover_linux_terminal()
        if terminal == "gnome-terminal":
            args = ["--", "bash", "-lc", rez_shell_command]
            display = f"{terminal} -- bash -lc {shlex.quote(rez_shell_command)}"
            return LaunchSpec(terminal, args, display)

        if terminal == "xfce4-terminal":
            bash_command = f"bash -lc {shlex.quote(rez_shell_command)}"
            args = ["--command", bash_command]
            display = f"{terminal} --command {shlex.quote(bash_command)}"
            return LaunchSpec(terminal, args, display)

        args = ["-e", "bash", "-lc", rez_shell_command]
        display = f"{terminal} -e bash -lc {shlex.quote(rez_shell_command)}"
        return LaunchSpec(terminal, args, display)

    def start(
        self,
        tool,
        open_shell: bool = False,
        parent: QtCore.QObject | None = None,
    ) -> tuple[QtCore.QProcess, LaunchSpec]:
        spec = self.build_launch(tool=tool, open_shell=open_shell)
        process = QtCore.QProcess(parent)
        process.start(spec.program, spec.args)
        return process, spec

    def _discover_linux_terminal(self) -> str:
        for terminal in [
            "gnome-terminal",
            "konsole",
            "xfce4-terminal",
            "x-terminal-emulator",
            "xterm",
        ]:
            if shutil.which(terminal):
                return terminal
        raise RuntimeError("No supported terminal emulator found")
