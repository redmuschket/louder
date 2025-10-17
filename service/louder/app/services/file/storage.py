from core.domain.file import File
from core.logger import Logger
from app.services.storage import BaseStorageService
from core.dto.user_file_id_pair import UserFileIDPair

import aiofiles
from fastapi import UploadFile
from pathlib import Path


logger = Logger.get_logger(__name__)


class FileStorageService(BaseStorageService):
    def __init__(self):
        self._path_master = self.create_path_master()

    async def save_file(self, upload_file: UploadFile, file: File, user_file_id_pair: UserFileIDPair) -> bool:
        """
        Saves the file to disk

        Args:
            user_file_id_pair:
            upload_file: File to save
            file: The domain object of the metadata file

        Returns:
            bool: True if successful, False in case of error
        """
        file_path = self.get_file_path(file, user_file_id_pair)

        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            contents = await upload_file.read()

            async with aiofiles.open(file_path, "wb") as buffer:
                await buffer.write(contents)

            logger.debug(f"File saved successfully to {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save file to disk: {e}")
            return False

    def delete_file(self, file: File, user_file_id_pair: UserFileIDPair) -> bool:
        """
        Deleting a file

        Args:
            user_file_id_pair:
            file: The domain object of the file

        Returns:
            True if deleted successfully or the file does not exist
        """
        file_path = self.get_file_path(file, user_file_id_pair)
        return self._delete_file_by_path(file_path)

    def _delete_file_by_path(self, file_path: Path) -> bool:
        """
        Deleting a file by path

        Args:
            file_path: The full path to the file

        Returns:
            bool: True if deleted successfully or the file does not existт

        """
        try:
            if file_path.exists():
                file_path.unlink()
                logger.debug(f"File deleted: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False

    def get_file_path(self, file: File, user_file_id_pair: UserFileIDPair) -> Path:
        """Getting the path to save the file"""
        return self._path_master.get_path(
        "user_file",
            user_uid=user_file_id_pair.user_uid,
            file_uid=user_file_id_pair.file_uid,
            filename=file.storage_filename
        )
