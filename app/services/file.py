from pathlib import Path
from typing import Tuple, Dict, Optional
from sqlalchemy.orm import Session
from core.db.models.file import File
from core.db.models.user import User
from core.db.models.user_files import UserFiles
from app.services.path_master import PathMaster
from core.domain.user_file_id_pair import UserFileIDPair
from core.logger import Logger
from uuid6 import uuid7

logger = Logger.get_logger(__name__)


class FileService:
    def __init__(self):
        self._create_storage_directory()

    async def _get_path_master(self, user_file_id_pair) -> PathMaster:
        return PathMaster(user_file_id_pair)

    async def save_file(self, user_uid: UUID, file, db: Session) -> tuple[bool, File or None]:
        if not file or getattr(file, 'size', 0) == 0:
            logger.error("File cannot be null or empty")
            return False, None

        user = db.query(User).filter(User.uuid == user_uid).first()
        if not user:
            logger.error(f"User not found for UUID: {user_uid}")
            return False, None


        filename = getattr(file, 'filename', 'unknown')
        file_extension = ""
        if filename and "." in filename:
            file_extension = filename.split(".")[-1]

        content_type = getattr(file, 'content_type', 'application/octet-stream')
        file_size = getattr(file, 'size', 0)

        file_entity = File(
            file_name=filename,
            file_extension=file_extension,
            is_public=True,
            file_size=file_size,
            mime_type=content_type
        )

        db.add(file_entity)
        db.flush()

        file_uuid = file_entity.uuid

        user_file_id_pair = UserFileIDPair(
            user_uid=user_uid,
            file_uid=file_uuid
        )

        path_master = await self._get_path_master(user_file_id_pair)
        file_path = path_master.base_path

        try:
            contents = await file.read()
            with open(file_path, "wb") as buffer:
                buffer.write(contents)
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save file to disk: {str(e)}")
            return False, None

        user_file = UserFiles(user=user, file=file_entity)
        db.add(user_file)

        try:
            db.commit()
            db.refresh(file_entity)
        except Exception as e:
            db.rollback()

            if file_path.exists():
                file_path.unlink()
            logger.error(f"Failed to save file to database: {str(e)}")
            return False, None

        return True, file_entity
