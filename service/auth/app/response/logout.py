from pydantic import BaseModel, Field
from typing import Optional


class LogoutResponse(BaseModel):
    refresh_token: str