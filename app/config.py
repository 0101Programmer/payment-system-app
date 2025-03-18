from dotenv import load_dotenv
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape


# Загружаем переменные окружения из .env
load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SANIC_HOST = os.getenv("SANIC_HOST", "0.0.0.0")
    SANIC_PORT = int(os.getenv("SANIC_PORT", 8000))

# Настройка Jinja2
env = Environment(
    loader=FileSystemLoader("app/templates"),  # Указываем путь к шаблонам
    autoescape=select_autoescape(["html", "xml"])  # Включаем автоэкранирование
)