from core.domain.file import File
from core.logger import Logger
from app.services.user import UserService
from fastapi import UploadFile
from app.services.file import *
from core.dto.user_file_id_pair import UserFileIDPair
from core.exceptions import *

from uuid6 import uuid7, UUID
from typing import Tuple, Optional
from sqlalchemy.orm import Session


logger = Logger.get_logger(__name__)


class FileService:
    def __init__(self,
                 ds: FileDataService,
                 ts: FileToolsService,
                 rs: FileRepositoryService,
                 ss: FileStorageService,):
        self._data_service = ds
        self._tools_service = ts
        self._repository_service = rs
        self._storage_service = ss

    async def create_file(self, file_name: str, user_uid: UUID) -> UUID:
        """
        Creates and persists a new file for the given user.

        Workflow:
            1. Create base file domain object
            2. Create user-file association
            3. Persist both to database within a transaction

        Args:
            file_name (str): Name of the file to create.
            user_uid (UUID): Unique identifier of the user.

        Returns:
            UUID: The unique ID of the created file.

        Raises:
            FileCreationError: If any part of the file creation process fails.
        """

        logger.debug("Start file creation")
        try:
            # Creating data objects
            file = self._data_service.create_base_file_domain(file_name)
            user_file_id_pair = self._data_service.create_base_user_files_dto(user_uid, file.uid)

            # Save to database using repository service
            await self._repository_service.save_file_to_db(file)
            await self._repository_service.save_user_file_association(user_file_id_pair)

            # Commit transaction
            await self._repository_service.commit_transaction()

            logger.debug(f"Successful creation of a file for the user {str(user_uid)[:8]}")

            return file.uid

        except Exception as e:
            await self._repository_service.rollback_db()
            logger.error(f"File creation failed: {str(e)}")
            raise FileCreationError(f"Error during file creation: {e}") from e

    async def save_file(self, user_file_id_pair: UserFileIDPair, upload_file: UploadFile) -> File:
        """
        Saves an uploaded file to disk and persists file metadata to the database.

        This method performs the complete file saving workflow:
        1. Validates the uploaded file
        2. Extracts file metadata
        3. Saves file to disk storage
        4. Persists file metadata to database
        5. Creates user-file association

        The file is stored using UUID-based filename for security and uniqueness.

        Args:
            user_file_id_pair:
            upload_file (UploadFile): The file uploaded via FastAPI's UploadFile

        Returns:
            tuple[bool, Optional[UUID]]:
                - bool: True if file saving was successful, False otherwise
                - UUID: Unique identifier of the saved file if successful, None if failed

        Note:
            In case of failure during database operations, the file on disk will be
            automatically removed to maintain consistency.
        """

        logger.debug(f"Start saving file for user {str(user_file_id_pair.user_uid)[:8]}")
        try:
            success = self._tools_service.validate_upload_file(upload_file)
            if not success:
                raise ValidationError(f"Error during file validation")

            file = self._tools_service.extract_file_metadata(upload_file, user_file_id_pair.file_uid)
            logger.debug(f"File ID before save: {file.uid}, expected: {user_file_id_pair.file_uid}")
            await self._repository_service.update_file_in_db(file)

            success = await self._storage_service.save_file(upload_file, file, user_file_id_pair)
            if not success:
                await self._repository_service.rollback_db()
                raise

            await self._repository_service.commit_transaction()

            logger.debug(f"Success saving file for user {str(user_file_id_pair.user_uid)[:8]}")
            return file
        except Exception as e:
            logger.error(f"Error during file saving: {e}")
            raise FileCreationError(f"Error during file saving: {e}")

    async def get_files(self, user_uid: UUID):
        """
        Retrieves all files associated with the specified user.

        This method serves as the main entry point for fetching user files from the database.
        It handles the business logic for file retrieval and error handling.

        Workflow:
            1. Log the start of the operation for debugging purposes
            2. Delegate to repository service to fetch files from database
            3. Log successful retrieval
            4. Return list of File domain objects
            5. Handle any exceptions and convert to domain-specific error

        Args:
            user_uid (UUID): Unique identifier of the user whose files to retrieve.
                            Must be a valid UUID.

        Returns:
            list[File]: List of File domain objects associated with the user.
                       Returns empty list if no files are found.

        Raises:
            FileGetError: If any error occurs during the file retrieval process.
                         This includes database errors, connection issues, or
                         any other unexpected exceptions.

        Example:
            >>> user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
            >>> files = file_service.get_files(user_id)
            >>> len(files)
            3

        Notes:
            - The method uses debug logging for tracking operation flow
            - Errors are logged with full exception details for debugging
            - Returns domain objects, not database entities
            - Empty list is returned when user has no files (no exception thrown)
        """
        logger.debug(f"Start get files for user {str(user_uid)[:8]}")
        try:
            files: list[File] = await self._repository_service.get_files_by_user_id(user_uid)
            logger.debug(f"Successful creation of a file for the user {str(user_uid)[:8]}")
            return files
        except Exception as e:
            logger.error(f"Failed to get files for user: {e}")
            raise FileGetError(f"Error during get files for user: {e}")
