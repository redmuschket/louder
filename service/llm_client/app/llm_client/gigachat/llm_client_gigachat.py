from abc import ABC
from app.llm_client.llm_client import LLMClient
from core.logger import Logger
from typing import Optional
from core.domain.gigachat_client_context import GigachatClientContext
from core.manager_config.ai import AiManagerConfig

logger = Logger.get_logger(__name__)


class GigachatClient(LLMClient, ABC):

    def __init__(self, config_ai: AiManagerConfig):
        super().__init__(config_ai)
        self.__context: Optional[GigachatClientContext] = None

    @property
    def context(self) -> Optional['GigachatClientContext']:
        return self.__context

    async def initialize(self):
        await self._validate()

    async def _validate(self):
        try:
            self.__context = GigachatClientContext()
            self.context.token = await self.validate_token()
            self.context.model = await self.validate_model()
            self.context.temperature = await self.validate_temperature()

            self.context.api_uri = await self.validate_api_uri()
        except Exception as e:
            logger.error(f"Failed to validate GigachatClient: {e}")
            raise