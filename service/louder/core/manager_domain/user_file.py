from typing import Dict
from core.domain.user import User
from core.manager_domain import *
from core.logger import Logger
from uuid6 import UUID

logger = Logger.get_logger(__name__)


class UserFilesManagerDomain(ManagerDomain):
    """
    Singleton manager for handling file managers associated with users.

    Maintains a mapping between User objects and their corresponding
    FileManagerDomain instances using the Singleton pattern.

    Attributes:
        _instance: Single instance of the class (Singleton pattern)
        __users_files: Private dictionary mapping User to FileManagerDomain
    """

    _instance = None
    __users_files: Dict[User, FileManagerDomain]

    def __new__(cls):
        """
        Creates the single instance of the class (Singleton pattern).

        Returns:
            UserFilesManagerDomain: Single instance of the user files manager
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__users_files = {}
        return cls._instance

    def add(self, user_uid: UUID):
        """
        Adds a new file manager for a user.

        Args:
            user_uid: UUID identifier of the user

        Note:
            - Creates a new FileManagerDomain instance for the user
            - Does nothing if user doesn't exist or already has a file manager
        """
        user_manager = UserManagerDomain()  # Singleton class
        user = user_manager.get(user_uid)
        if user is None:
            logger.error(f"User not found in UserManagerDomain")
            return
        if user not in self.__users_files:
            self.__users_files[user] = FileManagerDomain()

    def get(self, user_uid: UUID) -> FileManagerDomain | None:
        """
        Retrieves the file manager for a user.

        Args:
            user_uid: UUID identifier of the user

        Returns:
            FileManagerDomain | None: File manager instance if found, otherwise None
        """
        user_manager = UserManagerDomain()  # Singleton class
        user = user_manager.get(user_uid)
        if user is None:
            logger.error(f"User {user_uid} not found in UserManagerDomain")
            return None
        return self.__users_files.get(user)

    def remove(self, user_uid: UUID, file_uid: UUID):
        """
        Removes a specific file from user's file manager.

        Args:
            user_uid: UUID identifier of the user
            file_uid: UUID identifier of the file to remove

        Note:
            - Only removes the file, not the entire file manager
            - Logs errors if user or file manager not found
        """
        user_manager = UserManagerDomain()  # Singleton class
        user = user_manager.get(user_uid)
        if user is None:
            logger.error(f"User {user_uid} not found in UserManagerDomain")
            return

        file_manager = self.__users_files.get(user)
        if file_manager is None:
            logger.error(f"File manager not found for user {user_uid}")
            return

        file_manager.remove(file_uid)

    def edit(self, user_uid: UUID, file_manager: FileManagerDomain):
        """
        Replaces the file manager for a user.

        Args:
            user_uid: UUID identifier of the user
            file_manager: New FileManagerDomain instance to associate with the user

        Note:
            - Overwrites existing file manager if user already has one
            - Creates new association if user doesn't have a file manager
        """
        user_manager = UserManagerDomain()  # Singleton class
        user = user_manager.get(user_uid)
        if user is None:
            logger.error(f"User {user_uid} not found in UserManagerDomain")
            return

        self.__users_files[user] = file_manager
