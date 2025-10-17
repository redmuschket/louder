from abc import ABC, abstractmethod
from typing import Optional
from core.provider_config.provider_config import ProviderConfig


class ManagerConfig(ABC):

    @abstractmethod
    def _get_provider_config(self) -> Optional[ProviderConfig]:
        pass
