from fastapi import WebSocket
from typing import Dict, List, Deque, Optional
from collections import deque
import json
import asyncio
from datetime import datetime, timedelta
from core.logger import Logger

logger = Logger.get_logger(__name__)


class BufferedMessage:
    def __init__(self, data: dict, timestamp: Optional[datetime] = None):
        self.data = data
        self.timestamp = timestamp or datetime.now()

    def to_dict(self):
        return {
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }

class ConnectionManager:
    def __init__(self, max_buffer_size: int = 50, message_ttl: int = 3600):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.message_buffers: Dict[str, Deque[BufferedMessage]] = {}
        self.max_buffer_size = max_buffer_size
        self.message_ttl = message_ttl  # в секундах
        self._lock = asyncio.Lock()

    async def connect(self, chat_id: str, websocket: WebSocket):
        async with self._lock:
            logger.debug(f"[CONNECT] Начинаем подключение для chat_id={chat_id}")

            if chat_id not in self.active_connections:
                self.active_connections[chat_id] = []
                logger.debug(f"[CONNECT] Для chat_id={chat_id} создан новый список соединений")

            self.active_connections[chat_id].append(websocket)
            logger.debug(
                f"[CONNECT] Добавлено новое соединение. Всего соединений для {chat_id}: {len(self.active_connections[chat_id])}")

            # Логируем состояние буфера ДО флашинга
            buffer_size = len(self.message_buffers.get(chat_id, []))
            logger.debug(f"[CONNECT] Перед flush: буфер для {chat_id} содержит {buffer_size} сообщений")

            # Вызываем печать всех активных соединений
            await self.print_active_connections()

            # Пробуем сбросить буфер
            try:
                await self._flush_buffer(chat_id)
            except Exception as e:
                logger.error(f"[CONNECT] Ошибка во время flush буфера для {chat_id}: {e}")

            # Логируем состояние буфера ПОСЛЕ флашинга
            buffer_size_after = len(self.message_buffers.get(chat_id, []))
            logger.debug(f"[CONNECT] После flush: буфер для {chat_id} содержит {buffer_size_after} сообщений")

            logger.debug(f"[CONNECT] Завершено подключение для chat_id={chat_id}")

    async def disconnect(self, chat_id: str, websocket: WebSocket):
        async with self._lock:
            if chat_id in self.active_connections:
                self.active_connections[chat_id].remove(websocket)
                if not self.active_connections[chat_id]:
                    del self.active_connections[chat_id]
            await self.print_active_connections()

    async def send_message(self, chat_id: str, message: dict):
        try:
            logger.debug(f"Sending message to {chat_id}")
            success = await self._try_send_to_active_connections(chat_id, message)
            if not success:
                await self._add_to_buffer(chat_id, message)

        except Exception as e:
            logger.error(f"Error in send_message: {e}")

    async def _try_send_to_active_connections(self, chat_id: str, message: dict) -> bool:
        chat_id = str(chat_id)
        try:
            logger.debug(f"Trying to send message to {chat_id}, message: {str(message)}")
            """Пытается отправить сообщение активным подключениям, возвращает успех"""
            connections = self.active_connections.get(chat_id)
            if not connections:
                logger.debug(f"Нет активных подключений для chat_id: {chat_id}")
                return False

            success = False
            working_connections = []

            for connection in connections:
                try:
                    await connection.send_json(message)
                    success = True
                    working_connections.append(connection)
                    logger.debug(f"Сообщение успешно отправлено для: {connection}, {chat_id}")
                except Exception as e:
                    logger.debug(f"Connection failed for {chat_id}: {str(e)}")

            # Обновляем список активных соединений - оставляем только рабочие
            if len(working_connections) != len(connections):
                if working_connections:
                    self.active_connections[chat_id] = working_connections
                else:
                    del self.active_connections[chat_id]

            return success

        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {str(e)}")
            return False

    async def _add_to_buffer(self, chat_id: str, message: dict):
        """Добавляет сообщение в буфер"""
        if chat_id not in self.message_buffers:
            self.message_buffers[chat_id] = deque(maxlen=self.max_buffer_size)

        buffered_message = BufferedMessage(message)
        self.message_buffers[chat_id].append(buffered_message)
        logger.debug(f"Buffered message for {chat_id}. Buffer size: {len(self.message_buffers[chat_id])}")

    async def _flush_buffer(self, chat_id: str):
        try:
            """Отправляет все сообщения из буфера при подключении"""
            if chat_id not in self.message_buffers or not self.message_buffers[chat_id]:
                return

            logger.debug(f"Flushing buffer for {chat_id} ({len(self.message_buffers[chat_id])} messages)")

            # Очищаем просроченные сообщения
            await self._clean_old_messages(chat_id)

            # Отправляем все сообщения из буфера
            successful_messages = 0
            buffer = self.message_buffers[chat_id]

            while buffer:
                message = buffer[0]  # Смотрим первое сообщение, но не удаляем пока

                if await self._try_send_to_active_connections(chat_id, message.data):
                    # Успешно отправлено - удаляем из буфера
                    buffer.popleft()
                    successful_messages += 1
                else:
                    # Не удалось отправить - прерываем цикл
                    break

            logger.debug(f"Flushed {successful_messages} messages for {chat_id}")

            # Если буфер пуст, удаляем его
            if not buffer:
                del self.message_buffers[chat_id]
        except Exception as e:
            logger.error(f"Failed to flush buffer for {chat_id}: {e}")

    async def _clean_old_messages(self, chat_id: str):
        """Удаляет просроченные сообщения из буфера"""
        if chat_id not in self.message_buffers:
            return

        now = datetime.now()
        initial_count = len(self.message_buffers[chat_id])

        # Фильтруем сообщения, не превысившие TTL
        self.message_buffers[chat_id] = deque(
            (msg for msg in self.message_buffers[chat_id]
             if (now - msg.timestamp).total_seconds() <= self.message_ttl),
            maxlen=self.max_buffer_size
        )

        removed_count = initial_count - len(self.message_buffers[chat_id])
        if removed_count > 0:
            logger.debug(f"Removed {removed_count} expired messages from {chat_id} buffer")

    async def print_active_connections(self):
        try:
            if not self.active_connections:
                logger.debug("📭 Нет активных подключений")
            else:
                logger.debug("🔌 Активные подключения:")
                for key, websockets in self.active_connections.items():
                    logger.debug(f"  {key}: {len(websockets)} соединений")

            if self.message_buffers:
                logger.debug("📦 Буферизованные сообщения:")
                for chat_id, buffer in self.message_buffers.items():
                    logger.debug(f"  {chat_id}: {len(buffer)} сообщений")
                    logger.debug(f"buffer: {buffer}")
        except Exception as e:
            logger.error("Ебань")

    def get_buffer_stats(self, chat_id: str) -> dict:
        if chat_id in self.message_buffers:
            return {
                "message_count": len(self.message_buffers[chat_id]),
                "oldest_message": self.message_buffers[chat_id][0].timestamp if self.message_buffers[chat_id] else None,
                "newest_message": self.message_buffers[chat_id][-1].timestamp if self.message_buffers[chat_id] else None
            }
        return {"message_count": 0}

connection_manager = ConnectionManager()

def get_connection_manager():
    return connection_manager