from uuid6 import UUID
from typing import Optional
import datetime


class User:
    def __init__(
            self,
            uid: UUID,
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None
    ):
        self._uid: UUID = uid
        self._dir: str = str(self._uid)
        self._created_at: datetime = created_at or datetime.now()
        self._updated_at: datetime = updated_at or datetime.now()

        self._validate_parameters()

    def _validate_parameters(self) -> None:
        """Validation of input parameters"""

        if not isinstance(self._uid, UUID):
            raise ValueError("UUID must be a valid UUID object")

        if self._uid.version not in 7:
            raise ValueError("Invalid UUID version")

    @property
    def dir(self) -> str:
        return self._dir

    @property
    def uid(self) -> UUID:
        return self._uid

    def __str__(self) -> str:
        return f"User(uid={self.uid})"

    def __repr__(self) -> str:
        return f"User(uid={self.uid})"

    def to_dict(self) -> dict:
        """Serializing an object into a dictionary"""
        return {
            'uid': str(self._uid),
            'directory': self._dir,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'File':
        """Creating a File object from a dictionary"""
        return cls(uid=UUID(data['uid']))
