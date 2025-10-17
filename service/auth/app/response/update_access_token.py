from pydantic import BaseModel, Field
from typing import Optional

class UpAccessTokenResponse(BaseModel):
    access: str
    refresh: str