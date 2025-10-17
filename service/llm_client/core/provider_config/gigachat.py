from core import config
from typing import Optional
from core.token_manager.token_manager import TokenManager
from core.token_manager.gigachat import GigachatTokenManager
from core.provider_config.provider_config import ProviderConfig


class GigachatProviderConfig(ProviderConfig):

    def load(self) -> None:
         self.model = config.get("GIGACHAT_MODEL")
         self.temperature = float(config.get("GIGACHAT_TEMPERATURE"))
         self.api_uri = config.get("GIGACHAT_API_URL")
         self.repetition_penalty = config.get("GIGACHAT_REPETITION_PANALTY")

    def get_token_provider(self) -> Optional[TokenManager]:
        return GigachatTokenManager()