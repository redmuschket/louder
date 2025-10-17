import requests
from core.manager_config.service_client.user_service import UserServiceManagerConfig


class UserClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: UserServiceManagerConfig):
        self._config = config

    def user_exists(self, user_uid: str) -> bool:
        url = self._config.api_uri
        response = requests.get(f'{url}/users/exists/{user_uid}')
        if response.status_code == 200:
            data = response.json()
            return data.get('exists', False)
        else:
            logging.warning('Request error', response.status_code)
            return False
