from dotenv import load_dotenv
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape


# Загружаем переменные окружения из .env
load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL")
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    SANIC_HOST = os.getenv("SANIC_HOST", "0.0.0.0")
    SANIC_PORT = int(os.getenv("SANIC_PORT", 8000))
    ADMIN_KEY=os.getenv("ADMIN_KEY")
    PAYMENT_SECRET_KEY=os.getenv("PAYMENT_SECRET_KEY")

    # Определяем, используется ли Docker
    USE_DOCKER = int(os.getenv("USE_DOCKER"))

    # Переменные для использования без запуска Docker
    NO_DOCKER_DATABASE_URL = os.getenv("NO_DOCKER_DATABASE_URL")
    NO_DOCKER_REDIS_HOST = os.getenv("NO_DOCKER_REDIS_HOST")
    NO_DOCKER_REDIS_PORT = os.getenv("NO_DOCKER_REDIS_PORT")

# Настройка Jinja2
env = Environment(
    loader=FileSystemLoader("app/templates"),  # Указываем путь к шаблонам
    autoescape=select_autoescape(["html", "xml"])  # Включаем автоэкранирование
)