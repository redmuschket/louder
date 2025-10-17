from fastapi import WebSocket, WebSocketDisconnect
from core.connection_manager import get_connection_manager
from fastapi import APIRouter
from core.logger import Logger

router = APIRouter(prefix="/api/v1/ws/llm", tags=["LLM_Client"])
logger = Logger.get_logger(__name__)

@router.websocket("/{user_uid}")
async def websocket(
        websocket: WebSocket,
        user_uid: str
):
    try:
        await websocket.accept()
        connection_manager = get_connection_manager()

        try:
            chat_id = str(user_uid)
            await connection_manager.connect(chat_id, websocket)
            logger.info(f"User {user_uid} connected successfully")

            while True:
                data = await websocket.receive_text()
                logger.debug(f"Received message from user {user_uid}: {data}")

        except WebSocketDisconnect:
            logger.info(f"User {user_uid} disconnected")
        except Exception as e:
            logger.error(f"WebSocket error for user {user_uid}: {str(e)}")
        finally:
            await connection_manager.disconnect(user_uid, websocket)
            logger.info(f"User {user_uid} cleanup completed")

    except Exception as e:
        logger.error(f"{user_uid}: {str(e)}")

