from core.domain.file import File
from core.db.models.user_files import UserFileModel
from core.data_mapper.files.user_files import UserFileIdMapper
from core.data_mapper.files.file import FileMapper
from core.db.models.file import FileModel
from core.dto.user_file_id_pair import UserFileIDPair
from core.logger import Logger
from core.exceptions import *
from app.services.file.tools import FileToolsService
from app.services.repository import RepositoryService

from sqlalchemy import select
from uuid6 import UUID
from sqlalchemy.orm import Session
from typing import overload, Union
from sqlalchemy.ext.asyncio import AsyncSession

logger = Logger.get_logger(__name__)


class FileRepositoryService(RepositoryService):
    def __init__(self, db: AsyncSession, ts: FileToolsService):
        super().__init__(db = db)
        self._tool_service = ts

    @overload
    async def save_user_file_association(self, user_file_id_pair: UserFileIDPair) -> UserFileModel:
        ...

    @overload
    async def save_user_file_association(self, user_file_id_pair: UserFileModel) -> UserFileModel:
        ...

    async def save_user_file_association(self, user_file_id_pair: Union[UserFileIDPair, UserFileModel]) -> UserFileModel:
        """Create user-file association and return saved entity

        Args:
            user_file_id_pair: Either DTO or Model for user-file association

        Returns:
            UserFileModel: The saved association entity

        Raises:
            ServiceRepositoryError: If database operation fails
        """
        try:
            user_file_entity = UserFileIdMapper.to_model(user_file_id_pair)
            self._db.add(user_file_entity)
            return user_file_entity
        except Exception as e:
            logger.error(f"Failed to save user-file association: {e}")
            raise ServiceRepositoryError(f"Database save failed: {e}")

    @overload
    async def save_file_to_db(self, file: File) -> FileModel:
        ...

    @overload
    async def save_file_to_db(self, file: FileModel) -> FileModel:
        ...

    async def save_file_to_db(self, file: Union[File, FileModel]) -> FileModel:
        """Saving a file to a database with flexible input

        Args:
            file: Either File domain object or FileModel entity

        Raises:
            ServiceRepositoryError: If database operation fails
            ValueError: If unsupported type provided
        """
        try:
            file_entity = self._tool_service.convert_to_file_model(file)
            self._db.add(file_entity)
            return file_entity
        except ValueError as e:
            logger.error(f"Invalid file type: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to save file to database: {e}")
            raise ServiceRepositoryError(f"Database save failed: {e}")

    async def get_files_by_user_id(self, user_id: UUID) -> list[File]:
        """Get all files for specific user"""
        try:
            stmt = (
                select(FileModel)
                .join(UserFileModel, FileModel.id == UserFileModel.file_id)
                .where(UserFileModel.user_id == user_id)
            )

            result = await self._db.execute(stmt)
            file_models = result.scalars().all()

            files = [FileMapper.to_domain(file_model) for file_model in file_models]
            return files

        except Exception as e:
            logger.error(f"Failed to get files for user {str(user_id)[:8]}: {e}")
            raise ServiceRepositoryError(f"Database query failed: {e}")

    async def get_file_by_id(self, file_id: UUID) -> File:
        """Get file by ID"""
        try:
            stmt = select(FileModel).where(FileModel.id == file_id)
            result = await self._db.execute(stmt)
            file_model = result.scalar_one_or_none()

            if not file_model:
                raise FileNotFoundError(f"File with id {file_id} not found")

            return FileMapper.to_domain(file_model)

        except FileNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to get file {file_id}: {e}")
            raise ServiceRepositoryError(f"Database query failed: {e}")

    @overload
    async def update_file_in_db(self, file: File) -> FileModel:
        ...

    @overload
    async def update_file_in_db(self, file: FileModel) -> FileModel:
        ...

    async def update_file_in_db(self, file: Union[File, FileModel]) -> FileModel:
        """Updating a file in the database"""
        try:
            file_entity = self._tool_service.convert_to_file_model(file)

            await self._db.merge(file_entity)
            await self._db.flush()

            logger.debug(f"Файл {file.uid} обновлен в базе")
            return file_entity

        except Exception as e:
            logger.error(f"Error updating a file in the database: {e}")
            raise ServiceRepositoryError(f"File update error: {e}")