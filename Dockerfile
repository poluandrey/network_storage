FROM python:3.12.2-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME /usr/local

RUN apt-get update && \
    apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3

COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-root --no-dev

COPY . .
CMD ["poetry", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
