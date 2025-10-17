from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends

from core.db.db import get_db
from app.services.file import *

SessionDep = Annotated[AsyncSession, Depends(get_db)]

def get_file_service(db: SessionDep) -> FileService:
    ts = FileToolsService()
    return FileService(
        FileDataService(),
        ts,
        FileRepositoryService(db, ts),
        FileStorageService()
    )
