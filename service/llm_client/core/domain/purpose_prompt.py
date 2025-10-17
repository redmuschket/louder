from uuid6 import UUID
from core.logger import Logger
from core.enum.purpose_provider import AIProviderPurpose

logger = Logger.get_logger(__name__)

class PurposePrompt:
    def __init__(self, prompt, user_uid: UUID, purpose: AIProviderPurpose):
        if not isinstance(user_uid, UUID):
            raise TypeError("user_uid must be UUID")

        if not isinstance(purpose, AIProviderPurpose):
            raise TypeError("purpose must be AIProviderPurpose")

        if not prompt:
            raise TypeError("prompt must be AIProviderPurpose")

        self._uuid = user_uid
        self._prompt = prompt
        self._purpose = purpose

    @property
    def user_uid(self):
        return self._uuid

    @property
    def prompt(self):
        return self._prompt

    @property
    def purpose(self):
        return self._purpose
