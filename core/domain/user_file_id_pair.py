from typing import Optional
from uuid6 import UUID
from core import logger
from app.clients.user_client import UserClient
from core.manager_config.service_client.user import UserServiceManagerConfig


class UserFileIDPair:
    def __init__(self, user_uid: UUID, file_uid: UUID):
        if not isinstance(user_uid, UUID):
            raise TypeError("user_uid must be UUID")
        if not isinstance(file_uid, UUID):
            raise TypeError("file_uid must be UUID")
        self._user_uid = user_uid
        self._file_uid = file_uid

    @property
    def user_uid(self) -> UUID:
        return self._user_uid

    @property
    def file_uid(self) -> UUID:
        return self._file_uid
