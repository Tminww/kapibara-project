# backend/Dockerfile
FROM alpine:3.22

# Устанавливаем необходимые пакеты
RUN apk add --no-cache \
    curl \
    bash \
    tesseract-ocr \
    tesseract-ocr-data-rus \
    dcron \
    postgresql-client

# Устанавливаем uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# В Dockerfile добавьте:
RUN wget -O /usr/local/bin/supercronic https://github.com/aptible/supercronic/releases/download/v0.2.29/supercronic-linux-amd64 \
    && chmod +x /usr/local/bin/supercronic
    
# Создаем рабочую директорию
WORKDIR /code

# Копируем только файлы конфигурации для установки зависимостей
COPY .python-version pyproject.toml requirements.txt uv.lock ./

# Устанавливаем Python и зависимости
RUN uv python install $(cat .python-version) && \
    uv sync

# Создаем необходимые директории
RUN mkdir -p \
    /var/log/cron \
    /var/log/celery \
    /var/log/celery-beat \
    /var/log/backend \
    /code/celerybeat

# Настраиваем права доступа
RUN touch /var/log/cron/cron.log && \
    chmod 644 /var/log/cron/cron.log

# Точки монтирования для исходного кода
VOLUME ["/code/src", "/code/alembic", "/code/scripts"]

# Переменные окружения
ENV PYTHONPATH=/code
ENV PYTHONUNBUFFERED=1

# По умолчанию запускаем bash (команда будет переопределена в docker-compose)
CMD ["bash"]