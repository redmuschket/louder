from app.services.token_introspection import TokenIntrospectionService
from fastapi import APIRouter, HTTPException, Depends
from core.logger import Logger
from fastapi import APIRouter, HTTPException, Depends, Request, WebSocket, BackgroundTasks
from uuid6 import UUID
from core.manager_domain.user import UserManagerDomain, User
from core.connection_manager import get_connection_manager
import json
from fastapi.responses import Response, JSONResponse
from typing import Tuple, Optional
from core.logger import Logger
from core.domain.user_file_id_pair import UserFileIDPair

logger = Logger.get_logger(__name__)

async def reg(message: str, user_uid: str):
    user = User(user_uid)
    UserManagerDomain().add(user)
    logger.info(message)
    user_file = await FileService.get_files(user_uid)
    logger.debug(user_patents)

async def create_upidp(user_id, file_id):
    try:
        user_uid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user uid")

    try:
        file_uid = UUID(file_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid patent id")

    user = User(user_uid)
    if UserManagerDomain().get(user_uid) is None:
        UserManagerDomain().add(user)
    return UserFileIDPair(
        user_uid=user_uid,
        file_uid=file_uid)

