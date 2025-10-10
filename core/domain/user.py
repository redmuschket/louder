from uuid6 import UUID


class User:
    def __init__(self, user_id: UUID):
        self._uid: UUID = user_id
        self._dir: str = str(self._uid)

    @property
    def uid(self) -> UUID:
        return self._uid

    @property
    def dir(self):
        return self._dir
