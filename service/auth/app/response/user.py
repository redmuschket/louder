from pydantic import BaseModel, Field
from typing import Optional


class UserResponse(BaseModel):
    id: str
    login: str

    class Config:
        from_attributes = True