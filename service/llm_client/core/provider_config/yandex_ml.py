from core import config
from core.logger import Logger
from typing import Optional
from core.token_manager.token_manager import TokenManager
from core.provider_config.provider_config import ProviderConfig
from core.enum.api_protocol import ApiProtocol
from core.token_manager.yandex_cloud import YandexTokenManager

logger = Logger.get_logger(__name__)

class YandexMLProviderConfig(ProviderConfig):

    def __init__(self, api_protocol: ApiProtocol):
        self.api_protocol = api_protocol

    def load(self) -> None:
        if self.api_protocol == ApiProtocol.REST:
            self.model = config.get("YANDEX_ML_PARSER_REST_MODEL")
            self.api_uri = config.get("YANDEX_ML_PARSER_REST_API_URI")
            self.folders = config.get("YANDEX_ML_PARSER_REST_FOLDERS")
        elif self.api_protocol == ApiProtocol.GRPC:
            self.model = config.get("YANDEX_ML_PARSER_GRPC_MODEL")
            self.api_uri = config.get("YANDEX_ML_PARSER_GRPC_API_URI")
            self.folders = config.get("YANDEX_ML_PARSER_GRPC_FOLDERS")
        else:
            logger.error(f"YandexMLParser does not implement the api protocol - {self.api_protocol}."
                         f" The proxy storage path could not be determined: model, api_uri, folders")
            self.model = None
            self.api_uri = None
            self.folders = None

        self.prompt_path  = config.get('PATENT_PROMPTS_PARSER_YANDEX_PATH')
        self.service_account_id = config.get("YANDEX_ML_ATTRIBUTE_MATCHER_SERVICE_ACCOUNT_ID")
        self.max_token = int(config.get("YANDEX_ML_PARSER_MAX_TOKEN"))
        self.iam_key_path = config.get("YANDEX_ML_PARSER_IAM_KEY_PATH")
        self.jwt_key_path = config.get("YANDEX_ML_PARSER_JWT_KEY_PATH")
        self.authorized_key_path = config.get("YANDEX_ML_PARSER_AUTHORIZED_KEY_PATH")

    def get_token_provider(self) -> Optional[TokenManager]:
        return YandexTokenManager(
                self.authorized_key_path,
                self.jwt_key_path,
                self.iam_key_path,
                self.service_account_id
                )