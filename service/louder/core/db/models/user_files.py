from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from uuid6 import uuid7
from sqlalchemy.orm import relationship
from core.db.db import Base

class UserFileModel(Base):
    __tablename__ = "user_files"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(36), nullable=False)
    file_id = Column(String(36), ForeignKey("file.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Uniqueness of the user_id + file_id pair
    __table_args__ = (
        UniqueConstraint('user_id', 'file_id', name='uq_user_file'),
    )

    file = relationship("FileModel", back_populates="user_files")

    def __repr__(self):
        return f"UserFile(user_id={self.user_id}, file_id={self.file_id})"