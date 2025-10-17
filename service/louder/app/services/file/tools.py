from core.domain.file import File
from core.logger import Logger
from core.db.models.file import FileModel
from core.data_mapper.files.file import FileMapper
from core.dto.user_file_id_pair import UserFileIDPair
from core.db.models.user_files import UserFileModel
from core.exceptions import *

from fastapi import UploadFile
from pathlib import Path
from uuid6 import UUID
from typing import Union

logger = Logger.get_logger(__name__)


class FileToolsService:

    def extract_file_metadata(self, file: UploadFile, file_uid: UUID) -> File:
        """
        Extracts metadata from an uploaded file and creates a File domain object.

        Processes the uploaded file to extract:
        - File name
        - File extension
        - MIME type
        - File size

        Args:
            file_uid:
            file (UploadFile): The uploaded file object from FastAPI

        Returns:
            tuple[bool, File | None]:
                - bool: True if metadata ext_path_masterraction was successful
                - File: File domain object if successful, None if failed
        """
        file_name = getattr(file, 'filename', 'unknown')

        file_path = Path(file_name)
        if file_name and not file_name.startswith('.') and file_path.suffix:
            file_extension = file_path.suffix[1:].lower()
        else:
            file_extension = ""

        file_mime_type = getattr(file, 'content_type', 'application/octet-stream')
        file_size = getattr(file, 'size', 0)

        try:
            file = File(
                name=file_name,
                uid=file_uid,
                extension=file_extension,
                is_public=False,
                size=file_size,
                mime_type=file_mime_type
            )
            return file

        except Exception as e:
            logger.error(f"Error extract metadata from file: {e}")
            raise ServiceToolsError(f"Error extract metadata from file: {e}")

    def validate_upload_file(self, upload_file: UploadFile) -> bool:
        """Validation of the uploaded file"""
        if not upload_file or getattr(upload_file, 'size', 0) == 0:
            logger.error("File cannot be null or empty")
            return False
        return True

    def convert_to_file_model(self, file: Union[File, FileModel]) -> FileModel:
        """Convert input to FileModel with type safety"""
        if isinstance(file, FileModel):
            return file
        elif isinstance(file, File):
            return FileMapper.to_model(file)
        else:
            raise ValueError(f"Unsupported type: {type(file).__name__}")

    def convert_to_user_file_model(self, user_file_id_pair: Union[UserFileIDPair, UserFileModel]) -> UserFileModel:
        """Convert input to FileModel with type safety"""
        if isinstance(user_file_id_pair, UserFileIDPair):
            return user_file_id_pair
        elif isinstance(user_file_id_pair, UserFileModel):
            return FileMapper.to_model(user_file_id_pair)
        else:
            raise ValueError(f"Unsupported type: {type(user_file_id_pair).__name__}")