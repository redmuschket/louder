from uuid6 import UUID
from dataclasses import dataclass
from typing import ClassVar
from core import config

@dataclass(frozen=True)
class UserFileIDPair:
    """Immutable DTO for user-file association"""

    user_uid: UUID
    file_uid: UUID

    ALLOWED_UUID_VERSIONS: ClassVar[set] = config["USER_FILE_UUID_RESTRICTION"]

    def __post_init__(self):
        """Validation after initialization"""
        self._validate_uuids()

    def _validate_uuids(self) -> None:
        """Validate both UUIDs"""
        self._validate_uuid(self.user_uid, "user")
        self._validate_uuid(self.file_uid, "file")

    def _validate_uuid(self, uuid: UUID, entity_type: str) -> None:
        """Validate individual UUID"""
        if not isinstance(uuid, UUID):
            raise TypeError(f"{entity_type.capitalize()} UID must be UUID object")

        if uuid.version not in self.ALLOWED_UUID_VERSIONS:
            raise ValueError(
                f"Invalid {entity_type} UUID version {uuid.version}. "
                f"Allowed versions: {self.ALLOWED_UUID_VERSIONS}"
            )

    @classmethod
    def from_strings(cls, user_uid_str: str, file_uid_str: str) -> 'UserFileIDPair':
        """Alternative constructor from string representations"""
        try:
            user_uid = UUID(user_uid_str)
            file_uid = UUID(file_uid_str)
            return cls(user_uid, file_uid)
        except ValueError as e:
            raise ValueError(f"Invalid UUID string: {e}") from e
