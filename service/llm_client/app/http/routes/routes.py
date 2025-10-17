from app import *
from app.http.request_models.prompt_ask_request import AskRequest
from app.http.response_models.ask_response import AskResponse
from app.service.llm_gateway import LLMGateway
from core.logger import Logger
from fastapi import Depends, APIRouter
from uuid6 import UUID
from fastapi import HTTPException
from core.domain.purpose_prompt import PurposePrompt
from app.service.token_introspection import TokenIntrospectionService
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/v1/client", tags=["LLM_Client"])
logger = Logger.get_logger(__name__)

# ask. Basic call. Sending a prompt and receiving text.
@router.post('/ask', response_model=AskResponse)
async def ask(
    prompt_request: AskRequest,
    key: bool = Depends(TokenIntrospectionService.has_service_key)):
    try:
        user_uid = UUID(prompt_request.user_uuid)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Invalid user uid")
    try:
        purpose_prompt = PurposePrompt(
            user_uid=user_uid,
            prompt=prompt_request.prompt,
            purpose=prompt_request.purpose
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Invalid get request")
    success, request = await LLMGateway().ask(purpose_prompt)
    if success:
        return AskResponse(response=request)
    raise HTTPException(status_code=502, detail="Invalid get description")


@router.post('/ws_ask/{chat_id}', response_model=AskResponse)
async def ws_ask(
    chat_id: str,
    prompt_request: AskRequest,
    background_tasks: BackgroundTasks,
    key: bool = Depends(TokenIntrospectionService.has_service_key)):
    try:
        user_uid = UUID(prompt_request.user_uuid)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Invalid user uid")

    try:
        logger.debug(f"ws_ask: {prompt_request.prompt[:25]}, {prompt_request.purpose}")
        purpose_prompt = PurposePrompt(
            user_uid=user_uid,
            prompt=prompt_request.prompt,
            purpose=prompt_request.purpose
        )

        llm_gateway = LLMGateway()

        background_tasks.add_task(
            llm_gateway.ws_ask,
            purpose_prompt=purpose_prompt,
            chat_id=chat_id,
        )

        return JSONResponse(
            content={
                "message": "Процесс вычисления атрибутов запущен",
                "user_uid": str(user_uid)
            },
            status_code=202
        )

    except Exception as e:
        logger.error(f"Error: {e}")
        return JSONResponse(
            content={"error": "Internal server error"},
            status_code=500
        )

# batch_ask Processing multiple requests at once
@router.post('/batch_ask')
async def batch_ask(
        user_prompt_request: AskRequest,
        key: bool = Depends(TokenIntrospectionService.has_service_key)):
    pass

# chat. Contextual chat.
# stream. Streaming generation
# completion A method for fine-tuning
# embedding	Text vectorization
# token_count Counting tokens
# moderation Some LLM APIs can do moderation
# healthcheck Checking the availability of the service
# batch_ask Processing multiple requests at once
# cancel Long generation interrupt (if available)
