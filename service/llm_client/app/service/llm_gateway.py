from core.logger import Logger
from core.domain.purpose_prompt import PurposePrompt
from core.manager_domain.user import UserManagerDomain
from core.domain.user import User
from core.enum.model_provider import ModelProvider
from core.manager_domain.user_ai_config import UserAIConfigManagerDomain
from app.llm_client import LLMClient, YandexClient
from app.llm_client import DeepSeekWSClient,DeepSeekHTTPClient
from app.llm_client import GigachatHTTPClient, GigachatWSClient
from typing import Tuple, Optional
from core.manager_config.ai import AiManagerConfig
from fastapi import HTTPException

logger = Logger.get_logger(__name__)

class LLMGateway:

    def __init__(self):
        self.__context = None

    @property
    def context(self) -> Optional['_LLMGatewayContext']:
        return self.__context

    async def ask(self, purpose_prompt: PurposePrompt) -> Tuple[bool, str]:
        logger.debug(f"___Star LLMGateway ask___")
        await self._domain_authorization(purpose_prompt)
        client = await self._get_client()
        return await client.ask(purpose_prompt.prompt)

    async def ws_ask(self, chat_id, purpose_prompt: PurposePrompt):
        logger.debug(f"___Star LLMGateway ws_ask___")
        await self._domain_authorization(purpose_prompt)
        client = await self._get_client(
            chat_id=chat_id,
            ws=True
        )
        await client.ask(purpose_prompt.prompt)

    async def _get_client(self, chat_id="", ws = False) -> LLMClient:
        """Получение конкретного клиента LLM"""
        if not self.context or not self.context.llm_client:
            raise ValueError("Context not initialized")

        logger.debug(f"_get_client: config_ai is None: {self.context.config_ai is None}")
        logger.debug(f"_get_client: config_ai type: {type(self.context.config_ai)}")
        logger.debug(f"_get_client: config_ai value: {self.context.config_ai}")

        if self.context.llm_client == ModelProvider.DEEPSEEK:
            logger.debug(f"Selected llm_client - DEEPSEEK")
            if ws:
                return DeepSeekWSClient(
                    chat_id=chat_id,
                    config_ai=self.context.config_ai
                )
            else:
                return DeepSeekHTTPClient(self.context.config_ai)
        elif self.context.llm_client == ModelProvider.YANDEX:
            logger.debug(f"Selected llm_client - YANDEX")
            return YandexClient(self.context.config_ai)
        elif self.context.llm_client == ModelProvider.GIGACHAT:
            logger.debug(f"Selected llm_client - GIGACHAT")
            if ws:
                client = GigachatWSClient(
                    chat_id=chat_id,
                    config_ai=self.context.config_ai
                )
                await client.initialize()
                return client
            else:
                return DeepSeekHTTPClient(self.context.config_ai)
        else:
            raise HTTPException(status_code=502, detail=f"Unsupported LLM client: {self.context.llm_client}")

    async def _domain_authorization(self, purpose_prompt: PurposePrompt):
        self.__context = _LLMGatewayContext()
        user_uid = purpose_prompt.user_uid

        user = User(user_uid)
        UserManagerDomain().add(user)

        UserAIConfigManagerDomain().add(user_uid)
        self.__context.config_ai = UserAIConfigManagerDomain().get(user_uid, purpose_prompt.purpose)
        logger.debug(f"config_ai is None: {self.__context.config_ai is None}")
        self.__context.llm_client = ModelProvider.DEFAULT
        logger.debug(f"llm_client is None: {self.__context.llm_client is None}")

class _LLMGatewayContext:
    def __init__(self):
        self.config_ai: Optional[AiManagerConfig] = None
        self.llm_client: Optional[ModelProvider] = None
