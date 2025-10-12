from uuid6 import uuid7
from sqlalchemy import Column, String, Boolean, BigInteger, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from core.db.db import Base


class FileModel(Base):
    __tablename__ = "file"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
        nullable=False
    )
    file_name = Column(String, nullable=False)
    file_extension = Column(String, nullable=False, default="")
    is_public = Column(Boolean, nullable=False, default=False)
    file_size = Column(BigInteger, nullable=False, default=0)
    mime_type = Column(String, nullable=False, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user_files = relationship("UserFiles", back_populates="file", cascade="all, delete-orphan")
