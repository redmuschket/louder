from uuid6 import UUID

class User:
    def __init__(self, user_id: UUID):
        self._uuid = user_id

    @property
    def uid(self) -> UUID:
        return self._uuid
