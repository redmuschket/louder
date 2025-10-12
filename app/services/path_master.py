from pathlib import Path
from core.dto.user_file_id_pair import UserFileIDPair
from core.manager_domain.user_file import UserFilesManagerDomain
from core.manager_domain.file import FileManagerDomain
from core.manager_domain.user import UserManagerDomain
from typing import Dict
from core import config

class PathMaster():
    def __init__(self, user_file_id_pair: UserFileIDPair):
        self._init_user_and_file(user_file_id_pair)
        self._load_config_paths({
            "file_path": "STORAGE_USER_FILE_PATH",
            "_user_data_dir": "STORAGE_USER_DATA_DIR",
        })
        self.base_path = Path(self._user_data_dir) / self.__user.dir / self.__file.dir

    def _init_user_and_file(self, user_file_id_pair: UserFileIDPair):
        if not user_file_id_pair or not isinstance(user_file_id_pair, UserFileIDPair):
            raise ValueError("Invalid user_file_id_pair provided")
        files: FileManagerDomain = UserFilesManagerDomain().get(user_file_id_pair.user_uid)
        if not files:
            raise ValueError("No files found for user")
        self.__file = files.get(user_file_id_pair.file_uid)
        if not self.__file:
            raise ValueError("File not found")
        self.__user = UserManagerDomain().get(user_file_id_pair.user_uid)
        if not self.__user:
            raise ValueError("User not found")
        if not self.__user.dir:
            raise ValueError("User directory not set")
        if not self.__file.dir:
            raise ValueError("File directory not set")

    def _load_config_paths(self, keys: Dict[str, str]):
        for attr, cfg_key in keys.items():
            val = config.get(cfg_key)
            if not val:
                raise ValueError(f"{cfg_key} not configured")
            setattr(self, attr, val)

