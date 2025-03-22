import os

import redis
from dotenv import load_dotenv
import subprocess


# Шаг 1: Установка зависимостей
def install_dependencies():
    print("Установка зависимостей...")
    if not os.path.exists("requirements.txt"):
        raise FileNotFoundError("Файл requirements.txt отсутствует!")

    subprocess.run(["pip", "install", "--no-cache-dir", "-r", "requirements.txt"], check=True)


# Шаг 2: Загрузка переменных окружения
def load_environment():
    print("Загрузка переменных окружения...")
    if not os.path.exists(".env"):
        raise FileNotFoundError("Файл .env отсутствует!")

    load_dotenv()  # Загрузка переменных из .env


# Шаг 3: Проверка переменных окружения
def setup_environment():
    print("Проверка переменных окружения...")
    required_env_vars = [
        "NO_DOCKER_DATABASE_URL",
        "NO_DOCKER_REDIS_PORT",
        "NO_DOCKER_REDIS_HOST"
    ]

    for var in required_env_vars:
        if var not in os.environ:
            raise ValueError(f"Необходимо указать переменную окружения: {var}")


# Шаг 4: Проверка Redis
def check_redis():
    print("Проверка Redis...")
    try:
        # Подключение к Redis
        redis_client = redis.Redis(host=os.getenv("NO_DOCKER_REDIS_HOST"), port=os.getenv("NO_DOCKER_REDIS_PORT"), decode_responses=True)
        redis_client.ping()
        print("Redis доступен.")
    except redis.exceptions.ConnectionError as e:
        print(f"Ошибка подключения к Redis: {e}")

# Шаг 5: Запуск приложения
def run_application():
    print("Запуск приложения...")
    subprocess.run(["python", "-m", "app.main"], check=True)


if __name__ == "__main__":
    try:
        install_dependencies()
        load_environment()
        setup_environment()
        check_redis()
        run_application()
    except Exception as e:
        print(f"Произошла ошибка: {e}")