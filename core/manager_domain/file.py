from typing import Dict
from core.domain.file import File
from core.manager_domain import *
from core.logger import Logger
from uuid6 import UUID

logger = Logger.get_logger(__name__)


class FileManagerDomain(ManagerDomain):
    def __init__(self):
        self.__file: Dict[UUID, File] = {}

    def add(self, file: File):
        received_file = self.get(file.uid)
        if received_file is None:
            self.__file[file.uid] = file

    def get(self, file_uid: UUID) -> File | None:
        return self.__file.get(file_uid)

    def remove(self, file_uid: UUID):
        self.__file.pop(file_uid)

    def edit(self, file_uid, file: File):
        self.__file[file_uid] = file

    def list_uids(self) -> list[UUID]:
        return list(self.__file.keys())

    def all(self) -> list[File]:
        return list(self.__file.values())
