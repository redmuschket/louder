from abc import ABC, abstractmethod
from typing import Any


class ManagerDomain(ABC):

    @abstractmethod
    def add(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def get(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def remove(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def edit(self, *args: Any, **kwargs: Any) -> Any:
        pass
