FROM node:latest

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем Bun
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN bun install

# Устанавливаем nginx
RUN apt update && apt install -y nginx && rm -rf /var/lib/apt/lists/*

# Удаляем дефолтный html
RUN rm -rf /var/www/html/*

# Открываем порт
EXPOSE 80
