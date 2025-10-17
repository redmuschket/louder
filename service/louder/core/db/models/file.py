from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from uuid6 import uuid7
from sqlalchemy.orm import relationship
from core.db.db import Base


class FileModel(Base):
    __tablename__ = "file"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid7()),
        nullable=False
    )
    file_name = Column(String(255), nullable=False)
    file_extension = Column(String(50), nullable=False, default="")
    is_public = Column(Boolean, nullable=False, default=False)
    file_size = Column(BigInteger, nullable=False, default=0)
    mime_type = Column(String(100), nullable=False, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user_files = relationship("UserFileModel", back_populates="file", cascade="all, delete-orphan")

    def __repr__(self):
        return f"File(id={self.id}, name={self.file_name})"
