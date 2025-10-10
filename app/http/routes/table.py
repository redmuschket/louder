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
from fastapi import BackgroundTasks
import json
from fastapi.responses import Response, JSONResponse
from app.services.patent.patent import PatentService
from app.http.routes.route_methods import reg, create_upidp, handle_file_request_analog

router = APIRouter(prefix="/api/v1/patent", tags=["Patent Analogs"])
logger = Logger.get_logger(__name__)

@router.get("/{patent_id}/analog/link/{type}")
async def get_link(
    patent_id: str,
    type: str,
    user_uid: str = Depends(TokenIntrospectionService.has_user_jwt)
):
    return await handle_file_request_analog(
        patent_id=patent_id,
        file_type=type,
        field_type="link",
        user_uid=user_uid,
    )

@router.get("/{patent_id}/analog/abstract_claims/{type}")
async def get_link(
    patent_id: str,
    type: str,
    user_uid: str = Depends(TokenIntrospectionService.has_user_jwt)
):
    return await handle_file_request_analog(
        patent_id=patent_id,
        file_type=type,
        field_type="abstract_claims",
        user_uid=user_uid,
    )

@router.get("/{patent_id}/analog/attributes/{type}")
async def get_link(
    patent_id: str,
    type: str,
    user_uid: str = Depends(TokenIntrospectionService.has_user_jwt)
):
    return await handle_file_request_analog(
        patent_id=patent_id,
        file_type=type,
        field_type="attributes",
        user_uid=user_uid,
    )

@router.get("/{patent_id}/analog/search/{type}")
async def get_link(
    patent_id: str,
    type: str,
    user_uid: str = Depends(TokenIntrospectionService.has_user_jwt)
):
    return await handle_file_request_analog(
        patent_id=patent_id,
        file_type=type,
        field_type="search",
        user_uid=user_uid,
    )

@router.get("/{patent_id}/analog/statistics/{type}")
async def get_link(
    patent_id: str,
    type: str,
    user_uid: str = Depends(TokenIntrospectionService.has_user_jwt)
):
    return await handle_file_request_analog(
        patent_id=patent_id,
        file_type=type,
        field_type="statistics",
        user_uid=user_uid,
    )

@router.get('/patent/{patent_id}/analogues/{type}')
async def get_analogues_csv(
        patent_id: str,
        type: str,
        user_uid: str = Depends(TokenIntrospectionService.has_user_jwt)
):
    return await handle_file_request_analog(
        patent_id=patent_id,
        file_type=type,
        field_type="analogues",
        user_uid=user_uid,
    )