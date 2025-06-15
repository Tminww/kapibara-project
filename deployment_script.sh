#!/bin/bash
# deploy_offline.sh - Скрипт для развертывания на целевой машине

set -e

PACKAGE_NAME=""
EXTRACT_DIR="kapibara_deployment"

# Функция помощи
show_help() {
    cat << EOF
Использование: $0 [ОПЦИИ] АРХИВ

Развертывание Kapibara из оффлайн пакета

ОПЦИИ:
    -h, --help          Показать эту справку
    -d, --dir DIR       Директория для извлечения (по умолчанию: $EXTRACT_DIR)
    --no-start          Не запускать контейнеры после импорта
    --cleanup           Удалить временные файлы после развертывания

ПРИМЕРЫ:
    $0 kapibara_offline_20241215_143022.tar.gz
    $0 -d /opt/kapibara --no-start package.tar.gz
EOF
}

# Парсинг аргументов
AUTO_START=true
CLEANUP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -d|--dir)
            EXTRACT_DIR="$2"
            shift 2
            ;;
        --no-start)
            AUTO_START=false
            shift
            ;;
        --cleanup)
            CLEANUP=true
            shift
            ;;
        -*)
            echo "❌ Неизвестная опция: $1"
            show_help
            exit 1
            ;;
        *)
            if [ -z "$PACKAGE_NAME" ]; then
                PACKAGE_NAME="$1"
            else
                echo "❌ Слишком много аргументов"
                show_help
                exit 1
            fi
            shift
            ;;
    esac
done

# Проверяем аргументы
if [ -z "$PACKAGE_NAME" ]; then
    echo "❌ Не указан файл пакета"
    show_help
    exit 1
fi

if [ ! -f "$PACKAGE_NAME" ]; then
    echo "❌ Файл $PACKAGE_NAME не найден"
    exit 1
fi

# Проверяем Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен"
    exit 1
fi

echo "🚀 Развертывание Kapibara из $PACKAGE_NAME"

# Создаем директорию и распаковываем
echo "📦 Извлечение архива..."
mkdir -p "$EXTRACT_DIR"
tar -xzf "$PACKAGE_NAME" -C "$EXTRACT_DIR" --strip-components=1

# Переходим в директорию
cd "$EXTRACT_DIR"

# Проверяем наличие необходимых файлов
if [ ! -f "import_images.sh" ]; then
    echo "❌ Неверный формат пакета: import_images.sh не найден"
    exit 1
fi

if [ ! -f "docker-compose.inner.yml" ]; then
    echo "❌ Неверный формат пакета: docker-compose.inner.yml не найден"
    exit 1
fi

# Проверяем postgres.env
if [ ! -f "postgres.env" ]; then
    echo "⚠️  Файл postgres.env не найден, создаем пример..."
    cat > postgres.env << EOF
POSTGRES_DB=kapibara
POSTGRES_USER=kapibara
POSTGRES_PASSWORD=kapibara_password_$(date +%s)
EOF
    echo "📝 Отредактируйте postgres.env перед запуском"
fi

# Импортируем образы
echo "🔄 Импорт Docker образов..."
chmod +x import_images.sh
./import_images.sh

# Запускаем контейнеры, если требуется
if [ "$AUTO_START" = true ]; then
    echo "🚀 Запуск контейнеров..."
    docker-compose -f docker-compose.inner.yml up -d
    
    echo "⏳ Ожидание запуска сервисов..."
    sleep 10
    
    # Проверяем статус
    echo "📊 Статус контейнеров:"
    docker-compose -f docker-compose.inner.yml ps
    
    echo ""
    echo "✅ Развертывание завершено!"
    echo "🌐 Доступные сервисы:"
    echo "   Frontend:  http://localhost"
    echo "   Backend:   http://localhost:8080"
    echo "   MailDev:   http://localhost:8090"
    echo "   PostgreSQL: localhost:54321"
    echo "   Redis:     localhost:6379"
    echo ""
    echo "📋 Команды управления:"
    echo "   Логи:      docker-compose -f docker-compose.inner.yml logs -f"
    echo "   Остановка: docker-compose -f docker-compose.inner.yml down"
    echo "   Перезапуск: docker-compose -f docker-compose.inner.yml restart"
else
    echo "✅ Образы импортированы. Для запуска выполните:"
    echo "   cd $EXTRACT_DIR"
    echo "   docker-compose -f docker-compose.inner.yml up -d"
fi

# Очистка временных файлов
if [ "$CLEANUP" = true ]; then
    echo "🧹 Очистка временных файлов..."
    rm -rf images/
    rm import_images.sh
fi

echo "📂 Проект развернут в: $(pwd)"