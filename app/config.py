from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env
load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SANIC_HOST = os.getenv("SANIC_HOST", "0.0.0.0")
    SANIC_PORT = int(os.getenv("SANIC_PORT", 8000))