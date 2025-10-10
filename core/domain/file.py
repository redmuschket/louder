from typing import Optional
from uuid6 import uuid7, UUID
from core.logger import Logger

logger = Logger.get_logger(__name__)

class File:
    def __init__(self, name: str, uid: UUID):
        self._uid: UUID = uid
        self._name: str = name
        self._dir: str = str(self._uid)


    @classmethod
    def create(cls, name: str, uid: UUID = None) -> Optional["File"]:
        if not name:
            logger.error("File name not valid")
            return None
        return cls(name, uid or uuid7())

    @property
    def name(self):
        return self._name

    @property
    def dir(self):
        return self._dir

    @property
    def uid(self):
        return self._uid

