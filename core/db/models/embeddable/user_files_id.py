from uuid6 import uuid7
from core.db.db import Base
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class UserFilesId(Base):
    __tablename__ = "user_files"

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    file_id = Column(UUID(as_uuid=True), primary_key=True)

    def __init__(self, user_id: uuid.UUID, file_id: uuid.UUID):
        self.user_id = user_id
        self.file_id = file_id

    def __eq__(self, other):
        if not isinstance(other, UserFilesId):
            return False
        return self.user_id == other.user_id and self.file_id == other.file_id

    def __hash__(self):
        return hash((self.user_id, self.file_id))

    def __repr__(self):
        return f"UserFilesId(user_id={self.user_id}, file_id={self.file_id})"