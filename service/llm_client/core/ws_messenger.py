from core.connection_manager import get_connection_manager
from core.logger import Logger
from typing import Optional
import asyncio

logger = Logger.get_logger(__name__)


class WsMessenger:

    def __init__(self, chat_id):
        self.__chat_id = chat_id
        self.__websocket_manager = get_connection_manager()
        self.__result_future: Optional[asyncio.Future] = None

    @property
    def chat_id(self):
        return self.__chat_id

    @property
    def websocket_manager(self):
        return self.__websocket_manager

    @property
    def result_future(self):
        return self.__result_future

    @result_future.setter
    def result_future(self, value):
        self.__result_future = value

    async def handle_message(self, message: dict) -> str:
        """
        Обработка сообщений с автоматической отправкой через WebSocket

        Returns:
            str: статус обработки ("completed", "error", "continue")
        """
        try:
            status = message.get("status", "")

            if status == "processing":
                progress = int(message.get("progress", 0))
                msg_text = message.get("message", "")
                stage = message.get("stage", "")
                await self.send_update(msg_text, progress, stage)

            elif status == "completed":
                logger.debug(f"Completed message received: {str(message)[:150]}")
                result = message.get("result")
                if isinstance(result, dict) and self.result_future and not self.result_future.done():
                    self.result_future.set_result(result)
                    await self.send_success("Успех")
                    return "completed"

            elif status == "error":
                error_msg = message.get("message", "Parser error")
                if self.result_future and not self.result_future.done():
                    self.result_future.set_exception(Exception(error_msg))
                await self.send_error(error_msg)
                return "error"

        except Exception as e:
            logger.error(f"Error in handle_parser_message: {str(e)}")
            if self.result_future and not self.result_future.done():
                self.result_future.set_exception(e)
            await self.send_error(f"Ошибка обработки сообщения: {str(e)}")
            return "error"

        return "continue"

    async def send_error(self, error_message):
        await self.websocket_manager.send_message(
            self.chat_id,
            {
                "status": "error",
                "message": error_message,
                "stage": "failed"
            }
        )

    async def send_update(self, message, progress: int, stage: str):
        await self.websocket_manager.send_message(
            self.chat_id,
            {
                "status": "processing",
                "message": message,
                "progress": progress,
                "stage": stage
            })

    async def send_success(self, message):
        await self.websocket_manager.send_message(
            self.chat_id,
            {
                "status": "completed",
                "message": message,
                "stage": "completed"
            }
        )
