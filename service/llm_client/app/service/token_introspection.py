from core.token_manager.service_client.llm_client_service import LLMClientServiceTokenManager
from core.manager_config.auth_user import AuthUserManagerConfig
from typing import Optional
from core.logger import Logger
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends

logger = Logger.get_logger(__name__)


class TokenIntrospectionService:
    _instance = None
    security = HTTPBearer()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def has_user_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
        config_manager = AuthUserManagerConfig()
        successful, jwt_secret_key = config_manager.token

        if not successful:
            logger.error("Get token failed")
            raise HTTPException(status_code=500, detail="JWT configuration error")
        input_token = credentials.credentials
        try:
            payload = jwt.decode(
                input_token,
                jwt_secret_key,
                algorithms=[config_manager.jwt_algorithm]
            )
            if "uuid" not in payload:
                logger.error("Invalid token format")
                raise HTTPException(status_code=401, detail="Invalid token format")
            return payload["uuid"]
        except JWTError:
            logger.error("Invalid or expired token")
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="JWT configuration erro")


    @staticmethod
    def has_service_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
        my_token = TokenIntrospectionService._get_service_key()
        input_token = credentials.credentials
        if my_token is not None:
            if input_token == my_token:
                return True
            else:
                logger.warning("Attempt to access with an invalid service token")
                raise HTTPException(status_code=500, detail="Attempt invalid token")
        else:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

    @staticmethod
    def _get_service_key() -> Optional[str]:  # Returns the hash of the key
        token_manager = LLMClientServiceTokenManager()
        successful, token = token_manager.get_token()
        if successful:
            return token
        else:
            logger.error("Failed to retrieve a token from the storage for validation")
            return None
