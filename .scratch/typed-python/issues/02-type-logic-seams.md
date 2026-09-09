# 02 — Type the logic seams and the Config boundary

Status: ready-for-agent

Fully type (strict-clean) `model.py`, `data.py`, and `resources/__init__.py`.

- `model.py`: `rez_wants: list[str]`; return types on the `title`/`tools`
  properties and `add_tool`. Remove the write-only `tool.job = self.job`
  propagation and its guard. `ToolSet.job` becomes `str | None` (drop the `""`
  sentinel in favour of `None`).
- `data.py`: declare `TypedDict`s for the raw Config shape (`ConfigDict`,
  `ToolSetDict` with `NotRequired[str]` job, `ToolDict`). `parse_config(config:
  ConfigDict) -> list[ToolSet]`. Remove the dead module global `apps`. Type
  `toolset_from_name` as `-> ToolSet | None` and `populate` as `-> None`.
- `resources/__init__.py`: type every function. `load_config() -> ConfigDict`
  via a `TYPE_CHECKING` import of `ConfigDict` from `.data` plus a string-form
  `cast` (avoids the data↔resources runtime import cycle). `config_path(system:
  str, environ: Mapping[str, str])`, `launch_command`, `shell_command ->
  tuple[str, list[str]]`, etc.
