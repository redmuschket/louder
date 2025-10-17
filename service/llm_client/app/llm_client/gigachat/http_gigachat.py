from core.logger import Logger
import aiohttp
from typing import Tuple, Optional
from app.llm_client.gigachat.llm_client_gigachat import GigachatClient
from core.manager_config.ai import AiManagerConfig

logger = Logger.get_logger(__name__)

class GigachatHTTPClient(GigachatClient):

    def __init__(self, config_ai: Optional[AiManagerConfig] = None):
        super().__init__(config_ai)

    async def ask(self, prompt: str) -> Tuple[bool, str]:
        logger.debug(f"___Star GigachatHTTPClient ask___")

        messages = [{"role": "user", "content": prompt}]

        headers = {
            "Authorization": f"Bearer {self.context.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        data = {
            "model": self.context.model,
            "messages": messages,
            "stream": False,
            "repetition_penalty": self.context.repetition_penalty,
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