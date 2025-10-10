from app.http.request_models.patent import PatentUUIDResponse
from app.services.token_introspection import TokenIntrospectionService
from app.services.analog.analog import PatentAnalogService
from core.domain.user_file_id_pair import UserPatentIDPair
from fastapi import APIRouter, HTTPException, Depends
from core.logger import Logger
from fastapi import APIRouter, HTTPException, Depends, Request, WebSocket, BackgroundTasks
from uuid6 import UUID
from core.manager_domain.user import UserManagerDomain, User
from core.connection_manager import get_connection_manager
import json
from fastapi.responses import Response, JSONResponse
from app.services.patent.patent import PatentService
from app.http.routes.route_methods import handle_background_task_request

router = APIRouter(prefix="/api/v1/loader", tags=["Loader"])
logger = Logger.get_logger(__name__)

@router.post("/upload")
async def create_file(
    file: Annotated[UploadFile, File(...)],
    user_uid_request: Annotated[str, Header(alias="X-User-Id")],
    db: Session = Depends(get_db)
):
    logger.debug(f"Request to add a file from user {user_uid}")
    try:
        file_service = FileService()
        success, file_entity = await file_service.save_file(user_uid_request, file, db)

        if success and file_entity:
            return {
                "message": "File uploaded successfully",
                "file_id": str(file_entity.uuid),
                "file_name": file_entity.file_name,
                "file_size": file_entity.file_size,
                "mime_type": file_entity.mime_type
            }
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