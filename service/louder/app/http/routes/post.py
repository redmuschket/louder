from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Header
from uuid6 import UUID
from sqlalchemy.orm import Session
from typing import Annotated

from core.data_mapper.files.file import FileMapper
from core.dto.user_file_id_pair import UserFileIDPair
from core.depends.domain import get_user_file_id_pair
from core.logger import Logger
from core.db.db import get_db
from core.depends.service import get_file_service
from app.services.file import FileService
from app.http.request_models.file import CreateFileRequest
from documentation.swagger.file.file_post import FileCreationResponses
from app.http.response_models.file import CreateFileResponse
from core.exceptions import *


router = APIRouter(prefix="/api/v1/loader/file", tags=["Loader"])
logger = Logger.get_logger(__name__)
FileServiceDep = Annotated[FileService, Depends(get_file_service)]
UserFileIDPairDep = Annotated[UserFileIDPair, Depends(get_user_file_id_pair)]
DBDep = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    summary="Create a new file",
    description="Creates a new file for the authenticated user and returns the file UUID",
    responses=FileCreationResponses.get_responses(),
    response_model=CreateFileResponse
)
async def create_file(
        file_request: CreateFileRequest,
        user_id: Annotated[str, Header(alias="X-User-Id")],
        fs: FileServiceDep):

    logger.debug(f"Request to create a file from user {user_id[:10]}")
    try:
        user_uid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid file ID format")

    try:
        file_uuid = await fs.create_file(
            file_name=file_request.file_name,
            user_uid=user_uid
        )

        if file_uuid:
            return CreateFileResponse(file_uid=str(file_uuid))
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create file in the system"
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid request data: {str(e)}"
        )

    except FileCreationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="File creation process failed"
        )

    except ServiceRepositoryError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Storage service temporarily unavailable"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during file creation"
        )


@router.post("/{file_uid}")
async def upload_file(
        file: Annotated[UploadFile, File(...)],
        fs: FileServiceDep,
        user_file_id_pair: UserFileIDPairDep
):
    logger.debug(f"Request to upload a file from user")
    try:
        file = await fs.save_file(user_file_id_pair, file)
        file = FileMapper.to_pydantic(file)
        return file
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during file upload"
        )