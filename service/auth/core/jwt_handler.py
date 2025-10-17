from typing import Optional
from datetime import timedelta, datetime, timezone

import uuid6
from jose import jwt
import os
from typing import Any

from core.enum.token_frame import TokenFrame
from core import config

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(config.get("REFRESH_TOKEN_EXPIRE_MINUTES"))
JWT_ALGORITHM = config.get("JWT_ALGORITHM")


class JwtHandler:

    @staticmethod
    def create_access_token(
            data: dict[str, Any],
            subject: str,
            device_id: str,
            ttl: Optional[TokenFrame] = TokenFrame.DEFAULT):
        if ttl == TokenFrame.DEFAULT:
            ttl = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        else:
            ttl = None
        return JwtHandler.__sign_token("access", subject, device_id, data, ttl)

    @staticmethod
    def create_refresh_token(
            data: dict[str, Any],
            subject: str,
            device_id: str,
            ttl: Optional[TokenFrame] = TokenFrame.DEFAULT):
        if ttl == TokenFrame.DEFAULT:
            ttl = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        else:
            ttl = None
        return JwtHandler.__sign_token("refresh", subject, device_id, data, ttl)

    @staticmethod
    def __sign_token(
            type: str,
            subject: str,
            device_id: str,
            payload: dict[str, Any] = {},
            ttl: Optional[timedelta] = None) -> str:
        """
            Keyword arguments:
            type -- access/refresh;
            subject -- the entity to which the token is issued;
            payload -- the payload that you want to add to the token;
            ttl -- token lifetime
        """
        current_timestamp = datetime.now(timezone.utc)

        data = dict(
            iss='formula@auth_service',
            sub=subject,
            did=device_id,
            type=type,
            jti=str(uuid6.uuid7()),
            iat=current_timestamp,
            nbf=payload['nbf'] if payload.get('nbf') else current_timestamp,
        )
        if ttl:
            data['exp'] = data['nbf'] + ttl
        payload.update(data)

        return jwt.encode(payload, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str):
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload

    @staticmethod
    def get_token_type(token: str) -> str:
        try:
            payload = jwt.get_unverified_claims(token)
            return payload.get('type', 'access')
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    def validate_access_token(token: str) -> dict:
        payload = JwtHandler.decode_token(token)
        if payload.get('type') != 'access':
            raise HTTPException(status_code=401, detail="Access token required")
        return payload

    @staticmethod
    def validate_refresh_token(token: str) -> dict:
        payload = JwtHandler.decode_token(token)
        if payload.get('type') != 'refresh':
            raise HTTPException(status_code=401, detail="Refresh token required")
        return payload