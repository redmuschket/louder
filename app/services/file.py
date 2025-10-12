from core.domain.file import File
from core.domain_mapper.file import FileMapper
from core.domain_mapper.user_files import UserFileIdMapper
from core.db.models.file import FileModel
from core.db.models.user_files import UserFileModel
from app.services.path_master import PathMaster
from core.dto.user_file_id_pair import UserFileIDPair
from core.logger import Logger
from app.services.user import UserService
from core.manager_domain.user_file import UserFilesManagerDomain
from core.manager_domain.user import UserManagerDomain
from core.manager_domain.file import FileManagerDomain
from core.domain.user import User
from fastapi import UploadFile

from uuid6 import uuid7, UUID
from pathlib import Path
from typing import Tuple, Dict, Optional
from sqlalchemy.orm import Session


logger = Logger.get_logger(__name__)


class FileService:
    def __init__(self, db: Session, path_master: PathMaster, user_file_id_pair: UserFileIDPair):
        self._db = db
        self._path_master = path_master
        self._user_file_id_pair = user_file_id_pair

    @staticmethod
    def create_base_file_domain(file_name: str) -> File:
        """
        Creates a domain object File with validation

        Args:
           file_name: File Name

        Returns:
           File: The created domain object

        Raises:
           ValueError: If the parameters are invalid
        :param file_name
        """
        try:
            return File(name=file_name, uid=uuid7())
        except Exception as e:
            logger.error(f"Error creating file '{file_name}': {e}")
            raise

    @staticmethod
    def create_base_user_files_domain(user_uid: UUID, file_uid: UUID) -> UserFileIDPair:
        """
        Creates a domain object UserFileIDPair with validation

        Args:
           user_file_id_pair: File Name

        Returns:
           File: The created domain object

        Raises:
           ValueError: If the parameters are invalid
           :param file_uid:
           :param user_uid:
        """
        try:
            return UserFileIDPair(
                user_uid=user_uid,
                file_uid=file_uid
            )
        except Exception as e:
            logger.error(f"Error creating user_file_id_pair '{str(user_uid)[:8]}', '{str(file_uid)[:8]}': {e}")
            raise

    @staticmethod
    def file_registration_in_domain_system(user: User, file: File) -> None:
        """
        Registers a file in the domain system for the specified user.

        This method adds the user to the domain manager, creates a user files manager,
        and registers the file with the appropriate file manager.

        Args:
            user (User): The user domain object to register
            file (File): The file domain object to register

        Note:
            This operation is performed after successful database persistence.
        """
        logger.debug(f"Registration in domain system{str(user.uid):8}")
        UserManagerDomain().add(user)
        UserFilesManagerDomain().add(user_uid=user.uid)
        file_manager = UserFilesManagerDomain().get(user_uid=user.uid)
        file_manager.add(file)

    @staticmethod
    def create_file(file_name: str, user_uid: UUID, db: Session) -> Tuple[bool, UUID | None]:
        """
        Creates a new file record in the database and registers it in the domain system.

        This method handles the complete file creation workflow including:
        - Domain object creation
        - Database persistence
        - Domain system registration

        Args:
            file_name (str): Name of the file to create
            user_uid (UUID): Unique identifier of the user owning the file
            db (Session): Database session for transaction management

        Returns:
            Tuple[bool, UUID | None]:
                - bool: True if file creation was successful, False otherwise
                - UUID: File UID if successful, None if failed

        Raises:
            Exception: Any exception during the creation process will be logged
                     and the transaction will be rolled back
        """
        logger.debug("Start file creation")
        try:
            # Creating domain objects
            file = FileService.create_base_file_domain(file_name)
            user = UserService.create_base_user_domain(user_uid)
            user_file_id_pair = FileService.create_base_user_files_domain(user_uid, file.uid)

            # Convert to DB models
            file_entity = FileMapper.to_model(file)
            user_files_entity = UserFileIdMapper.to_model(user_file_id_pair)

            db.add(file_entity)
            db.add(user_files_entity)

            db.commit()
            db.refresh(file_entity)
            db.refresh(user_files_entity)

            logger.debug("Finish file creation")
            logger.info(f"Successful creation of a file for the user {str(user_uid)[:8]}")

            # Register in the domain system
            FileService.file_registration_in_domain_system(user, file)

            return True, file.uid

        except Exception as e:
            logger.error(f"Error file creation: {e}")
            db.rollback()
            return False, None

    def _extract_file_metadata(self, file: UploadFile) -> tuple[bool, File | None]:
        """
        Extracts metadata from an uploaded file and creates a File domain object.

        Processes the uploaded file to extract:
        - File name
        - File extension
        - MIME type
        - File size

        Args:
            file (UploadFile): The uploaded file object from FastAPI

        Returns:
            tuple[bool, File | None]:
                - bool: True if metadata extraction was successful
                - File: File domain object if successful, None if failed
        """
        file_name = getattr(file, 'filename', 'unknown')

        file_path = Path(filename)
        if filename and not filename.startswith('.') and file_path.suffix:
            file_extension = file_path.suffix[1:].lower()
        else:
            file_extension = ""

        file_mime_type = getattr(file, 'content_type', 'application/octet-stream')
        file_size = getattr(file, 'size', 0)

        try:
            file = File(
                name=file_name,
                uid=self._user_file_id_pair.file_uid,
                extension=file_extension,
                is_public=False,
                size=file_size,
                mime_type=file_mime_type
            )
            return True, file
        except Exception as e:
            logger.error(f"Error extract metadata from file: {e}")
            return False, None

    async def save_file(self, upload_file: UploadFile) -> tuple[bool, Optional[UUID]]:
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
            upload_file (UploadFile): The file uploaded via FastAPI's UploadFile

        Returns:
            tuple[bool, Optional[UUID]]:
                - bool: True if file saving was successful, False otherwise
                - UUID: Unique identifier of the saved file if successful, None if failed

        Note:
            In case of failure during database operations, the file on disk will be
            automatically removed to maintain consistency.
        """
        if not upload_file or getattr(upload_file, 'size', 0) == 0:
            logger.error("File cannot be null or empty")
            return False, None

        success, file = self._extract_file_metadata(upload_file)

        if not success:
            return False, None

        file_entity = FileMapper.to_model(file)
        self._db.add(file_entity)
        self._db.flush()

        file_path = self._path_master.base_path / file.storage_filename

        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            contents = await upload_file.read()
            with open(file_path, "wb") as buffer:
                buffer.write(contents)
        except Exception as e:
            self._db.rollback()
            logger.error(f"Failed to save file to disk: {str(e)}")
            return False, None

        user_file_entity = UserFileIdMapper.to_model(self._user_file_id_pair)
        self._db.add(user_file_entity)

        try:
            self._db.commit()
            self._db.refresh(file_entity)
            self._db.refresh(user_file_entity)
        except Exception as e:
            self._db.rollback()

            if file_path.exists():
                file_path.unlink()
            logger.error(f"Failed to save file to database: {str(e)}")
            return False, None

        return True, file_entity.uid
