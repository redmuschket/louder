from pathlib import Path
from typing import Dict
from core import config
import yaml
from uuid6 import UUID

class PathMaster:
    def __init__(self):
        config_path = self._get_config_path()
        self._config = self._load_config(config_path)
        self.base_storage_path = Path(self._config['storage']['base_path'])
        self._path_templates = self._config['templates']

    @staticmethod
    def _get_config_path():
        return config.get("PATH_YAML_FILE")

    @staticmethod
    def _load_config(config_path: str) -> Dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_path(self, path_type: str, **kwargs) -> Path:
        if path_type not in self._path_templates:
            available_types = list(self._path_templates.keys())
            raise ValueError(f"Unknown path type: '{path_type}'. Available: {available_types}")

        template = self._path_templates[path_type]

        try:
            formatted_kwargs = {}
            for key, value in kwargs.items():
                if isinstance(value, UUID):
                    formatted_kwargs[key] = str(value)
                else:
                    formatted_kwargs[key] = value

            path_str = template.format(**formatted_kwargs)
            return self.base_storage_path / path_str

        except KeyError as e:
            raise ValueError(f"Missing parameter for template: {e}")
