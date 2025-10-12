from typing import Dict
from core.domain.file import File
from core.manager_domain import *
from uuid6 import UUID


class FileManagerDomain(ManagerDomain):
    """
    Manager for handling File objects in the domain layer.

    Provides centralized storage and management of File objects
    with basic CRUD operations. Each file is identified by a unique UUID.

    Attributes:
        __file: Private dictionary storing files {UUID: File}
    """

    def __init__(self):
        """Initializes the FileManagerDomain with an empty files dictionary."""
        self.__file: Dict[UUID, File] = {}

    def add(self, file: File):
        """
        Adds a new file to the manager.

        Args:
            file: File object to add to the manager

        Note:
            If a file with the same UUID already exists,
            the addition is silently ignored to prevent overwriting.
        """
        received_file = self.get(file.uid)
        if received_file is None:
            self.__file[file.uid] = file

    def get(self, file_uid: UUID) -> File | None:
        """
        Retrieves a file by its UUID.

        Args:
            file_uid: UUID identifier of the file

        Returns:
            File | None: File object if found, otherwise None
        """
        return self.__file.get(file_uid)

    def remove(self, file_uid: UUID):
        """
        Removes a file by its UUID.

        Args:
            file_uid: UUID identifier of the file to remove

        Raises:
            KeyError: If file with the specified UUID is not found
        """
        self.__file.pop(file_uid)

    def edit(self, file_uid: UUID, file: File):
        """
        Replaces a file with a new File object.

        Args:
            file_uid: UUID identifier of the file to replace
            file: New File object to store

        Note:
            - Overwrites existing file if file_uid exists
            - Adds new file if file_uid doesn't exist
            - Effectively performs an upsert operation
        """
        self.__file[file_uid] = file

    def list_uids(self) -> list[UUID]:
        """
        Returns list of all file UUIDs in the manager.

        Returns:
            list[UUID]: List of all file UUIDs
        """
        return list(self.__file.keys())

    def all(self) -> list[File]:
        """
        Returns list of all File objects in the manager.

        Returns:
            list[File]: List of all File objects
        """
        return list(self.__file.values())
