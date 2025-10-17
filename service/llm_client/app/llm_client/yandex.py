import grpc
from google.protobuf import struct_pb2
from storage.generated.yandex import text_generation_pb2_grpc as pb_grpc
from storage.generated.yandex import text_generation_pb2 as pb
from app.llm_client.llm_client import LLMClient
from core.manager_config.ai import AiManagerConfig
from core.enum.api_protocol import ApiProtocol
import requests
from core.logger import Logger
from typing import Tuple

logger = Logger.get_logger(__name__)

class YandexClient(LLMClient):
    async def ask(self, prompt: str) -> Tuple[bool, str]:
        if self.config_ai.api_protocol == ApiProtocol.REST:
            return await YandexClient._ask_rest(self.config_ai, prompt)
        elif self.config_ai.api_protocol == ApiProtocol.GRPC:
            return await YandexClient._ask_grpc(self.config_ai, prompt)
    """
    @staticmethod
    async def generate_search_query_to_get_analogues(discription_patent):
        api_key = config.get('YANDEX_API_KEY')
        folders = config.get('YANDEX_FOLDERS')
        url = config.get('YANDEX_API_URL')
        iam_key = config.get('YANDEX_IAM_KEY')
        promt = ''

        data = {}
        data["modelUri"] = f"gpt://{folders}/yandexgpt"
        data["completionOptions"] = {"temperature": 0.3, "maxTokens": 1000}
        data["messages"] = [
            {"role": "system", "text": f"{promt}"},
            {"role": "user", "text": f"{discription_patent}"},
        ]

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url,
                    headers={
                        "Accept": "application/json",
                        "Authorization": f"Bearer {iam_key}"
                    },
                    json=data
            ) as resp:
                response = await resp.json()

        print(f'{response=}')
        return response
    """
    @staticmethod
    async def _ask_rest(config_ai: AiManagerConfig, prompt: str) -> Tuple[bool, str]:
        success, iam_token_or_error = config_ai.token
        if not success:
            logger.error(f"Failed to get IAM Yandex token: {iam_token_or_error}")
            return False, ""

        data = {
            "modelUri": f"gpt://{config_ai.folders}/{config_ai.model}",
            "completionOptions": {
                "temperature": config_ai.temperature,
                "maxTokens": config_ai.max_token
            },
            "messages": [{"role": "user", "text": prompt}]
        }

        try:
            response = requests.post(
                config_ai.api_uri,
                headers={
                    "Authorization": f"Bearer {iam_token_or_error}",
                    "Content-Type": "application/json"
                },
                json=data
            )
            response.raise_for_status()

            result = response.json()
            assistant_reply = result['choices'][0]['message']['content']
            logger.debug("assistant reply: %s", assistant_reply)
            return True, assistant_reply

        except Exception as e:
            logger.error(f"REST request failed: {str(e)}")
            return False, ""

    @staticmethod
    async def _ask_grpc(config_ai: AiManagerConfig, prompt: str) -> Tuple[bool, str]:
        success, iam_token_or_error = config_ai.token
        if not success:
            logger.error(f"Failed to get IAM Yandex token: {iam_token_or_error}")
            return False, ""

        try:
            channel_credentials = grpc.ssl_channel_credentials()
            call_credentials = grpc.access_token_call_credentials(iam_token_or_error)
            credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)

            with grpc.secure_channel(
                    config_ai.api_uri,
                    credentials=credentials
            ) as channel:
                stub = pb_grpc.TextGenerationServiceStub(channel)

                # Создаем запрос с правильными типами
                request = pb.CompletionRequest(
                    model_uri=f"gpt://{config_ai.folders}/{config_ai.model}",
                    messages=[pb.Message(role="user", text=prompt)],
                    completion_options=pb.CompletionOptions(
                        stream=False,
                        temperature=struct_pb2.DoubleValue(value=config_ai.temperature),
                        max_tokens=struct_pb2.Int64Value(value=config_ai.max_token)
                    )
                )

                # Получаем ответ
                response = stub.Completion(request)
                full_response = []

                for resp in response:
                    for alternative in resp.alternatives:
                        full_response.append(alternative.message.text)

                if full_response:
                    assistant_reply = " ".join(full_response)
                    logger.debug("assistant reply: %s", assistant_reply)
                    return True, assistant_reply

        except grpc.RpcError as e:
            logger.error(f"gRPC request failed: {e.code()}: {e.details()}")
            return False, ""
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False, ""