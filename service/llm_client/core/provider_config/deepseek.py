from core import config
from typing import Optional
from core.token_manager.token_manager import TokenManager
from core.token_manager.deepseek import DeepSeekTokenManager
from core.provider_config.provider_config import ProviderConfig


class DeepSeekProviderConfig(ProviderConfig):

    def load(self) -> None:
         self.model = config.get("DEEPSEEK_MODEL")
         self.temperature = float(config.get("DEEPSEEK_TEMPERATURE"))
         self.referer = config.get("DEEPSEEK_REFERER")
         self.site_name = config.get("DEEPSEEK_SITE_NAME")
         self.prompt_path = config.get("PATENT_PROMPTS_PARSER_DEEPSEEK_PATH")
         self.api_uri = config.get("DEEPSEEK_API_URL")

    def get_token_provider(self) -> Optional[TokenManager]:
        return DeepSeekTokenManager()