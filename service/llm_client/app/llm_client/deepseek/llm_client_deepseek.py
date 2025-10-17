from abc import ABC

from app.llm_client.llm_client import LLMClient
from core.logger import Logger
from typing import Optional
from core.domain.deep_seek_client_context import DeepSeekClientContext
from core.manager_config.ai import AiManagerConfig

logger = Logger.get_logger(__name__)


class DeepSeekClient(LLMClient, ABC):

    def __init__(self, config_ai: AiManagerConfig):
        super().__init__(config_ai)
        self.__context: Optional[DeepSeekClientContext] = None
        self._validate()


    @property
    def context(self) -> Optional['DeepSeekClientContext']:
        return self.__context

    def _validate(self):
        try:
            self.__context = DeepSeekClientContext()

            success, token_or_error = self.config_ai.token
            if not success:
                logger.error("Failed DeepSeekClient to validate token_or_error")
                raise "Failed DeepSeekClient to validate token_or_error"
            else:
                self.context.token = token_or_error

            referer = self.config_ai.referer
            if not referer:
                logger.error("Failed to validate referer")
                raise "Failed to validate referer"
            else:
                self.context.referer = referer

            site_name = self.config_ai.site_name
            if site_name is None:
                logger.error("Failed to validate site_name")
                raise "Failed to validate site_name"
            else:
                self.context.site_name = site_name

            model = self.config_ai.model
            if model is None:
                logger.error("Failed to validate model")
                raise "Failed to validate model"
            else:
                self.context.model = model

            temperature = self.config_ai.temperature
            if temperature is None:
                logger.error("Failed to validate temperature")
                raise "Failed to validate temperature"
            else:
                self.context.temperature = temperature

            api_uri = self.config_ai.api_uri
            if api_uri is None:
                logger.error("Failed to validate api_uri")
                raise "Failed to validate api_uri"
            else:
                self.context.api_uri = api_uri
        except Exception as e:
            logger.error(f"Failed to validate DeepSeekClient error: {e}")
            raise Exception(f"Failed to validate DeepSeekClient error: {e}") from e