import os.path
from core.enum.purpose import AIPurpose
from typing import Dict, Any
from core import config


class PromptManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def get_prompt(self, purpose: AIPurpose, variables: Dict[str, Any]):
        prompt_path = PromptManager._resolve_prompt_path(purpose)
        if not os.path.exists(prompt_path):
            logger.error(f"Prompt path not found: {prompt_path}")
            return ""

        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                raw_prompt = f.read()
                prompt = Template(raw_prompt).safe_substitute(variables)
                return prompt
        except Exception as e:
            logger.error(f"Failed to read or format prompt: {e}")
            return ""

    @staticmethod
    def _resolve_prompt_path(purpose: AIPurpose) -> str:
        pass
