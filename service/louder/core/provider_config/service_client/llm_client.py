from typing import Optional
from core.token_manager.service_client.llm_client import LLMServiceServiceTokenManager, TokenManager
from core.provider_config.provider_config import ProviderConfig
from core import config


class LLMClientProviderConfig(ProviderConfig):

    def load(self) -> None:
        self.api_url = config.get("LLMCLIENT_SERVICE_URL")

    def get_token_provider(self) -> Optional[TokenManager]:
        return LLMServiceServiceTokenManager()