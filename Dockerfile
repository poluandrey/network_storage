# Используем официальный образ Python
FROM python:3.11-slim

# Установка зависимостей для компиляции и установки Poetry
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей Poetry и блокировку версий
COPY src/pyproject.toml src/poetry.lock* /app

# Устанавливаем зависимости с помощью Poetry
RUN poetry config virtualenvs.create false && poetry install --no-root --only main

# Копируем исходный код проекта
COPY src /app

# Устанавливаем рабочую директорию на /app/src
WORKDIR /app

# Запускаем FastAPI с Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
