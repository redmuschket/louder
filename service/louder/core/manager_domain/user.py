from typing import Dict
from core.domain.user import User
from core.manager_domain import *
from core.logger import Logger
from uuid6 import UUID

logger = Logger.get_logger(__name__)


class UserManagerDomain(ManagerDomain):
    """
    Singleton manager for user management in the domain layer.

    Provides centralized storage and management of User objects
    using the Singleton pattern. Each user is identified by a unique UUID.

    Attributes:
        _instance: Single instance of the class (Singleton pattern)
        __user: Private dictionary for storing users {UUID: User}
    """

    _instance = None
    __user: Dict[UUID, User]

    def __new__(cls):
        """
        Creates the single instance of the class (Singleton pattern).

        Returns:
            UserManagerDomain: Single instance of the user manager

        Note:
            Initializes the private users dictionary on first call.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__user = {}
        return cls._instance

    def add(self, user: User):
        """
        Adds a new user to the manager.

        Args:
            user: User object to add to the manager

        Note:
            If a user with the same UUID already exists, the addition is silently ignored.
            This prevents accidental overwriting of existing users.

        Example:
            >>> user_manager = UserManagerDomain()
            >>> user = User(name="John", uid=UUID("..."))
            >>> user_manager.add(user)
        """
        received_user = self.get(user.uid)
        if received_user is None:
            self.__user[user.uid] = user

    def get(self, user_uid: UUID) -> User | None:
        """
        Retrieves a user by their UUID.

        Args:
            user_uid: UUID identifier of the user

        Returns:
            User | None: User object if found, otherwise None
        """
        return self.__user.get(user_uid)

    def remove(self, user_uid: UUID):
        """
        Removes a user by their UUID.

        Args:
            user_uid: UUID identifier of the user to remove

        Raises:
            KeyError: If user with the specified UUID is not found

        Note:
            Uses dict.pop() which raises KeyError if key doesn't exist
        """
        self.__user.pop(user_uid)

    def edit(self, user_uid: UUID, user: User):
        """
        Edits or adds a user.

        Args:
            user_uid: UUID identifier of the user to edit
            user: User object to save

        Note:
            - If user with user_uid exists, it will be overwritten
            - If user doesn't exist, it will be added
            - Effectively performs an upsert operation (update + insert)
        """
        self.__user[user_uid] = user