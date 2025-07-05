FROM python:3.10-slim

WORKDIR /app

# Устанавливаем Poetry
ENV POETRY_VERSION=1.7.0
RUN pip install "poetry==$POETRY_VERSION"

# Копируем только файлы зависимостей сначала (для кэширования)
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Копируем остальной код
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]