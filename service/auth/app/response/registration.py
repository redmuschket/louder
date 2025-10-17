from pydantic import BaseModel, Field
from typing import Optional
from app.response.user import UserResponse


class RegistrationResponse(BaseModel):
    access: str
    refresh: str
    user: UserResponse
