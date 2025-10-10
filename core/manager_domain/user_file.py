from typing import Dict
from core.domain.user import User
from core.manager_domain import *
from core.logger import Logger
from uuid6 import UUID

logger = Logger.get_logger(__name__)


class UserFilesManagerDomain(ManagerDomain):
    _instance = None
    __users_files: Dict[User, FileManagerDomain]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__users_files = {}
        return cls._instance
    
    def add(self, user_uid: UUID):
        user_manager = UserManagerDomain()  # Singleton class
        user = user_manager.get(user_uid)
        if user is None:
            logger.error(f"User not found in UserManagerDomain")
            return
        if user not in self.__users_files:
            self.__users_files[user] = FileManagerDomain()
            
    def get(self, user_uid: UUID) -> FileManagerDomain | None:
        user_manager = UserManagerDomain()  # Singleton class
        user = user_manager.get(user_uid)
        if user is None:
            logger.error(f"User {user_uid} not found in UserManagerDomain")
        return self.__users_files.get(user)

    def remove(self, user_uid: UUID, file_uid: UUID):
        user_manager = UserManagerDomain()  # Singleton class
        user = user_manager.get(user_uid)
        file_manager = self.__users_files.get(user)
        file_manager.remove(file_uid)

    def edit(self, user_uid: UUID, file_manager: FileManagerDomain):
        user_manager = UserManagerDomain()  # Singleton class
        user = user_manager.get(user_uid)
        self.__users_files[user] = file_manager

