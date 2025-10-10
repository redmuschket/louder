from core.hash_provider import HashProviderService
from time import time

class HashedPatentName:
    def __init__(self, raw_name: str):
        if not isinstance(raw_name, str):
            raise ValueError("Expected raw patent name (str)")
        self._hashed = HashProviderService.get_hash(raw_name+str(time()))

    @property
    def value(self) -> str:
        return self._hashed

    def __str__(self):
        return self._hashed