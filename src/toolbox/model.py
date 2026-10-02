from dataclasses import dataclass


@dataclass
class Tool():
    name: str
    version: str
    subtitle: str
    rez_wants: list[str]
    icon: str
    command: str

    @property
    def title(self) -> str:
        return f"{self.name} {self.version}"

    @property
    def display_name(self) -> str:
        """The title, with the subtitle in parentheses when there is one."""
        if self.subtitle:
            return f"{self.title} ({self.subtitle})"
        return self.title

    @property
    def packages(self) -> list[tuple[str, str]]:
        """Each Rez want as ``(package, version)``, split at the first hyphen.

        A want with no version (``"site"``) gets an empty version; anything
        after the first hyphen is the version, hyphens included.
        """
        return [
            (package, version)
            for package, _, version in (want.partition("-") for want in self.rez_wants)
        ]

@dataclass
class ToolSet():
    name: str
    description: str
    # An optional Rez context identifier for the group (see CONTEXT.md "Job").
    # None means "no job"; recorded intent only — not yet applied at launch.
    job: str | None
    _tools: list[Tool]

    @property
    def tools(self) -> list[Tool]:
        return self._tools

    def add_tool(self, tool: Tool) -> None:
        self._tools.append(tool)
