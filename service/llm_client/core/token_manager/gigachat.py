from core.token_manager.token_manager import TokenManager
from core.logger import Logger
from core import config
import json
import os
import time
from typing import Tuple
from pathlib import Path
from uuid import uuid4
import requests
import certifi

logger = Logger.get_logger(__name__)


class GigachatTokenManager(TokenManager):
    def __init__(self):
        self._keys_iam = {}
        self._keys_jwt = {}
        self._access_token = ""
        self._token_expires_at = 9999999999

        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        relative_iam_key_path = config.get("GIGACHAT_AUTHORIZED_IAM_KEY_PATH")
        relative_jwt_key_path = config.get("GIGACHAT_AUTHORIZED_JWT_KEY_PATH")
        self.json_iam_path = self.BASE_DIR / Path(relative_iam_key_path)
        self.json_jwt_path = self.BASE_DIR / Path(relative_jwt_key_path)

        logger.debug(f"dep_key_path: {self.json_iam_path}")
        logger.debug(f"dep_key_path: {self.json_jwt_path}")

        if not os.path.exists(self.json_iam_path):
            raise RuntimeError(f"Keys file not found: {self.json_iam_path}")
        if not os.path.exists(self.json_jwt_path):
            raise RuntimeError(f"Keys file not found: {self.json_jwt_path}")

        self._load()

    def _load(self):
        with open(self.json_iam_path, "r", encoding="utf-8") as f:
            self._keys_iam = json.load(f)
        with open(self.json_jwt_path, "r", encoding="utf-8") as f:
            self._keys_jwt = json.load(f)

    def _save_iam(self):
        with open(self.json_iam_path, "w", encoding="utf-8") as f:
            json.dump(self._keys_iam, f, ensure_ascii=False, indent=4)

    def _save_jwt(self):
        with open(self.json_jwt_path, "w", encoding="utf-8") as f:
            json.dump(self._keys_jwt, f, ensure_ascii=False, indent=4)

    def get_token(self) -> Tuple[bool, str | None]:
        now = time.time() * 1000
        lifetime_corrector = 180 * 1000
        for token, token_info in list(self._keys_jwt.items()):
            expires_at = token_info.get("expires_at")
            if expires_at > (now + lifetime_corrector):
                logger.debug(f"Using valid Gigachat API token")
                return True, token

        logger.info("No valid tokens found, attempting to get new one...")
        try:
            new_token = self._update_jwt()
            if new_token:
                self._save_jwt()
                return True, new_token
        except Exception as e:
            logger.error(f"Error getting new token: {e}")

        logger.error("No available Gigachat API tokens")
        return False, None

    def _update_jwt(self) -> str | None:
        rq_uid = str(uuid4())
        iam_key = list(self._keys_iam.keys())[0]

        logger.info(f"Updating JWT token with RqUID: {rq_uid}")

        headers = {
            "Authorization": f"Basic {iam_key}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": rq_uid,
        }

        data = {
            "scope": config.get("GIGACHAT_SCOPE")
        }

        try:
            response = requests.post(
                config.get("GIGACHAT_OAUTH_URL"),
                headers=headers,
                data=data,
                timeout=30,
                verify=False
            )
            if response.status_code == 200:
                result = response.json()
                access_token = result.get('access_token')
                expires_at = result.get('expires_at')

                if not access_token or not expires_at:
                    logger.error("Missing access_token or expires_at in response")
                    return None

                self._keys_jwt = {
                    access_token: {
                        "RqUID": rq_uid,
                        "expires_at": expires_at,
                        "created_at": time.time() * 1000,
                    }
                }

                logger.info(f"Successfully updated JWT token, expires at: {expires_at}")
                return access_token
            else:
                logger.error(f"Error getting token: {response.status_code} - {response.text}")
                return None

        except requests.Timeout:
            logger.error("Timeout while updating JWT token")
            return None
        except requests.RequestException as e:
            logger.error(f"HTTP client error in update_jwt: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected exception in update_jwt: {e}")
            return None