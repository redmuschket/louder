from pathlib import Path
from passlib.context import CryptContext
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.dto import TokenPair

from core.dto import UserCreate
from app.service.token import TokenService
from app.response.registration import UserResponse
from core.dto import RegistrationPair
from app.service.user import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    @staticmethod
    async def registration(
            dto: UserCreate,
            db: AsyncSession
    ) -> RegistrationPair:
        new_user = await UserService.create_user(dto, db)
        response_user = UserResponse(id=str(new_user.id), login=new_user.login)
        token = await TokenService.create_token(db, new_user.id, dto.device_id)
        return RegistrationPair(token=token, new_user=response_user)

    @staticmethod
    async def login(
            dto: UserCreate,
            db: AsyncSession
    ) -> RegistrationPair:
        new_user = await UserService.login(dto, db)
        response_user = UserResponse(id=str(new_user.id), login=new_user.login)
        token = await TokenService.create_token(db, new_user.id, dto.device_id)
        return RegistrationPair(token=token, new_user=response_user)

    @staticmethod
    async def update_access_token(refresh_token, db):
        return await TokenService.update_tokens(refresh_token, db)

    @staticmethod
    async def validate(access_token, db):
        return await TokenService.check_access_token(access_token, db)
