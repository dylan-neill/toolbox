# PySide6's bundled 6.11 stubs under-type signals/slots and many overloads, and
# Qt getters that can return None (parent(), primaryScreen(), ...) make strict
# null-checking noisy on UI glue. Per ADR 0005 this file runs the relaxed Qt
# profile — scoped to those stub-driven rules, not a blanket opt-out.
# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false, reportAttributeAccessIssue=false, reportOptionalMemberAccess=false

import os
import platform
from collections.abc import Mapping
from PySide6 import QtWidgets

from .. import resources
from .. import settings
from .. import terminals

class SettingsDialog(QtWidgets.QDialog):
    """The modal **Settings** dialog (spec §4) — the UI face of the two settings
    wired in tickets 01 and 02.

    Two rows plus OK/Cancel: a **Config file** row (the current selected path, a
    **Browse…** for an existing ``.json``, a **Clear** that reverts to the
    default, and an inline note when ``TOOLBOX_CONFIG`` is overriding the
    setting), and an **Open Shell terminal** row (the OS's predefined terminals
    from the ``terminals`` registry + Custom, whose selection reveals program /
    arguments fields).

    The pure logic lives in the ``settings`` and ``terminals`` seams (tickets
    01/02); this dialog is the Qt glue that reads the store to seed its widgets
    and, on OK, does the **load-modify-write** back. ``system`` and ``environ``
    are injectable so the terminal registry and the override note are testable
    off the host OS; they default to the live platform and process environment.
    """

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        *,
        system: str | None = None,
        environ: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(parent)
        self._system = system if system is not None else platform.system()
        self._environ = environ if environ is not None else os.environ

        stored = settings.load_settings()
        # ``config_path`` as the setting sees it: a path string, or None for the
        # default. Captured at open so ``config_path_changed`` can tell the caller
        # whether a live reload is needed on OK.
        self._initial_config_path = stored.get("config_path")
        self._config_path: str | None = self._initial_config_path
        # Set by ``save`` (on OK) so ``on_settings_clicked`` knows to reload.
        self.config_path_changed = False

        self.setup_ui()
        self.load_from_settings(stored)


    def setup_ui(self) -> None:
        self.setWindowTitle("Settings")
        self.setModal(True)

        layout = QtWidgets.QVBoxLayout(self)
        self.form = QtWidgets.QFormLayout()
        layout.addLayout(self.form)

        # Config-file row: read-only path + Browse… + Clear.
        config_row = QtWidgets.QHBoxLayout()
        self.config_path_field = QtWidgets.QLineEdit()
        self.config_path_field.setReadOnly(True)
        self.config_path_field.setMinimumWidth(320)
        config_row.addWidget(self.config_path_field)
        self.browse_button = QtWidgets.QPushButton("Browse…")
        config_row.addWidget(self.browse_button)
        self.clear_button = QtWidgets.QPushButton("Clear")
        config_row.addWidget(self.clear_button)
        self.form.addRow("Config file", config_row)

        # Inline note shown only while TOOLBOX_CONFIG is overriding the setting.
        self.override_note = QtWidgets.QLabel(
            "TOOLBOX_CONFIG is set and is currently overriding this selection."
        )
        self.override_note.setWordWrap(True)
        self.form.addRow(self.override_note)

        # Open Shell terminal row: the OS's terminals + Custom.
        self.terminal_combo = QtWidgets.QComboBox()
        self.form.addRow("Open Shell terminal", self.terminal_combo)

        # Custom program / arguments, revealed only when Custom is selected.
        self.custom_program_field = QtWidgets.QLineEdit()
        self.form.addRow("Program", self.custom_program_field)
        self.custom_args_field = QtWidgets.QLineEdit()
        self.custom_args_field.setPlaceholderText("-e {command}")
        self.form.addRow("Arguments", self.custom_args_field)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        layout.addWidget(self.button_box)

        self.browse_button.clicked.connect(self.on_browse)
        self.clear_button.clicked.connect(self.on_clear)
        self.terminal_combo.currentIndexChanged.connect(
            self.update_custom_visibility
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)


    def load_from_settings(self, stored: settings.SettingsDict) -> None:
        """Seed the widgets from the store (spec §4)."""
        self.refresh_config_field()
        self.override_note.setVisible(bool(self._environ.get("TOOLBOX_CONFIG")))

        # The OS's predefined terminals in registry order, then Custom.
        for terminal_id, terminal in terminals.registry_for(self._system).items():
            self.terminal_combo.addItem(terminal.label, terminal_id)
        self.terminal_combo.addItem("Custom…", terminals.CUSTOM_TERMINAL_ID)

        # An unset terminal shows the OS default (today's behaviour); a stored id
        # selects that terminal. An unknown/stale stored id (e.g. a terminal from
        # another OS in a shared store) also falls back to the OS default rather
        # than leaning on index 0 — decoupled from the registry's ordering.
        terminal_id = stored.get("terminal_id") or terminals.default_terminal_id(
            self._system
        )
        index = self.terminal_combo.findData(terminal_id)
        if index < 0:
            index = self.terminal_combo.findData(
                terminals.default_terminal_id(self._system)
            )
        self.terminal_combo.setCurrentIndex(index)

        custom = stored.get("terminal_command")
        if custom:
            self.custom_program_field.setText(custom.get("program", ""))
            self.custom_args_field.setText(" ".join(custom.get("args", [])))

        self.update_custom_visibility()


    def refresh_config_field(self) -> None:
        """Show the selected path, or an empty field hinting the default when unset.

        A selected ``config_path`` shows as the field's text. When unset — the
        default, or after **Clear** — the field is left empty with the default
        location as greyed placeholder text. Two reasons: the user can tell "using
        the default" apart from an explicit pick (a real path shown as plain text
        would look identical to a selection), and Clear now visibly empties the
        field rather than swapping in another path-looking string. An empty
        ``environ`` is passed so the default shown is the true default,
        independent of any ``TOOLBOX_CONFIG`` override (which the note explains).
        """
        default = resources.config_path(self._system, {}, None)
        self.config_path_field.setPlaceholderText(f"Default: {default}")
        self.config_path_field.setText(self._config_path or "")


    def update_custom_visibility(self) -> None:
        """Reveal the Custom program/arguments fields only for the Custom entry.

        Resizes the dialog to fit afterwards: hiding the two rows shrinks the
        layout's size hint, but Qt does not pull an already-shown window back in
        on its own — without ``adjustSize`` the dialog keeps the taller height it
        grew to for Custom when switching back to a predefined terminal.
        """
        is_custom = (
            self.terminal_combo.currentData() == terminals.CUSTOM_TERMINAL_ID
        )
        self.form.setRowVisible(self.custom_program_field, is_custom)
        self.form.setRowVisible(self.custom_args_field, is_custom)
        self.adjustSize()


    def on_browse(self) -> None:
        """Pick an existing ``.json`` Config file (spec §4)."""
        start_dir = (
            os.path.dirname(self._config_path) if self._config_path else ""
        )
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Config file", start_dir, "Config files (*.json)"
        )
        if path:
            self._config_path = path
            self.refresh_config_field()


    def on_clear(self) -> None:
        """Revert to the default Config (removes ``config_path`` on save)."""
        self._config_path = None
        self.refresh_config_field()


    def save(self) -> None:
        """Load-modify-write the edited settings (spec §4).

        Re-reads the store immediately before writing so a partial update never
        clobbers keys another writer touched while the dialog was open (e.g. the
        silently-persisted ``window_geometry`` / ``last_toolset``). Clearing the
        Config path removes the key entirely rather than storing an empty string,
        so resolution falls through to the default. ``config_path_changed`` is
        set for the caller's live-reload decision.
        """
        stored = settings.load_settings()

        if self._config_path:
            stored["config_path"] = self._config_path
        else:
            stored.pop("config_path", None)

        terminal_id = self.terminal_combo.currentData()
        stored["terminal_id"] = terminal_id
        if terminal_id == terminals.CUSTOM_TERMINAL_ID:
            stored["terminal_command"] = {
                "program": self.custom_program_field.text(),
                # Whitespace-split into argv templates; a bare ``{command}``
                # becomes its own element and expands to the rez tokens (spec §3).
                "args": self.custom_args_field.text().split(),
            }
        else:
            stored.pop("terminal_command", None)

        settings.save_settings(stored)

        self.config_path_changed = (self._config_path or None) != (
            self._initial_config_path or None
        )


    def accept(self) -> None:
        """OK: persist the settings, then close (Cancel/``reject`` writes nothing)."""
        self.save()
        super().accept()
