from typing import Optional
from uuid6 import uuid7, UUID
import datetime


class File:
    def __init__(
            self,
            name: str,
            uid: UUID,
            extension: Optional[str] = "",
            is_public: Optional[bool] = False,
            size: Optional[int] = 0,
            mime_type: Optional[str] = "",
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None
    ):
        self._uid: UUID = uid
        self._name: str = name
        self._dir: str = str(self._uid)
        self._extension: str = extension
        self._is_public: bool = is_public
        self._size: int = size
        self._mime_type: str = mime_type
        self._created_at: datetime = created_at or datetime.now()
        self._updated_at: datetime = updated_at or datetime.now()

        self._validate_parameters()

    def _validate_parameters(self) -> None:
        """Validation of input parameters"""
        if not self._name or not self._name.strip():
            raise ValueError("The file name cannot be empty")

        if not isinstance(self._uid, UUID):
            raise ValueError("UUID must be a valid UUID object")

        if self._uid.version not in 7:
            raise ValueError("Invalid UUID version")

        if not self._name or not self._name.strip():
            raise ValueError("The file name cannot be empty")

        if self._size < 0:
            raise ValueError("The file size cannot be negative")

    @property
    def name(self) -> str:
        return self._name

    @property
    def dir(self) -> str:
        return self._dir

    @property
    def uid(self) -> UUID:
        return self._uid

    @property
    def extension(self) -> str:
        return self._extension

    @property
    def is_public(self) -> bool:
        return self._is_public

    @property
    def size(self) -> int:
        return self._size

    @property
    def mime_type(self) -> str:
        return self._mime_type

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def filename(self) -> str:
        """Full file name with the extension"""
        if self._extension:
            return f"{self._name}.{self._extension}"
        else:
            return self._name

    @property
    def storage_filename(self) -> str:
        """File name for storage (using UUID)"""
        if self._extension:
            return f"{self._uid}.{self._extension}"
        else:
            return str(self._uid)

    @property
    def size_in_mb(self) -> float:
        return self._size / (1024 * 1024)

    @property
    def size_in_kb(self) -> float:
        return self._size / 1024

    def __str__(self) -> str:
        return f"File(name='{self.name}', uid={self.uid}, size={self.size} bytes)"

    def __repr__(self) -> str:
        return (f"File(name='{self.name}', uid={self.uid}, extension='{self.extension}', "
                f"is_public={self.is_public}, size={self.size}, mime_type='{self.mime_type}')")

    def to_dict(self) -> dict:
        """Serializing an object into a dictionary"""
        return {
            'name': self._name,
            'uid': str(self._uid),
            'directory': self._dir,
            'extension': self._extension,
            'is_public': self._is_public,
            'size': self._size,
            'mime_type': self._mime_type,
            'filename': self.filename,
            'path': self.path
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'File':
        """Creating a File object from a dictionary"""
        return cls(
            name=data['name'],
            uid=UUID(data['uid']),
            extension=data['extension'],
            is_public=data['is_public'],
            size=data['size'],
            mime_type=data['mime_type'],
        )