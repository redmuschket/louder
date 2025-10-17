from uuid6 import uuid7
from core.db.db import Base
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Token(Base):
    __tablename__ = "tokens"

    jti = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    token = Column(String, nullable=False, unique=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    device_id = Column(UUID(as_uuid=True), nullable=False, index=True, default=uuid7)
    revoked = Column(Boolean, default=False)
    token_type = Column(String)  # 'access' or 'refresh'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User", back_populates="tokens")