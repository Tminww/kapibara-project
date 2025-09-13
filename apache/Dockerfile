# Proxy Dockerfile
FROM httpd:2.4-alpine

# Устанавливаем необходимые утилиты
RUN apk add --no-cache apache2-utils openssl

# Точка монтирования для конфигурации
VOLUME ["/usr/local/apache2/conf"]

# Открываем порты
EXPOSE 80 443