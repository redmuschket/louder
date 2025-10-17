from pydantic import BaseModel, Field
from typing import Optional

class LogoutRequest(BaseModel):
    refresh_token: str