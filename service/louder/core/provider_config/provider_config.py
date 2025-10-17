from abc import ABC, abstractmethod
from typing import Optional
from core.token_manager.token_manager import TokenManager


class ProviderConfig(ABC):

    @abstractmethod
    def load(self) -> None:
        pass

    def get_token_provider(self) -> Optional[TokenManager]:
        return None
