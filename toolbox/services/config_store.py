from __future__ import annotations

import json
import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path


class ConfigStore(ABC):
    @abstractmethod
    def load(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def save(self, config_data: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def path(self) -> str | None:
        raise NotImplementedError


class JsonConfigStore(ConfigStore):
    def __init__(self, app_path: str | Path | None = None, env_var: str = "TOOLBOX_CONFIG") -> None:
        if app_path is None:
            app_path = Path(__file__).resolve().parents[2]
        self._app_path = Path(app_path)
        self._env_var = env_var
        self._config_file: Path | None = None

    def _resolve_config_file(self) -> Path:
        configured = os.environ.get(self._env_var)
        if configured:
            config_file = Path(os.path.expanduser(configured))
            if config_file.is_dir():
                config_file = config_file / "config.json"
        else:
            config_file = Path(os.path.expanduser("~/.config/toolbox/config.json"))
        return config_file

    def _default_config_file(self) -> Path:
        return self._app_path / "resources" / "default_config.json"

    def load(self) -> dict:
        config_file = self._resolve_config_file()
        if not config_file.is_file():
            config_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(self._default_config_file(), config_file)

        self._config_file = config_file
        with config_file.open("r", encoding="utf-8") as file_id:
            return json.load(file_id)

    def save(self, config_data: dict) -> None:
        if self._config_file is None:
            self._config_file = self._resolve_config_file()
        assert self._config_file is not None
        self._config_file.parent.mkdir(parents=True, exist_ok=True)
        with self._config_file.open("w", encoding="utf-8") as file_id:
            json.dump(config_data, file_id, indent=2)
            file_id.write("\n")

    def path(self) -> str | None:
        return str(self._config_file) if self._config_file is not None else None
