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

router = APIRouter(prefix="/api/v1/loader", tags=["Loader"])
logger = Logger.get_logger(__name__)