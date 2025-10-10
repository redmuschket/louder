from uuid6 import uuid7
from sqlalchemy import Column, String, Boolean, BigInteger, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
import uuid

class File(Base):
    __tablename__ = "files"

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
        nullable=False
    )
    file_name = Column(String, nullable=False)
    file_extension = Column(String, nullable=False)
    is_public = Column(Boolean, nullable=False, default=False)
    file_size = Column(BigInteger, nullable=False)
    mime_type = Column(String, nullable=False)

    user_files = relationship(
        "UserFiles",
        back_populates="file",
        cascade="all, delete-orphan"
    )

    users = relationship("User", secondary="user_files", viewonly=True)

    def __init__(self, file_name: str, file_extension: str, is_public: bool,
                 file_size: int, mime_type: str, uuid: uuid.UUID = None):
        self.uuid = uuid or uuid7()
        self.file_name = file_name
        self.file_extension = file_extension
        self.is_public = is_public
        self.file_size = file_size
        self.mime_type = mime_type

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def file_extension(self):
        return self._file_extension

    @file_extension.setter
    def file_extension(self, value):
        self._file_extension = value

    @property
    def is_public(self):
        return self._is_public

    @is_public.setter
    def is_public(self, value):
        self._is_public = value

    @property
    def file_size(self):
        return self._file_size

    @file_size.setter
    def file_size(self, value):
        self._file_size = value

    @property
    def mime_type(self):
        return self._mime_type

    @mime_type.setter
    def mime_type(self, value):
        self._mime_type = value

    def __repr__(self):
        return f"File(uuid={self.uuid}, name='{self.file_name}.{self.file_extension}', size={self.file_size})"
