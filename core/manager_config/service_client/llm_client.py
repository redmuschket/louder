from core.provider_config.service_client.llm_client import LLMClientProviderConfig, ProviderConfig

class LLMClientServiceManagerConfig:
    def __init__(self):
        self.__config = self._get_provider_config()
        self.__config.load()

    def _get_provider_config(self) -> ProviderConfig | None:
        return LLMClientProviderConfig()

    @property
    def api_url(self):
        return getattr(self.__config, 'api_url')

    @property
    def token(self):
        return self.__config.get_token_provider().get_token()