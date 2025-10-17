from typing import Dict
from core.domain.user import User
from core.enum.purpose_provider import AIProviderPurpose
from core.manager_domain import ManagerDomain
from core.manager_domain.user import UserManagerDomain
from core.manager_config.ai import AiManagerConfig
from core.logger import Logger
from uuid6 import UUID

logger = Logger.get_logger(__name__)

class UserAIConfigManagerDomain(ManagerDomain):
    __users_config: Dict[User, Dict[AIProviderPurpose, AiManagerConfig]] = {}
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def add(self, user_uid):
        user = UserManagerDomain().get(user_uid)
        if user is None:
            logger.error(f"User {user_uid} not found in UserManagerDomain")
        if user not in self.__users_config:
            self.__users_config[user] = {}

        self.__users_config[user][AIProviderPurpose.ATTRIBUTE_GENERATION] = AiManagerConfig()
        self.__users_config[user][AIProviderPurpose.ATTRIBUTE_MATCHER] = AiManagerConfig()
        self.__users_config[user][AIProviderPurpose.CHECKING_ATTRIBUTE] = AiManagerConfig()

    def get(self, user_uid: UUID, purpose: AIProviderPurpose) -> AiManagerConfig | None:
        user = UserManagerDomain().get(user_uid)
        if user is None:
            logger.error(f"User {user_uid} not found in UserManagerDomain")
        return self.__users_config.get(user).get(purpose)

    def remove(self, user_uid, purpose: AIProviderPurpose):
        user = UserManagerDomain().get(user_uid)
        dick_purpose = self.__users_config.get(user)
        dick_purpose.pop(purpose)

    def edit(self, user_uid, purpose: AIProviderPurpose, ai_config: AiManagerConfig):
        user = UserManagerDomain().get(user_uid)
        self.__users_config[user][purpose] = ai_config
