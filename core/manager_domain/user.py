from typing import Dict
from core.domain.user import User
from core.manager_domain import *
from core.logger import Logger
from uuid6 import UUID

logger = Logger.get_logger(__name__)


class UserManagerDomain(ManagerDomain):
    _instance = None
    __user: Dict[UUID, User]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__user = {}
        return cls._instance

    def add(self, user: User):
        received_user = self.get(user.uid)
        if received_user is None:
            self.__user[user.uid] = user

    def get(self, user_uid: UUID) -> User | None:
        return self.__user.get(user_uid)

    def remove(self, user_uid: UUID):
        self.__user.pop(user_uid)

    def edit(self, user_uid: UUID, user: User):
        self.__user[user_uid] = user
