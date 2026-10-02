# PySide6's bundled 6.11 stubs under-type signals/slots and many overloads.
# Per ADR 0005 this file runs the relaxed Qt profile — scoped to those
# stub-driven rules, not a blanket opt-out.
# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false, reportAttributeAccessIssue=false

import platform
from PySide6 import QtCore

from .. import resources
from .. import settings
from .. import terminals
from ..model import Tool


class ToolLauncher(QtCore.QObject):
    """Starts Tools as ``QProcess``es and reports what happened as log lines.

    Owns the running processes, keeping each one referenced until it finishes
    (or fails to start). Everything the user should see — the command, the
    merged stdout/stderr, a failure to start, the exit code — is emitted on
    ``log`` rather than written to a widget, so the launcher has no UI of its
    own; a silent launch failure is issue #7.
    """

    log = QtCore.Signal(str)

    def __init__(self, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._processes: list[QtCore.QProcess] = []


    def run(self, tool: Tool, open_shell: bool = False) -> None:
        """Launch ``tool``, or open a shell in its Rez environment."""
        self.log.emit(f'Running: {tool.title} {tool.subtitle}...')

        process = QtCore.QProcess(self)
        process.setProcessChannelMode(QtCore.QProcess.ProcessChannelMode.MergedChannels)
        process.readyReadStandardOutput.connect(lambda: self._read_output(process))

        def on_error(error: QtCore.QProcess.ProcessError) -> None:
            self._on_error(process, error)

        def on_finished(exit_code: int) -> None:
            self._on_finished(process, exit_code)

        process.errorOccurred.connect(on_error)
        process.finished.connect(on_finished)
        self._processes.append(process)

        if open_shell:
            # Pass the rez invocation as tokens (not a joined string): the seam
            # splices them into the chosen terminal's args template per its
            # placeholder. The terminal comes from the Settings store — unset
            # reproduces today's per-OS default (ticket 02, spec §3).
            rez_tokens = [resources.REZ_COMMAND, *tool.rez_wants]
            stored = settings.load_settings()
            program, arguments = terminals.shell_command(
                platform.system(),
                rez_tokens,
                stored.get("terminal_id"),
                stored.get("terminal_command"),
            )
        else:
            program, arguments = resources.launch_invocation(
                platform.system(), resources.REZ_COMMAND, tool.rez_wants, tool.command
            )
        self.log.emit(f'Command: {program} {" ".join(arguments)}')
        process.start(program, arguments)


    def _read_output(self, process: QtCore.QProcess) -> None:
        output = bytes(process.readAll().data()).decode(errors="replace").strip()
        if output:
            self.log.emit(output)


    def _on_error(self, process: QtCore.QProcess, error: QtCore.QProcess.ProcessError) -> None:
        if error == QtCore.QProcess.ProcessError.FailedToStart:
            # No finished signal follows a failed start, so clean up here.
            self.log.emit(
                f"Error: {process.program()} failed to start: {process.errorString()}"
            )
            self._processes.remove(process)
        else:
            self.log.emit(f"Error: {process.errorString()}")


    def _on_finished(self, process: QtCore.QProcess, exit_code: int) -> None:
        self._read_output(process)
        self.log.emit(f"Process finished (exit code {exit_code})")
        self._processes.remove(process)
