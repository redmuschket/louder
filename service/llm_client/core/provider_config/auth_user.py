from typing import Optional
from core.token_manager.token_manager_jwt_user import JWTUserTokenManager, TokenManager
from core.provider_config.provider_config import ProviderConfig
from core import config


class AuthUserProviderConfig(ProviderConfig):

    def load(self) -> None:
        self.jwt_algorithm = config.get("JWT_ALGORITHM")

    def get_token_provider(self) -> Optional[TokenManager]:
        return JWTUserTokenManager()