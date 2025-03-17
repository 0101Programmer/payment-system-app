FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Добавляем /app в PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Команда для запуска приложения
CMD ["python", "-m", "app.main"]
