from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Header
from uuid6 import UUID
import json
from sqlalchemy.orm import Session

from core.dto.user_file_id_pair import UserFileIDPair
from core.logger import Logger
from core.db.db import get_db
from core.depends.service import get_file_service
from app.services.file import FileService
from app.http.request_models.file import FileRequest, CreateFileRequest
from typing import Annotated, Optional

router = APIRouter(prefix="/api/v1/loader/file", tags=["Loader"])
logger = Logger.get_logger(__name__)
FileServiceDep = Annotated[FileService, Depends(get_file_service)]
DBDep = Annotated[Session, Depends(get_db)]


@router.post("/create")
async def create_file(
        file_request: CreateFileRequest,
        user_id: Annotated[str, Header(alias="X-User-Id")],
        db: DBDep):

    logger.debug(f"Request to create a file from user {user_id[:10]}")
    try:
        user_uid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid file ID format")

    try:
        success, file_uuid = await FileService.create_file(
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


@router.post("/upload")
async def upload_file(
        file: Annotated[UploadFile, File(...)],
        file_service: FileServiceDep,
):
    logger.debug(f"Request to upload a file from user")
    try:
        success, file_entity = await file_service.save_file(file)
        if success and file_entity:
            return {"file_uid": str(file_entity)}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save file"
            )
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during file upload"
        )