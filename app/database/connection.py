from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base

from ..config import Config

# Асинхронный движок для подключения к базе данных
DATABASE_URL = Config.DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем асинхронную фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс для моделей
Base = declarative_base()

# Асинхронный контекстный менеджер для получения сессии
@asynccontextmanager
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session