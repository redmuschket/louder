from core.token_manager.token_manager import TokenManager
from typing import Tuple
from core.logger import Logger
import os

logger = Logger.get_logger(__name__)

class JWTUserTokenManager(TokenManager):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_token(self) -> Tuple[bool, str]:
        token = JWTUserTokenManager._read_secret_key()
        if token is not None:
            return True, token
        else:
            logger.error("JWT_SECRET_KEY is not set!")
            return False, ""

    @staticmethod
    def _read_secret_key():
        logger.warning("Reading jwt secret key")
        key = os.getenv('JWT_SECRET_KEY')
        return key
