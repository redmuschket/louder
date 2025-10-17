from abc import ABC, abstractmethod
from typing import Tuple


class TokenManager(ABC):
    @abstractmethod
    def get_token(self) -> Tuple[bool, str]:
        pass
