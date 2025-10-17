from core.domain.file import File
from core.db.models.user_files import UserFileModel
from core.data_mapper.files.user_files import UserFileIdMapper
from core.data_mapper.files.file import FileMapper
from core.db.models.file import FileModel
from core.dto.user_file_id_pair import UserFileIDPair
from core.logger import Logger
from core.exceptions import *
from app.services.file.tools import FileToolsService

from sqlalchemy import select
from uuid6 import UUID
from sqlalchemy.orm import Session
from typing import overload, Union
from sqlalchemy.ext.asyncio import AsyncSession

logger = Logger.get_logger(__name__)


class RepositoryService:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def commit_transaction(self) -> None:
        """Fixing a transaction in the database"""
        try:
            await self._db.commit()
        except Exception as e:
            logger.error(f"Failed to commit transaction: {e}")
            raise ServiceRepositoryError(f"Database commit failed: {e}")

    async def rollback_db(self) -> None:
        """Rollback of a database transaction"""
        try:
            await self._db.rollback()
        except Exception as e:
            logger.error(f"Error during rollback: {e}")
            raise ServiceRepositoryError(f"Database rollback failed: {e}")