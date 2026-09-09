"""Seam A: launch-command construction.

Turning a Tool's ``rez_wants`` and ``command`` into the
``rez-env <rez_wants> -- <command>`` invocation is a pure function, so the exact
string the launcher runs is guarded here rather than tangled inside the UI.
"""

from toolbox import resources


def test_multiple_rez_wants_are_space_joined_before_the_command():
    command = resources.launch_command(
        "rez-env", ["maya-2025", "site", "deadline"], "maya"
    )
    assert command == "rez-env maya-2025 site deadline -- maya"


def test_single_rez_want():
    command = resources.launch_command("rez-env", ["maya-2025"], "maya")
    assert command == "rez-env maya-2025 -- maya"


def test_empty_rez_wants_still_launches_the_command():
    # No packages requested: the invocation is just the Rez command and the
    # target. This preserves the pre-refactor output exactly — the doubled space
    # where the empty want list used to sit is shell-equivalent to a single one.
    command = resources.launch_command("rez-env", [], "maya")
    assert command == "rez-env  -- maya"


def test_rez_command_is_a_parameter_not_hardcoded():
    # The Rez command is injected so the seam has no hidden dependency on how the
    # launcher happens to spell it today.
    command = resources.launch_command("/opt/rez/bin/rez-env", ["blender-4.5"], "blender")
    assert command == "/opt/rez/bin/rez-env blender-4.5 -- blender"
