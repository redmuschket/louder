from pydantic import BaseModel, Field
from typing import Optional

class UpAccessTokenRequest(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str