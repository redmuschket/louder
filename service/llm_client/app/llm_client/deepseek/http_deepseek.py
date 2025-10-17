from core.logger import Logger
import aiohttp
from typing import Tuple, Optional
from app.llm_client.deepseek.llm_client_deepseek import DeepSeekClient
from core.manager_config.ai import AiManagerConfig

logger = Logger.get_logger(__name__)

class DeepSeekHTTPClient(DeepSeekClient):

    def __init__(self, config_ai: Optional[AiManagerConfig] = None):
        super().__init__(config_ai)
    
    async def ask(self, prompt: str) -> Tuple[bool, str]:
        logger.debug(f"___Star DeepSeekHTTPClient ask___")

        messages = [{"role": "user", "content": prompt}]

        headers = {
            "Authorization": f"Bearer {self.context.token}",
            "HTTP-Referer": self.context.referer,
            "X-Title": self.context.site_name,
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek/deepseek-chat",
            "messages": messages,
            "temperature": self.context.temperature,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        self.context.api_uri,
                        headers=headers,
                        json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        assistant_reply = result['choices'][0]['message']['content']
                        logger.debug("assistant reply: %s", assistant_reply)
                        return True, assistant_reply
                    else:
                        error_text = await response.text()
                        logger.error(f"Response ai: {response.status}, {error_text}")
                        return False, ""
        except Exception as e:
            logger.error(f"Connection to AI failed: {e}")
            return False, ""