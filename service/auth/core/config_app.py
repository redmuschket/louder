from typing import Any, Optional
import importlib.util
from pathlib import Path


class ConfigAPP:
    def __init__(self):
        self._data = {}

    def from_pyfile(self, file_path: str | Path) -> None:
        file_path = Path(file_path)

        spec = importlib.util.spec_from_file_location("configs", file_path)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)

        self._data = {
            k: v for k, v in vars(config).items()
            if not k.startswith('_')
        }

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __contains__(self, key: str) -> bool:
        return key in self._data