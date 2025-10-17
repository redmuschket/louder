from pydantic import BaseModel, Field
from typing import Optional

class RegistrationRequest(BaseModel):
    login: str = Field(..., min_length=1, description="The login must contain at least 1 character.")
    password: str = Field(..., min_length=1, description="The password must contain at least 1 character.")