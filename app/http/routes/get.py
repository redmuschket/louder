from core.dto.user_file_id_pair import UserFileIDPair
from core.logger import Logger
from core.manager_domain.user import UserManagerDomain, User
from app.services.file import FileService
from core.db.db import get_db

from fastapi import APIRouter, HTTPException, Depends
from fastapi import Request, Header
from uuid6 import UUID
from typing import Annotated
import json
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/v1/loader", tags=["Loader"])
logger = Logger.get_logger(__name__)
DBDep = Annotated[Session, Depends(get_db)]


@router.post("/get")
async def get_files(
        user_uid: Annotated[str, Header(alias="X-User-Id")],
        db: DBDep):

    logger.debug(f"Request to get a files from user {user_uid}")
    try:
        user_uid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid file ID format")

    try:
        success, files = await FileService.create_file(
            file_name=file_request.file_name,
            user_uid=user_uid,
            db=db
        )

        if success and file_uuid:
            return {"file_uid": str(file_uuid)}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create file"
            )

    except Exception as e:
        logger.error(f"Error create file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during file create"
        )
