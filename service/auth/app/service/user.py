from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from fastapi import HTTPException

from core.db.models.user import User
from core.logger import Logger
from core.dto import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = Logger.get_logger(__name__)


class AccessError:
    @staticmethod
    def get_error_in_user_data():
        raise HTTPException(status_code=401, detail="The user was not found")


class UserService:

    @staticmethod
    async def create_user(dto: UserCreate, db: AsyncSession):
        result = await db.execute(select(User).where(User.login == dto.login))
        candidate = result.scalar_one_or_none()

        if candidate is not None:
            raise HTTPException(status_code=401, detail="User already exists")

        hashed_password = pwd_context.hash(dto.password)
        new_user = User(login=dto.login, hashed_password=hashed_password)

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user

    @staticmethod
    async def login(dto: UserCreate, db: AsyncSession):
        result = await db.execute(select(User).where(User.login == dto.login))
        user = result.scalar_one_or_none()

        if user is None:
            AccessError.get_error_in_user_data()

        if not pwd_context.verify(dto.password, user.hashed_password):
            AccessError.get_error_in_user_data()

        return user
