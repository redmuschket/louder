from typing import Optional
from uuid6 import UUID
from core import logger
from core.manager_config.service_client.user import UserServiceManagerConfig


class UserFileIDPair:
    def __init__(self, user_uid: UUID, file_uid: UUID):
        self._user_uid = user_uid
        self._file_uid = file_uid

        self._validate_parameters()

    def _validate_parameters(self) -> None:
        """Validation of input parameters"""

        if not isinstance(self._user_uid, UUID):
            raise ValueError("UUID must be a valid user UUID object")

        if self._user_uid.version not in 7:
            raise ValueError("Invalid user UUID version")

        if not isinstance(self._file_uid, UUID):
            raise ValueError("UUID must be a valid file UUID object")

        if self._file_uid.version not in 7:
            raise ValueError("Invalid file UUID version")

    @property
    def user_uid(self) -> UUID:
        return self._user_uid

    @property
    def file_uid(self) -> UUID:
        return self._file_uid
