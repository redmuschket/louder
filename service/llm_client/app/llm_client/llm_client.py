from core.manager_config.ai import AiManagerConfig
from typing import Tuple
from abc import ABC, abstractmethod
from core.logger import Logger

logger = Logger.get_logger(__name__)

class LLMClient(ABC):
    def __init__(self, config_ai: AiManagerConfig):
        logger.debug(f"LLMClient init: config_ai={config_ai}")
        logger.debug(f"LLMClient init: config_ai is None: {config_ai is None}")

        self.__config_ai = config_ai

    @property
    def config_ai(self) -> AiManagerConfig:
        return self.__config_ai

    @abstractmethod
    async def ask(self, prompt) -> Tuple[bool, str]:
        pass

    async def validate_token(self) -> str:
        success, token_or_error = self.config_ai.token
        if not success:
            logger.error("Failed to validate token_or_error")
            raise Exception("Failed to validate token_or_error")
        else:
            return token_or_error

    async def validate_model(self) -> str:
        model = self.config_ai.model
        if model is None:
            logger.error("Failed to validate model")
            raise Exception("Failed to validate model")
        else:
            return model

    async def validate_temperature(self) -> str:
        temperature = self.config_ai.temperature
        if temperature is None:
            logger.error("Failed to validate temperature")
            raise Exception("Failed to validate temperature")
        else:
            return temperature

    async def validate_api_uri(self) -> str:
        api_uri = self.config_ai.api_uri
        if api_uri is None:
            logger.error("Failed to validate api_uri")
            raise Exception("Failed to validate api_uri")
        else:
            return api_uri

