from uuid6 import uuid7
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
        nullable=False,
        unique=True
    )
    name = Column(String)
    role = Column(String)
    last_online = Column(DateTime(timezone=True))

    user_files = relationship(
        "UserFiles",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    files = relationship("File", secondary="user_files", viewonly=True)

    def __init__(self, ip: str = None):
        if ip is not None:
            self.ip = ip

    @property
    def get_uuid(self) -> uuid.UUID:
        return self.uuid

    @property
    def get_name(self) -> str:
        return self.name

    @property
    def get_role(self) -> str:
        return self.role

    @property
    def get_last_online(self) -> datetime:
        return self.last_online

    @name.setter
    def set_name(self, value: str):
        self.name = value

    @role.setter
    def set_role(self, value: str):
        self.role = value

    @last_online.setter
    def set_last_online(self, value: datetime):
        self.last_online = value


    def __repr__(self):
        return f"User(uuid={self.uuid}, name='{self.name}', ip='{self.ip}', role='{self.role}')"