from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
from core.UUID6 import UUID6
from uuid import UUID

class FileFieldsResponse(BaseModel):
    uid: UUID = Field(..., description="File UUID")
    name: str = Field(..., description="File name")
    extension: Optional[str] = Field("", description="File extension")
    is_public: Optional[bool] = Field(False, description="Is file public")
    size: Optional[int] = Field(0, description="File size in bytes")
    mime_type: Optional[str] = Field("", description="MIME type")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    filename: Optional[str] = Field(None, description="Full filename with extension")
    storage_filename: Optional[str] = Field(None, description="Storage filename with UUID")
    size_in_mb: Optional[float] = Field(None, description="File size in MB")
    size_in_kb: Optional[float] = Field(None, description="File size in KB")

class FilesResponse(BaseModel):
    files: Dict[UUID, FileFieldsResponse]


class CreateFileResponse(BaseModel):
    file_uid: str = Field(..., description="UUID of the created file")