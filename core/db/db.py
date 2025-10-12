from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.pool import NullPool
import os
from core import config

DATABASE_URL = config.get("DATABASE_URL")


def get_config_bool(key: str, default: bool = False) -> bool:
    value = config.get(key)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'y', 't')
    return default


def get_config_int(key: str, default: int = 0) -> int:
    value = config.get(key)
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return default

db_echo = get_config_bool("DATABASE_ECHO")
db_pool_size = get_config_int("DATABASE_POOL_SIZE")
db_max_overflow = get_config_int("DATABASE_MAX_OVERFLOW")
db_pre_ping = get_config_bool("DATABASE_PRE_PING")
db_pool_recycle = get_config_int("DATABASE_POOL_RECYCLE")
db_pool_class = config.get("DATABASE_POOL_CLASS")
db_expire_on_commit = get_config_bool("DATABASE_EXPIRE_ON_COMMIT")
db_autocommit = get_config_bool("DATABASE_AUTOCOMMIT")
db_autoflush = get_config_bool("DATABASE_AUTOFLUSH")
db_future = get_config_bool("DATABASE_FUTURE")

# Basic settings for the engine
engine_kwargs = {
    "echo": db_echo,
    "pool_pre_ping": db_pre_ping,
    "pool_recycle": db_pool_recycle,
    "future": db_future,
}


# Pool Settings
if db_pool_class:
    engine_kwargs["poolclass"] = db_pool_class
else:
    # Adding pool size settings only for QueuePool
    engine_kwargs.update({
        "pool_size": db_pool_size,
        "max_overflow": db_max_overflow,
    })

engine = create_async_engine(DATABASE_URL, **engine_kwargs)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=db_expire_on_commit,
    autocommit=db_autocommit,
    autoflush=db_autoflush,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)