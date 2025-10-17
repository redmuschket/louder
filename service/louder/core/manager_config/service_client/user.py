from core.provider_config.service_client.user import UserServiceProviderConfig
from core.provider_config.provider_config import ProviderConfig
from core.manager_config.manager_config import ManagerConfig


class UserServiceManagerConfig(ManagerConfig):
    def __init__(self):
        self.__config = self._get_provider_config()
        self.__config.load()

    def _get_provider_config(self) -> ProviderConfig | None:
        return UserServiceProviderConfig()

    @property
    def api_uri(self):
        return getattr(self.__config, "api_uri", None)
