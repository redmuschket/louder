from core.token_manager.token_manager import TokenManager
from typing import Tuple
from core.logger import Logger
import os

logger = Logger.get_logger(__name__)

class LLMClientServiceTokenManager(TokenManager):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_token(self) -> Tuple[bool, str]:
        token = self._read_secret_key()
        if token is not None:
            return True, token
        else:
            logger.error("LLMCLIENT_SERVICE_SECRET_KEY is not set!")
            return False, ""

    def _read_secret_key(self):
        logger.warning("Reading LLM Client Service secret key")
        key = os.getenv('LLMCLIENT_SERVICE_SECRET_KEY')
        return key
