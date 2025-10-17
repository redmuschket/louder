from core.token_manager.token_manager import TokenManager
from core.logger import Logger
from core import config
import json
import os
import time
from typing import Tuple, Optional
from pathlib import Path

logger = Logger.get_logger(__name__)

class DeepSeekTokenManager(TokenManager):
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        relative_key_path = config.get("DEEPSEEK_AUTHORIZED_KEY_PATH")
        self.json_path = self.BASE_DIR / Path(relative_key_path)
        logger.debug(f"DeepSeek_key_path: {self.json_path}")
        if not os.path.exists(self.json_path):
            raise RuntimeError(f"Keys file not found: {self.json_path}")
        self._load()

    def _load(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            self._keys = json.load(f)

    def _save(self):
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self._keys, f, ensure_ascii=False, indent=4)

    def get_token(self) -> Tuple[bool, Optional[str]]:
        now = time.time()
        for key, key_info in self._keys.items():
            if key_info["reset_time"] > 0 and now >= key_info["reset_time"]:
                logger.info(f"Key {key[9:13]}... unlocked automatically")
                key_info["reset_time"] = 0
                key_info["used"] = 0
                self._save()

            if key_info["reset_time"] == 0 and key_info["used"] < key_info["limit"]:
                logger.debug(f"Using DeepSeek API key: {key[9:13]}...")
                self.mark_usage(key)
                return True, key

        logger.error("No available DeepSeek API keys")
        return False, None

    def mark_usage(self, key: str):
        key_info = self._keys.get(key)
        if key_info:
            key_info["used"] += 1
            if key_info["used"] != key_info["limit"]:
                self._save()
            else:
                self.mark_rate_limit(key)

    def mark_rate_limit(self, key: str):
        key_info = self._keys.get(key)
        if key_info:
            key_info["reset_time"] = time.time() + 86400
            self._save()
            logger.warning(f"Key {key[:4]}... blocked")