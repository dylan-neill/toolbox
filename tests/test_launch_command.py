"""Seam A: launch-command construction.

Turning a Tool's ``rez_wants`` and ``command`` into the
``rez-env <rez_wants> -- <command>`` invocation is a pure function, so the exact
string the launcher runs is guarded here rather than tangled inside the UI.
"""

import pytest

from toolbox import resources


def test_multiple_rez_wants_are_space_joined_before_the_command() -> None:
    command = resources.launch_command(
        "rez-env", ["maya-2025", "site", "deadline"], "maya"
    )
    assert command == "rez-env maya-2025 site deadline -- maya"


def test_single_rez_want() -> None:
    command = resources.launch_command("rez-env", ["maya-2025"], "maya")
    assert command == "rez-env maya-2025 -- maya"


def test_empty_rez_wants_still_launches_the_command() -> None:
    # No packages requested: the invocation is just the Rez command and the
    # target. This preserves the pre-refactor output exactly — the doubled space
    # where the empty want list used to sit is shell-equivalent to a single one.
    command = resources.launch_command("rez-env", [], "maya")
    assert command == "rez-env  -- maya"


def test_rez_command_is_a_parameter_not_hardcoded() -> None:
    # The Rez command is injected so the seam has no hidden dependency on how the
    # launcher happens to spell it today.
    command = resources.launch_command("/opt/rez/bin/rez-env", ["blender-4.5"], "blender")
    assert command == "/opt/rez/bin/rez-env blender-4.5 -- blender"


# --- launch_invocation: the (program, args) QProcess.start runs ---------------


def test_macos_launch_runs_through_an_interactive_login_shell() -> None:
    # A Finder-launched .app inherits launchd's minimal PATH, so rez-env is not
    # found unless the user's shell profile is sourced (issue #7). The joined
    # rez invocation is a single token for -c.
    program, args = resources.launch_invocation(
        "Darwin", "rez-env", ["maya-2025", "site"], "maya"
    )
    assert program == "/bin/zsh"
    assert args == ["-lic", "rez-env maya-2025 site -- maya"]


@pytest.mark.parametrize("system", ["Windows", "Linux"])
def test_other_systems_launch_the_rez_invocation_directly(system: str) -> None:
    # Only macOS needs the login shell; elsewhere the rez invocation is the argv.
    program, args = resources.launch_invocation(
        system, "rez-env", ["maya-2025", "site"], "maya"
    )
    assert program == "rez-env"
    assert args == ["maya-2025", "site", "--", "maya"]
