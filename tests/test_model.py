"""The Tool model's derived views: its display name and its package table.

Pure logic that used to sit inside the UI (the desktop-shortcut name and the
details panel's Package/Version rows), guarded here under strict typing.
"""

from toolbox.model import Tool


def _tool(subtitle: str = "", rez_wants: list[str] | None = None) -> Tool:
    return Tool("Maya", "2025", subtitle, rez_wants or [], "app_icon512.png", "maya")


def test_display_name_is_the_title_without_a_subtitle() -> None:
    assert _tool().display_name == "Maya 2025"


def test_display_name_puts_the_subtitle_in_parentheses() -> None:
    assert _tool("Redshift 2025.6").display_name == "Maya 2025 (Redshift 2025.6)"


def test_packages_split_each_want_at_the_first_hyphen() -> None:
    tool = _tool(rez_wants=["maya-2025", "site", "redshift-2025.6-beta"])
    assert tool.packages == [
        ("maya", "2025"),
        ("site", ""),
        ("redshift", "2025.6-beta"),
    ]


def test_no_wants_means_no_packages() -> None:
    assert _tool().packages == []
