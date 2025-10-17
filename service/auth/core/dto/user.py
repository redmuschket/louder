from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid6 import UUID


# User Schemas
class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    id: Optional[str] = None
    device_id: Optional[str] = None
    password: str