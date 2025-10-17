from core.domain.user import User
from core.logger import Logger

from uuid6 import uuid7, UUID
from pathlib import Path
from typing import Tuple, Dict, Optional
from sqlalchemy.orm import Session


logger = Logger.get_logger(__name__)


class UserService:
    def __init__(self, db: Session):
        self._db = db

    @staticmethod
    def create_base_user_domain(user_uid: UUID) -> User:
        """
        Creates a domain object User with validation

        Args:
           user_uid: User uid

        Returns:
           User: The created domain object

        Raises:
           ValueError: If the parameters are invalid
        """
        try:
            return User(uid=user_uid)
        except Exception as e:
            logger.error(f"Error creating user '{user_uid}': {e}")
            raise
