from core.logger import Logger
import aiohttp
from typing import Tuple, Optional
from app.llm_client.gigachat.llm_client_gigachat import GigachatClient
from core.manager_config.ai import AiManagerConfig
from core.ws_messenger import WsMessenger

logger = Logger.get_logger(__name__)

class GigachatWSClient(GigachatClient):

    def __init__(self, chat_id, config_ai: Optional[AiManagerConfig] = None):
        logger.debug(f"DeepSeekWSClient init: chat_id={chat_id}, config_ai={config_ai}")
        logger.debug(f"DeepSeekWSClient init: config_ai is None: {config_ai is None}")
        logger.debug(f"DeepSeekWSClient init: config_ai type: {type(config_ai)}")

        super().__init__(config_ai)
        self._ws_messenger = WsMessenger(chat_id)

    async def ask(self, prompt: str):
        logger.debug(f"___Star GigachatHTTPClient ask___")

        logger.debug(f"context.api_uri:{self.context.api_uri}")
        logger.debug(f"context.model:{self.context.model}")
        logger.debug(f"context.model:{self.context.temperature}")
        logger.debug(f"context.token:{self.context.token}")
        await self._ws_messenger.send_update(
            "Собираем messages",
            10,
            "collecting_message"
        )

        messages = [{"role": "user", "content": prompt}]

        await self._ws_messenger.send_update(
            "Собираем headers",
            30,
            "collecting_headers"
        )

        headers = {
            "Authorization": f"Bearer {self.context.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        await self._ws_messenger.send_update(
            "Собираем data",
            40,
            "collecting_data"
        )

        data = {
            "model": self.context.model,
            "messages": messages,
            "stream": False,
            "repetition_penalty": self.context.repetition_penalty,
            "temperature": self.context.temperature,
        }

        await self._ws_messenger.send_update(
            "Отправляем запрос",
            50,
            "calculating_start_attributes"
        )

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
                        await self._ws_messenger.send_success(assistant_reply)
                    else:
                        error_text = await response.text()
                        logger.error(f"Response ai: {response.status}, {error_text}")
                        await self._ws_messenger.send_error(f"Response ai: {response.status}, {error_text}")

        except Exception as e:
            logger.error(f"Connection to AI failed: {e}")
            await self._ws_messenger.send_error(f"Connection to AI failed: {e}")