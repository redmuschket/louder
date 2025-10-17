from core.provider_config.gigachat import GigachatProviderConfig
from core.provider_config.provider_config import ProviderConfig
from typing import Optional
from core.manager_config.manager_config import ManagerConfig
from core.enum.purpose_provider import AIProviderPurpose
from core.enum.model_provider import ModelProvider
from core.enum.api_protocol import ApiProtocol
from core.provider_config.deepseek import DeepSeekProviderConfig
from core.provider_config.yandex_ml import YandexMLProviderConfig
from core.logger import Logger

logger = Logger.get_logger(__name__)

class AiManagerConfig(ManagerConfig):
    def __init__(
            self,
            model_provider: ModelProvider = ModelProvider.DEFAULT,
            api_protocol: ApiProtocol = ApiProtocol.DEFAULT,
            provider_purpose: AIProviderPurpose = None):
        self._model_provider = model_provider
        self._api_protocol = api_protocol
        self._provider_purpose = provider_purpose
        self.__config = self._get_provider_config()
        self.__config.load()

    def _get_provider_config(self) -> ProviderConfig | None:
        if self._model_provider == ModelProvider.DEEPSEEK:
            return DeepSeekProviderConfig()
        elif self._model_provider == ModelProvider.GIGACHAT:
            return GigachatProviderConfig()
        elif self._model_provider == ModelProvider.YANDEX:
            if self._provider_purpose == AIProviderPurpose.ATTRIBUTE_GENERATION:
                return YandexMLProviderConfig(self._api_protocol)
            elif self._provider_purpose == AIProviderPurpose.ATTRIBUTE_MATCHER:
                return YandexMLProviderConfig(self._api_protocol)
            else:
                logger.error(f"Unsupported purpose of the Yandex provider: {self._provider_purpose}.")
                return None
        else:
            logger.error(f"Unsupported model provider: {self._model_provider}")
            return None

    @property
    def api_protocol(self):
        return self._api_protocol

    @property
    def model(self):
        return getattr(self.__config, "model", None)

    @property
    def temperature(self):
        return getattr(self.__config, "temperature", None)

    @property
    def service_account_id(self):
        return getattr(self.__config, "service_account_id", None)

    @property
    def api_uri(self):
        return getattr(self.__config, "api_uri", None)

    @property
    def folders(self):
        return getattr(self.__config, "folders", None)

    @property
    def referer(self):
        return getattr(self.__config, "referer", None)

    @property
    def site_name(self):
        return getattr(self.__config, "site_name", None)

    @property
    def token(self):
        return self.__config.get_token_provider().get_token()

    @property
    def max_token(self):
        return getattr(self.__config, "max_token", None)

    @property
    def prompt_path(self):
        return getattr(self.__config, "prompt_path", None)

    @property
    def repetition_penalty(self):
        return getattr(self.__config, "repetition_penalty", None)