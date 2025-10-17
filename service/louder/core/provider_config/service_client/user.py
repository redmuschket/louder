from typing import Optional
from core.token_manager.service_client.user import UserServiceTokenManager, TokenManager
from core.provider_config.provider_config import ProviderConfig
from core import config


class UserServiceProviderConfig(ProviderConfig):

    def load(self) -> None:
        self.url = config.get("USER_SERVICE_URL")

    def get_token_provider(self) -> Optional[TokenManager]:
        return UserServiceTokenManager()
