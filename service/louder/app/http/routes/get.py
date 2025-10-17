from core.dto.user_file_id_pair import UserFileIDPair
from core.logger import Logger
from core.manager_domain.user import UserManagerDomain, User
from app.services.file import FileService
from core.db.db import get_db
from core.data_mapper.files.files import FilesMapper
from core.domain.file import File
from app.http.response_models.file import FilesResponse
from core.exceptions import *
from documentation.swagger.file.files import FileResponses

from fastapi import APIRouter, HTTPException, Depends
from fastapi import Request, Header, status
from uuid6 import UUID
from typing import Annotated
import json
from sqlalchemy.ext.asyncio import AsyncSession

from core.depends.service import get_file_service

router = APIRouter(prefix="/api/v1/loader", tags=["Loader"])
logger = Logger.get_logger(__name__)
DBDep = Annotated[AsyncSession, Depends(get_db)]
FileServiceDep = Annotated[FileService, Depends(get_file_service)]


@router.get(
    "/file",
    summary="Get user files",
    description="Retrieve all files associated with the authenticated user",
    response_model=FilesResponse,
    responses=FileResponses.get_responses(),
    operation_id="get_user_files"
)
async def get_files(
        user_uid: Annotated[str, Header(alias="X-User-Id")],
        fs: FileServiceDep):
    logger.debug(f"Request to get a files from user {user_uid}")

    try:
        user_uid = UUID(user_uid)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid file ID format")

    try:
        # Getting files
        files: list[File] = await fs.get_files(user_uid)

        # If there are no files, we return an empty list.
        if not files:
            logger.info(f"No files found for user {str(user_uid)[:8]}")
            return FilesResponse(files={})

        # Conversion to response
        response: FilesResponse = FilesMapper.to_pydantic(files)
        logger.debug(f"Successfully retrieved {len(files)} files for user {str(user_uid)[:8]}")
        return response

    except FileGetError as e:
        logger.error(f"File service error for user {str(user_uid)[:8]}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Files not found or access denied"
        )
    except ServiceRepositoryError as e:
        logger.error(f"Database error for user {str(user_uid)[:8]}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Temporary service unavailable. Please try again later."
        )
    except ValueError as e:
        logger.error(f"Data validation error for user {str(user_uid)[:8]}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid data format"
        )
    except Exception as e:
        logger.error(f"Unexpected error getting files for user {str(user_uid)[:8]}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )