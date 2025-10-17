from pydantic import BaseModel, Field
from typing import Optional, Dict
from core.UUID6 import UUID6


class FileFieldsRequest(BaseModel):
    name: Optional[str] = None


class FileRequest(BaseModel):
    files: Dict[str, FileFieldsRequest]


class CreateFileRequest(BaseModel):
    file_name: str = Field(..., min_length=1, max_length=255, description="Name of the file to create")


class FileUUIDRequest(BaseModel):
    file_uuid: str
