from pydantic import BaseModel, Field
from typing import Optional, Dict
from core.UUID6 import UUID6


class FileFieldsRequest(BaseModel):
    name: Optional[str] = None


class FileRequest(BaseModel):
    patents: Dict[str, FileFieldsRequest]


class CreateFileRequest(BaseModel):
    file_name: str


class FileUUIDRequest(BaseModel):
    file_uuid: str
