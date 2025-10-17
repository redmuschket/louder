from app.service.auth import AuthService
from fastapi import Security, Depends, HTTPException, APIRouter, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import UUID

from app.dto.user import *
from app.request import *
from app.response import *
from core.logger import Logger
from core.db.db import get_db

security = HTTPBearer()
router = APIRouter(prefix="/api/v1", tags=["Auth"])
logger = Logger.get_logger(__name__)


@router.post('/logout')
async def logout(request: LogoutRequest):
    pass

@router.get('/validate')
async def validate(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Authorization header required")

    if not credentials.scheme.lower() == "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")

    raw_token = credentials.credentials
    access_token = raw_token.strip()
    access_token = re.sub(r'[^A-Za-z0-9\-\._~\+/=]', '', access_token)

    try:
        result = await AuthService.update_access_token(access_token, db)
        if result:
            return Response(status_code=200)

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Refresh error: {e}")
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.post('/login')
async def login(
        request: Request,
        login_request: LoginRequest,
        db: AsyncSession = Depends(get_db)):
    device_id = request.headers.get("x-device-id")
    if not device_id or len(device_id) < 36:
        raise HTTPException(status_code=400, detail="Device ID is invalid")
    try:
        UUID(device_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Device ID is invalid")

    dto = UserCreate(device_id=device_id, login=login_request.login, password=login_request.password)

    registration_pair = await AuthService.login(dto, db)
    token_pair = registration_pair.token
    user = registration_pair.new_user

    return LoginResponse(user=user, access=token_pair.access_token, refresh=token_pair.refresh_token)

@router.post('/registration')
async def registration(
        request: Request,
        registration_request: RegistrationRequest,
        db: AsyncSession = Depends(get_db)):
    device_id = request.headers.get("x-device-id")
    if not device_id or len(device_id) < 36:
        raise HTTPException(status_code=400, detail="Device ID is invalid")
    try:
        UUID(device_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Device ID is invalid")

    dto = UserCreate(
        device_id=device_id,
        login=registration_request.login,
        password=registration_request.password)

    registration_pair = await AuthService.registration(dto, db)
    token_pair = registration_pair.token
    user = registration_pair.new_user

    return RegistrationResponse(user=user, access=token_pair.access_token, refresh=token_pair.refresh_token)


@router.post('/refresh')
async def refresh(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Authorization header required")

    if not credentials.scheme.lower() == "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")

    refresh_token = credentials.credentials

    try:
        token_pair = await AuthService.update_access_token(refresh_token, db)
        return UpAccessTokenResponse(
            access=token_pair.access_token,
            refresh=token_pair.refresh_token
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Refresh error: {e}")
        raise HTTPException(status_code=401, detail="Invalid refresh token")