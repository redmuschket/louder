import json
import os
import time
from jose import jwt
from core.logger import Logger
from datetime import datetime
from core.token_manager.token_manager import TokenManager
import yandexcloud
from yandex.cloud.iam.v1.iam_token_service_pb2 import (CreateIamTokenRequest)
from yandex.cloud.iam.v1.iam_token_service_pb2_grpc import IamTokenServiceStub
from typing import Tuple

logger = Logger.get_logger(__name__)

class YandexTokenManager(TokenManager):
    def __init__(
            self,
            authorized_key_path,
            jwt_key_path,
            iam_key_path,
            service_account_id):
        self._authorized_key_path = authorized_key_path
        self._jwt_key_path = jwt_key_path
        self._iam_key_path = iam_key_path
        self._service_account_id = service_account_id

    def get_token(self) -> Tuple[bool, str]:
        if self._is_iam_token_valid():
            return True, self._read_iam_token() 

        if self._is_jwt_token_valid():
            if not self._create_iam():
                return False, "error receiving iam"
            return True, self._read_iam_token() 

        if self._is_authorized_key_valid():
            if not self._create_jwt():
                return False, "error receiving jwt"
            if not self._create_iam():
                return False, "error receiving iam"
            return True, self._read_iam_token() 
        else:
            return False, "authorized_keys is not valid"


    def _read_authorized_key(self) -> {str, str, str}:
        logger.warning("Reading yandex authorized key")
        with open(self._authorized_key_path, 'r') as f:
            obj = f.read()
            obj = json.loads(obj)
            private_key = obj['private_key']
            key_id = obj['id']
            service_account_id = obj['service_account_id']

        sa_key = {
            "id": key_id,
            "service_account_id": service_account_id,
            "private_key": private_key
        }
        return sa_key

    def _read_jwt_token(self) -> str:
        with open(self._jwt_key_path, "r") as f:
            jwt_data = json.load(f)
        jwt_token = jwt_data["jwt"]
        return jwt_token

    def _read_iam_token(self) -> str:
        with open(self._iam_key_path, "r") as f:
            return json.load(f)["iamToken"]

    def _create_jwt(self) -> bool:
        try:
            sa_key = self._read_authorized_key()
            now = int(time.time())
            payload = {
                'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
                'iss': self._service_account_id,
                'iat': now,
                'exp': now + 3600
            }

            encoded_token = jwt.encode(
                payload,
                sa_key["private_key"],
                algorithm='PS256',
                headers={'kid': sa_key["id"]}
            )

            with open(self._jwt_key_path, "w") as f:
                json.dump({"jwt": encoded_token}, f)
            return True
        except Exception as e:
            logger.error(f"JWT creation error: {e}")
            return False

    def _create_iam(self) -> bool:
        try:
            jwt = self._read_jwt_token()
            sa_key = self._read_authorized_key()
            sdk = yandexcloud.SDK(service_account_key=sa_key)
            iam_service = sdk.client(IamTokenServiceStub)
            iam_token = iam_service.Create(
                CreateIamTokenRequest(jwt=jwt)
            )

            with open(self._iam_key_path, "w") as f:
                json.dump({
                    "iamToken": iam_token.iam_token,
                    "expiresAt": iam_token.expires_at
                }, f)
            return True
        except Exception as e:
            logger.error(f"IAM creation error: {e}")
            return False

    def _is_iam_token_valid(self) -> bool:
        if not os.path.exists(self._iam_key_path):
            return False
        try:
            with open(self._iam_key_path, "r") as f:
                data = json.load(f)
            expires_at = data.get("expiresAt")
            if not expires_at:
                return False
            return datetime.fromisoformat(expires_at.replace("Z", "+00:00")) > datetime.utcnow()
        except Exception:
            return False

    def _is_jwt_token_valid(self) -> bool:
        if not os.path.exists(self._jwt_key_path):
            return False
        try:
            with open(self._jwt_key_path, "r") as f:
                jwt_data = json.load(f)
            exp = jwt.decode(jwt_data["jwt"], options={"verify_signature": False})["exp"]
            return exp > time.time()
        except Exception:
            return False

    def _is_authorized_key_valid(self) -> bool:
        return os.path.exists(self._authorized_key_path)