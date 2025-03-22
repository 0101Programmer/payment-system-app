import logging
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from ..config import Config

# Настройка логирования SQLAlchemy
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)  # Уровень INFO
logging.getLogger('sqlalchemy.pool').setLevel(logging.INFO)    # Логирование пула соединений

# Асинхронный движок для подключения к базе данных
DATABASE_URL = Config.DATABASE_URL if int(Config.USE_DOCKER) else Config.NO_DOCKER_DATABASE_URL
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

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
        try:
            yield session
            await session.commit()  # Фиксируем транзакцию при успешном завершении
        except Exception as e:
            await session.rollback()  # Откатываем транзакцию в случае ошибки
            logging.error(f"Database error: {str(e)}")
            raise