# Этап 1: Сборка приложения
FROM node:latest AS build

# Устанавливаем рабочую директорию
WORKDIR /code

# Устанавливаем Bun
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"

# Копируем файлы зависимостей
COPY ./package.json .
COPY ./bun.lock .

# Копируем весь проект
COPY . .

# Устанавливаем зависимости и выполняем сборку
RUN bun install
RUN bun run build

# Этап 2: Настройка Nginx для продакшена
FROM nginx:alpine

# Копируем сгенерированные файлы из этапа сборки
COPY --from=build /code/dist /usr/share/nginx/html

# Копируем конфигурацию Nginx (если есть кастомная, иначе используем дефолтную)
# Если у вас есть свой nginx.conf, раскомментируйте следующую строку и добавьте файл
# COPY nginx.conf /etc/nginx/nginx.conf

# Открываем порт 80
EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]