from pydantic import BaseModel, Field


class AskResponse(BaseModel):
    response: str
