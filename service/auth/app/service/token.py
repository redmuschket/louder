from core.jwt_handler import JwtHandler
from typing import Tuple, Optional, Dict, Union
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, select
from typing import NamedTuple
from fastapi import Depends
from fastapi import Security, Depends, HTTPException, APIRouter
from datetime import timedelta, datetime, timezone
from sqlalchemy import update

from app.dto.token_pair import TokenPair
from app.dto.user import UserCreate
from core.db.db import get_db
from core.db.models.user import User
from core.db.models.token import Token
from passlib.context import CryptContext
from core.enum.token_frame import TokenFrame
from core.logger import Logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = Logger.get_logger(__name__)


class AccessError:
    @staticmethod
    def get_token_already_revoked_error():
        return HTTPException(
            status_code=401,
            detail="Token has been revoked. Please reauthenticate."
        )


class TokenService:

    @staticmethod
    async def create_token(db, user_id, device_id):
        access_token = JwtHandler.create_access_token({}, str(user_id), str(device_id))
        refresh_token = JwtHandler.create_refresh_token({}, str(user_id), str(device_id))
        await TokenService.__revoke_user_tokens(db, user_id, device_id)
        await TokenService.__save_token(db, user_id, device_id, refresh_token, "refresh")
        await TokenService.__save_token(db, user_id, device_id, access_token, "access")

        return TokenPair(access_token, refresh_token)

    @staticmethod
    async def check_access_token(access_token,  db: AsyncSession):
        token_type = JwtHandler.get_token_type(access_token)

        if token_type == 'access':
            payload = JwtHandler.validate_access_token(clear_token)
        else:
            raise HTTPException(status_code=400, detail="Invalid token type")

        if await TokenService.check_revoked(payload['jti'], db):
            raise AccessError.get_token_already_revoked_error()

        result = await db.execute(exists().where(User.id == payload['sub']))
        user = result.scalar()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return True

    @staticmethod
    async def update_tokens(refresh_token, db: AsyncSession):
        token_type = JwtHandler.get_token_type(refresh_token)
        logger.debug(f"up token type:{token_type}")
        if token_type == 'refresh':
            payload = JwtHandler.validate_refresh_token(refresh_token)
        else:
            raise HTTPException(status_code=400, detail="Invalid token type")
        logger.debug(f"up token :{payload}")
        if await TokenService.check_revoked(payload['jti'], db):
            await TokenService.revoke_token_family(payload['sub'], db)
            raise AccessError.get_token_already_revoked_error()

        user_id = payload['sub']
        device_id = payload['did']
        logger.debug(f"Request token data: {payload}")
        logger.debug(f"Revoke all keys to use: {user_id}")

        result = await db.execute(select(exists().where(User.id == user_id)))
        user_exists = result.scalar()
        if not user_exists:
            raise HTTPException(status_code=401, detail="User not found")

        await TokenService.mark_token_as_used(payload['jti'], db)

        await TokenService.__revoke_user_tokens(db, user_id, device_id)

        token_pair = await TokenService.create_token(db, user_id, device_id)

        return token_pair

    @staticmethod
    async def check_revoked(jti: str, db: AsyncSession) -> bool:
        query = await db.execute(
            select(Token.revoked).where(Token.jti == jti)
        )
        token_record = query.scalar_one_or_none()
        return token_record is not None and token_record.revoked

    @staticmethod
    async def revoke_token_family(user_id: str, db: AsyncSession):
        await db.execute(
            update(Token)
            .where(Token.user_id == user_id)
            .values(revoked=True)
        )
        await db.commit()

    @staticmethod
    async def mark_token_as_used(jti: str, db: AsyncSession):
        await db.execute(
            update(Token)
            .where(Token.jti == jti)
            .values(revoked=True)
        )
        await db.commit()

    @staticmethod
    async def __revoke_user_tokens(session, user_id, device_id):
        stmt = (
            update(Token)
            .where(
                (Token.user_id == user_id),
                (Token.device_id == device_id),
                (Token.revoked.is_(False))
            )
            .values(revoked=True)
        )
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def __save_token(db, user_id, device_id, token, type):
        expires_at = datetime.now() + timedelta(days=30)
        db_token = Token(
            token=token,
            user_id=user_id,
            expires_at=expires_at,
            device_id=device_id,
            token_type=type
        )

        db.add(db_token)
        await db.commit()
        await db.refresh(db_token)

        return db_token

    @staticmethod
    async def revoke_expired_tokens(db: AsyncSession):
        try:
            now = datetime.now()

            result = await db.execute(
                update(IssuedJWTToken)
                .where(
                    and_(
                        IssuedJWTToken.expires_at <= now,
                        IssuedJWTToken.revoked == False
                    )
                )
                .values(
                    revoked=True,
                    revoked_at=now,
                    revoked_reason="token_expired"
                )
            )

            await db.commit()

            expired_count = result.rowcount
            if expired_count > 0:
                logger.ingo(f"The token is rotten: {expired_count}")
            else:
                logger.ingo(f"No rotten tokens were found for review in {now}")
            return expired_count

        except Exception as e:
            await db.rollback()
            logger.error(f"Error when revoking expired tokens: {e}")
            return 0
