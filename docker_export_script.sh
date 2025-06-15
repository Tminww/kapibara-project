#!/bin/bash

# Скрипт для экспорта всех образов проекта Kapibara
# Запускать в корне проекта

set -e

EXPORT_DIR="kapibara_offline_package"
IMAGES_DIR="$EXPORT_DIR/images"

echo "🚀 Создание пакета для оффлайн развертывания..."

# Создаем директории
mkdir -p "$IMAGES_DIR"

# Собираем все образы из docker-compose
echo "📦 Сборка образов..."
docker-compose -f docker-compose.inner.yml build

# Список образов для экспорта
IMAGES=(
    "postgres:16"
    "redis:7-alpine" 
    "maildev/maildev"
)

# Получаем имена собранных образов для backend и frontend
BACKEND_IMAGE=$(docker-compose -f docker-compose.inner.yml config | grep -A5 "backend:" | grep "image:" | awk '{print $2}' || echo "kapibara_backend")
FRONTEND_IMAGE=$(docker-compose -f docker-compose.inner.yml config | grep -A5 "frontend:" | grep "image:" | awk '{print $2}' || echo "kapibara_frontend")
APACHE_IMAGE=$(docker-compose -f docker-compose.inner.yml config | grep -A5 "apache:" | grep "image:" | awk '{print $2}' || echo "kapibara_apache")

# Если образы не найдены в config, используем стандартные имена
if [ "$BACKEND_IMAGE" = "kapibara_backend" ]; then
    BACKEND_IMAGE="kapibara-inner_backend"
fi
if [ "$FRONTEND_IMAGE" = "kapibara_frontend" ]; then
    FRONTEND_IMAGE="kapibara-inner_frontend"
fi
if [ "$APACHE_IMAGE" = "kapibara_apache" ]; then
    APACHE_IMAGE="kapibara-inner_apache"
fi

# Добавляем собранные образы в список
IMAGES+=("$BACKEND_IMAGE" "$FRONTEND_IMAGE" "$APACHE_IMAGE")

echo "📥 Скачивание внешних образов..."
for image in "postgres:16" "redis:7-alpine" "maildev/maildev"; do
    echo "Pulling $image..."
    docker pull "$image"
done

echo "💾 Экспорт образов..."
for image in "${IMAGES[@]}"; do
    echo "Экспорт $image..."
    safe_name=$(echo "$image" | sed 's/[\/:]/_/g')
    docker save "$image" | gzip > "$IMAGES_DIR/${safe_name}.tar.gz"
done

# Копируем исходный код и конфигурацию
echo "📁 Копирование файлов проекта..."
cp -r apache "$EXPORT_DIR/"
cp -r backend "$EXPORT_DIR/"
cp -r frontend "$EXPORT_DIR/"
cp docker-compose.inner.yml "$EXPORT_DIR/"
cp postgres.env "$EXPORT_DIR/" 2>/dev/null || echo "⚠️  postgres.env не найден, создайте его вручную"

# Создаем скрипт для импорта
cat > "$EXPORT_DIR/import_images.sh" << 'EOF'
#!/bin/bash
# Скрипт для импорта образов на целевой машине

set -e

echo "🔄 Импорт Docker образов..."

IMAGES_DIR="images"

if [ ! -d "$IMAGES_DIR" ]; then
    echo "❌ Директория $IMAGES_DIR не найдена!"
    exit 1
fi

for image_file in "$IMAGES_DIR"/*.tar.gz; do
    if [ -f "$image_file" ]; then
        echo "Импорт $(basename "$image_file")..."
        gunzip -c "$image_file" | docker load
    fi
done

echo "✅ Все образы импортированы!"
echo "📋 Список доступных образов:"
docker images --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}"

echo ""
echo "🚀 Для запуска выполните:"
echo "   docker-compose -f docker-compose.inner.yml up -d"
EOF

chmod +x "$EXPORT_DIR/import_images.sh"

# Создаем README
cat > "$EXPORT_DIR/README.md" << 'EOF'
# Kapibara Offline Package

Этот пакет содержит все необходимое для запуска проекта Kapibara без доступа к интернету.

## Требования
- Docker
- Docker Compose

## Установка

1. Импортируйте образы:
   ```bash
   ./import_images.sh
   ```

2. Убедитесь, что файл `postgres.env` содержит корректные настройки БД:
   ```
   POSTGRES_DB=kapibara
   POSTGRES_USER=kapibara
   POSTGRES_PASSWORD=your_password
   ```

3. Запустите контейнеры:
   ```bash
   docker-compose -f docker-compose.inner.yml up -d
   ```

## Проверка
- Frontend: http://localhost (через Apache)
- Backend API: http://localhost:8080
- MailDev: http://localhost:8090
- PostgreSQL: localhost:54321
- Redis: localhost:6379

## Логи
```bash
docker-compose -f docker-compose.inner.yml logs -f
```

## Остановка
```bash
docker-compose -f docker-compose.inner.yml down
```
EOF

# Создаем архив
echo "🗜️  Создание архива..."
tar -czf "kapibara_offline_$(date +%Y%m%d_%H%M%S).tar.gz" "$EXPORT_DIR"

echo "✅ Пакет готов!"
echo "📦 Размер директории: $(du -sh "$EXPORT_DIR" | cut -f1)"
echo "📦 Размер архива: $(du -sh kapibara_offline_*.tar.gz | cut -f1)"
echo ""
echo "🚛 Для переноса скопируйте архив kapibara_offline_*.tar.gz на целевую машину"
echo "📂 Или скопируйте всю директорию $EXPORT_DIR"