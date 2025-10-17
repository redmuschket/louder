from core.provider_config.auth_user import AuthUserProviderConfig, ProviderConfig
from core.manager_config.manager_config import ManagerConfig


class AuthUserManagerConfig(ManagerConfig):
    def __init__(self):
        self.__config = self._get_provider_config()
        self.__config.load()

    def _get_provider_config(self) -> ProviderConfig | None:
        return AuthUserProviderConfig()

    @property
    def jwt_algorithm(self):
        return getattr(self.__config, "jwt_algorithm", None)

    @property
    def token(self):
        return self.__config.get_token_provider().get_token()