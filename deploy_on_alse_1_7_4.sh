#!/bin/bash
# Интерактивный скрипт для развертывания FastAPI и фронтенда на Astra Linux SE 1.7

# Цвета для вывода
ERROR='\033[0;31m'
SUCCESS='\033[0;32m'
WARNING='\033[1;33m'
INFO='\033[0;36m'
PRIMARY='\033[0;37m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Функция для вывода цветного текста
print_color() {
    printf "${1}${2}${NC}\n"
}

# Функция для отображения прогресса
show_progress() {
    local duration=${1}
    local task=${2}
    local progress=0
    local bar_length=50

    while [ $progress -le 100 ]; do
        local filled=$((progress * bar_length / 100))
        local empty=$((bar_length - filled))

        printf "\r${CYAN}${task}${NC} ["
        printf "%${filled}s" | tr ' ' '█'
        printf "%${empty}s" | tr ' ' '░'
        printf "] ${progress}%%"

        progress=$((progress + 2))
        sleep 0.1
    done
    printf "\n"
}

# Функция для проверки успешности выполнения команды
check_status() {
    if [ $? -eq 0 ]; then
        print_color $SUCCESS "✓ $1 выполнено успешно"
    else
        print_color $ERROR "✗ Ошибка: $1"
        exit 1
    fi
}

# Функция для валидации порта
validate_port() {
    local port="$1"
    local min="${2:-1}"
    local max="${3:-65535}"

    # Проверяем, что это число
    if ! [[ "$port" =~ ^[0-9]+$ ]]; then
        return 1
    fi

    # Проверяем диапазон
    if [ "$port" -lt "$min" ] || [ "$port" -gt "$max" ]; then
        return 1
    fi

    return 0
}

# Функция для интерактивного ввода с валидацией
read_input() {
    local prompt="$1"
    local default="$2"
    local validation="$3"
    local value

    while true; do
        if [ -n "$default" ]; then
            printf "\033[1;33m%s [%s]: \033[0m" "$prompt" "$default" >&2
        else
            printf "\033[1;33m%s: \033[0m" "$prompt" >&2
        fi

        read value

        # Если пустой ввод и есть значение по умолчанию
        if [ -z "$value" ] && [ -n "$default" ]; then
            value="$default"
        fi

        # Проверка валидации
        if [ -z "$validation" ]; then
            # Нет валидации - принимаем любое значение
            echo "$value"
            return 0
        else
            # Есть валидация - проверяем
            if eval "testval=\"$value\"; [ \"\$testval\" != \"\" ] && $validation"; then
                echo "$value"
                return 0
            else
                printf "\033[0;31mНекорректное значение. Попробуйте еще раз.\033[0m\n" >&2
            fi
        fi
    done
}

# Функция для генерации случайного пароля
generate_password() {
    local length=${1:-16}
    openssl rand -base64 32 | tr -d "=+/" | cut -c1-${length}
}

# Заголовок
clear
print_color $PRIMARY "
██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗   ██╗
██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝
██║  ██║█████╗  ██████╔╝██║     ██║   ██║ ╚████╔╝
██║  ██║██╔══╝  ██╔═══╝ ██║     ██║   ██║  ╚██╔╝
██████╔╝███████╗██║     ███████╗╚██████╔╝   ██║
╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝
"
echo
print_color $CYAN "Интерактивный скрипт развертывания приложения"
print_color $CYAN "Astra Linux SE 1.7 | FastAPI + Frontend + PostgreSQL + Apache2"
echo

# Параметры по умолчанию
ARCHIVE_PATH=$(pwd)
TRANSFER_DIR=$ARCHIVE_PATH
DEPLOY_DIR=$ARCHIVE_PATH/deploy

# Интерактивная настройка параметров
print_color $INFO "=== НАСТРОЙКА ПАРАМЕТРОВ РАЗВЕРТЫВАНИЯ ==="
echo

# Путь развертывания
DEPLOY_DIR=$(read_input "Путь для развертывания" "$DEPLOY_DIR")

# Настройки PostgreSQL
echo
print_color $INFO "=== НАСТРОЙКИ POSTGRESQL ==="
echo
DB_NAME=$(read_input "Имя базы данных" "kapibara")
DB_USER=$(read_input "Пользователь базы данных" "kapibara")
DB_PASSWORD=$(read_input "Пароль базы данных (оставьте пустым для автогенерации)" "")
if [ -z "$DB_PASSWORD" ]; then
    DB_PASSWORD=$(generate_password 16)
    print_color $SUCCESS "Сгенерирован пароль: $DB_PASSWORD"
fi
DB_HOST=$(read_input "Хост базы данных" "localhost")
DB_PORT=$(read_input "Порт базы данных" "5432" '[[ "$testval" =~ ^[0-9]+$ ]] && [ "$testval" -ge 1 ] && [ "$testval" -le 65535 ]')

# Настройки бэкенда
echo
print_color $INFO "=== НАСТРОЙКИ BACKEND ==="
echo

# Путь к файлам
ENV_EXAMPLE_PATH="$TRANSFER_DIR/backend/.env.example"
ENV_PATH="$TRANSFER_DIR/backend/.env"

# Проверяем существование .env.example
if [ ! -f "$ENV_EXAMPLE_PATH" ]; then
    print_color $ERROR "Файл .env.example не найден по пути: $ENV_EXAMPLE_PATH"
    exit 1
fi

# Интерактивный ввод параметров
BACKEND_HOST=$(read_input "Хост бэкенда" "127.0.0.1")
BACKEND_PORT=$(read_input "Порт бэкенда" "8080" '[[ "$testval" =~ ^[0-9]+$ ]] && [ "$testval" -ge 1000 ] && [ "$testval" -le 65535 ]')

# База данных
echo
# print_color $INFO "=== НАСТРОЙКИ БАЗЫ ДАННЫХ ==="
DB_HOST=$(read_input "Хост базы данных" "localhost")
DB_PORT=$(read_input "Порт базы данных" "5432" '[[ "$testval" =~ ^[0-9]+$ ]] && [ "$testval" -ge 1 ] && [ "$testval" -le 65535 ]')
DB_USER=$(read_input "Пользователь базы данных" "kapibara")
DB_PASS=$(read_input "Пароль базы данных (оставьте пустым для автогенерации)" "")
DB_NAME=$(read_input "Имя базы данных" "kapibara")

# Redis
echo
# print_color $INFO "=== НАСТРОЙКИ REDIS ==="
REDIS_HOST=$(read_input "Хост Redis" "localhost")
REDIS_PORT=$(read_input "Порт Redis" "6379" '[[ "$testval" =~ ^[0-9]+$ ]] && [ "$testval" -ge 1 ] && [ "$testval" -le 65535 ]')
REDIS_DB=$(read_input "База данных Redis" "0")

# Внешние сервисы
echo
# print_color $INFO "=== НАСТРОЙКИ ВНЕШНИХ СЕРВИСОВ ==="
EXTERNAL_URL=$(read_input "URL внешнего API" "http://publication.pravo.gov.ru")
PROXY=$(read_input "Прокси (оставьте пустым если не используется)" "http://10.0.0.1:3128")

# SMTP
echo
# print_color $INFO "=== НАСТРОЙКИ SMTP ==="
SMTP_SERVER=$(read_input "SMTP сервер" "localhost")
SMTP_PORT=$(read_input "SMTP порт" "8025" '[[ "$testval" =~ ^[0-9]+$ ]] && [ "$testval" -ge 1 ] && [ "$testval" -le 65535 ]')
SMTP_USERNAME=$(read_input "SMTP логин" "your-email@gmail.com")
SMTP_PASSWORD=$(read_input "SMTP пароль (оставьте пустым для автогенерации)" "")
if [ -z "$SMTP_PASSWORD" ]; then
    SMTP_PASSWORD=$(generate_password 16)
    print_color $SUCCESS "Сгенерирован SMTP пароль: $SMTP_PASSWORD"
fi
FROM_EMAIL=$(read_input "Email отправителя" "publication@analiz.com")

# Создание .env файла на основе .env.example с заменой значений
print_color $CYAN "Создание файла .env..."

# Копируем .env.example в .env
cp "$ENV_EXAMPLE_PATH" "$ENV_PATH"

# Заменяем значения в .env файле
sed -i "s|^DB_HOST=.*|DB_HOST=$DB_HOST|" "$ENV_PATH"
sed -i "s|^DB_PORT=.*|DB_PORT=$DB_PORT|" "$ENV_PATH"
sed -i "s|^DB_USER=.*|DB_USER=$DB_USER|" "$ENV_PATH"
sed -i "s|^DB_PASS=.*|DB_PASS=$DB_PASS|" "$ENV_PATH"
sed -i "s|^DB_NAME=.*|DB_NAME=$DB_NAME|" "$ENV_PATH"

sed -i "s|^EXTERNAL_URL=.*|EXTERNAL_URL=$EXTERNAL_URL|" "$ENV_PATH"
sed -i "s|^PROXY=.*|PROXY=$PROXY|" "$ENV_PATH"

sed -i "s|^HOST=.*|HOST=$BACKEND_HOST|" "$ENV_PATH"
sed -i "s|^PORT=.*|PORT=$BACKEND_PORT|" "$ENV_PATH"

sed -i "s|^REDIS_HOST=.*|REDIS_HOST=$REDIS_HOST|" "$ENV_PATH"
sed -i "s|^REDIS_PORT=.*|REDIS_PORT=$REDIS_PORT|" "$ENV_PATH"
sed -i "s|^REDIS_DB=.*|REDIS_DB=$REDIS_DB|" "$ENV_PATH"

# Обновляем CELERY URLs с новыми параметрами Redis
sed -i "s|^CELERY_BROKER_URL=.*|CELERY_BROKER_URL=redis://$REDIS_HOST:$REDIS_PORT/$REDIS_DB|" "$ENV_PATH"
sed -i "s|^CELERY_RESULT_BACKEND=.*|CELERY_RESULT_BACKEND=redis://$REDIS_HOST:$REDIS_PORT/$REDIS_DB|" "$ENV_PATH"

sed -i "s|^SMTP_SERVER=.*|SMTP_SERVER=$SMTP_SERVER|" "$ENV_PATH"
sed -i "s|^SMTP_PORT=.*|SMTP_PORT=$SMTP_PORT|" "$ENV_PATH"
sed -i "s|^SMTP_USERNAME=.*|SMTP_USERNAME=$SMTP_USERNAME|" "$ENV_PATH"
sed -i "s|^SMTP_PASSWORD=.*|SMTP_PASSWORD=$SMTP_PASSWORD|" "$ENV_PATH"
sed -i "s|^FROM_EMAIL=.*|FROM_EMAIL=$FROM_EMAIL|" "$ENV_PATH"

check_status "Создание .env файла"

print_color $SUCCESS "✓ Файл .env создан по пути: $ENV_PATH"

# Показываем содержимое созданного файла для проверки
echo
print_color $INFO "=== СОДЕРЖИМОЕ СОЗДАННОГО .ENV ФАЙЛА ==="
print_color $CYAN "Путь: $ENV_PATH"
echo
cat "$ENV_PATH"
echo

# Настройки фронтенда
echo
print_color $INFO "=== НАСТРОЙКИ FRONTEND ==="
echo
API_URL=$(read_input "URL API для фронтенда" "http://localhost:$BACKEND_PORT")
FRONTEND_TITLE=$(read_input "Заголовок приложения" "My Application")

# Настройки Apache
echo
print_color $INFO "=== НАСТРОЙКИ APACHE ==="
echo
APACHE_PORT=$(read_input "Порт Apache для фронтенда" "80")
while ! validate_port "$APACHE_PORT" 80 65535; do
    printf "\033[0;31mНекорректный порт. Введите число от 80 до 65535.\033[0m\n"
    APACHE_PORT=$(read_input "Порт Apache для фронтенда" "80")
done
SERVER_NAME=$(read_input "Имя сервера" "localhost")

echo
print_color $WARNING "Проверьте настройки:"
echo "Путь развертывания: $DEPLOY_DIR"
echo "База данных: $DB_NAME @ $DB_HOST:$DB_PORT (пользователь: $DB_USER)"
echo "Бэкенд: $BACKEND_HOST:$BACKEND_PORT"
echo "Фронтенд: $SERVER_NAME:$APACHE_PORT"
echo

while true; do
    printf "${WARNING}Продолжить развертывание? (y/n): ${NC}"
    read confirm
    case $confirm in
        [Yy]* ) break;;
        [Nn]* ) print_color $ERROR "Развертывание отменено"; exit 0;;
        * ) print_color $ERROR "Пожалуйста, ответьте y или n";;
    esac
done

# Создание директории развертывания
mkdir -p "$DEPLOY_DIR"

print_color $INFO "\n=== УСТАНОВКА СИСТЕМНЫХ ЗАВИСИМОСТЕЙ ==="

# Обновление системы
print_color $CYAN "Обновление системы..."
show_progress 3 "Обновление пакетов"
sudo apt update && sudo apt upgrade -y >/dev/null 2>&1
check_status "Обновление системы"

# Установка базовых зависимостей
print_color $CYAN "Установка базовых зависимостей..."
show_progress 2 "Установка tesseract-ocr unzip"
sudo apt install -y tesseract-ocr unzip >/dev/null 2>&1
check_status "Установка базовых зависимостей"

print_color $INFO "\n=== УСТАНОВКА POSTGRESQL ==="

# Установка PostgreSQL
print_color $CYAN "Установка PostgreSQL..."
show_progress 4 "Установка PostgreSQL"
sudo apt install -y postgresql >/dev/null 2>&1
check_status "Установка PostgreSQL"

# Запуск PostgreSQL
print_color $CYAN "Запуск службы PostgreSQL..."
sudo systemctl start postgresql
sudo systemctl enable postgresql >/dev/null 2>&1
check_status "Запуск PostgreSQL"

# Настройка базы данных
print_color $CYAN "Настройка базы данных..."
sudo -u postgres psql <<EOF >/dev/null 2>&1
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
ALTER USER $DB_USER CREATEDB;
\q
EOF
check_status "Создание базы данных и пользователя"

print_color $INFO "\n=== УСТАНОВКА APACHE2 ==="

# Установка Apache2
print_color $CYAN "Установка Apache2..."
show_progress 3 "Установка Apache2"
sudo apt install -y apache2 >/dev/null 2>&1
check_status "Установка Apache2"

# Включение модулей Apache
print_color $CYAN "Настройка модулей Apache..."
sudo a2enmod rewrite proxy proxy_http >/dev/null 2>&1
check_status "Включение модулей Apache"

print_color $INFO "\n=== УСТАНОВКА UV И PYTHON ==="


# Установка uv в пользовательскую папку
print_color $CYAN "Установка uv..."

# Создаем локальную папку bin если её нет
mkdir -p "$HOME/.local/bin"

if [ -d "$TRANSFER_DIR/uv" ]; then
    cd "$TRANSFER_DIR/uv"
    tar -xzf uv.tar.gz >/dev/null 2>&1
    cd uv-*
    
    # Копируем в локальную папку пользователя
    cp uv "$HOME/.local/bin/"
    chmod +x "$HOME/.local/bin/uv"
    
    # Добавляем в PATH если ещё не добавлено
    if ! echo $PATH | grep -q "$HOME/.local/bin"; then
        export PATH="$HOME/.local/bin:$PATH"
        
        # Добавляем в bashrc/profile для постоянного использования
        if [ -f "$HOME/.bashrc" ]; then
            if ! grep -q "export PATH=\"\$HOME/.local/bin:\$PATH\"" "$HOME/.bashrc"; then
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
            fi
        elif [ -f "$HOME/.profile" ]; then
            if ! grep -q "export PATH=\"\$HOME/.local/bin:\$PATH\"" "$HOME/.profile"; then
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.profile"
            fi
        fi
    fi
    
    check_status "Установка uv"
    print_color $SUCCESS "uv установлен в $HOME/.local/bin/"
    print_color $INFO "Путь $HOME/.local/bin добавлен в PATH"
else
    print_color $WARNING "Папка uv не найдена..."
fi


# Установка bun в пользовательскую папку
print_color $CYAN "Установка bun..."

# Создаем локальную папку bin если её нет
mkdir -p "$HOME/.local/bin"

if [ -d "$TRANSFER_DIR/bun" ]; then
    cd "$TRANSFER_DIR/bun"
    unzip -q bun.zip >/dev/null 2>&1
    cd bun-*
    
    # Копируем в локальную папку пользователя
    cp bun "$HOME/.local/bin/"
    chmod +x "$HOME/.local/bin/bun"
    
    # Добавляем в PATH если ещё не добавлено
    if ! echo $PATH | grep -q "$HOME/.local/bin"; then
        export PATH="$HOME/.local/bin:$PATH"
        
        # Добавляем в bashrc/profile для постоянного использования
        if [ -f "$HOME/.bashrc" ]; then
            if ! grep -q "export PATH=\"\$HOME/.local/bin:\$PATH\"" "$HOME/.bashrc"; then
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
            fi
        elif [ -f "$HOME/.profile" ]; then
            if ! grep -q "export PATH=\"\$HOME/.local/bin:\$PATH\"" "$HOME/.profile"; then
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.profile"
            fi
        fi
    fi
    
    check_status "Установка bun"
    print_color $SUCCESS "bun установлен в $HOME/.local/bin/"
    print_color $INFO "Путь $HOME/.local/bin добавлен в PATH"
else
    print_color $WARNING "Папка bun не найдена..."
fi


# Установка Python 3.10
print_color $CYAN "Установка Python 3.10..."

if [ -d "$TRANSFER_DIR/python" ]; then
    cd "$TRANSFER_DIR/python"
    show_progress 2 "Копирование Python в директорию uv"
    
    # Получаем директорию где uv хранит версии Python
    UV_PYTHON_DIR=$("$HOME/.local/bin/uv" python dir 2>/dev/null)
    
    if [ -n "$UV_PYTHON_DIR" ]; then
        # Создаем директорию если её нет
        mkdir -p "$UV_PYTHON_DIR"
        
        # Копируем готовую версию Python в директорию uv
        cp -r cpython-3.10.17-linux-x86_64-gnu "$UV_PYTHON_DIR/" >/dev/null 2>&1
        
        check_status "Установка Python 3.10"
        
        # Проверяем что Python доступен через uv
        if "$HOME/.local/bin/uv" python list | grep -q "3.10"; then
            print_color $SUCCESS "Python 3.10 успешно установлен в $UV_PYTHON_DIR"
        else
            print_color $INFO "Python скопирован, но может потребоваться время для обнаружения uv"
        fi
    else
        print_color $WARNING "Не удалось определить директорию uv python, устанавливаем через uv install"
        "$HOME/.local/bin/uv" python install 3.10 >/dev/null 2>&1
        check_status "Установка Python 3.10"
    fi
else
    print_color $WARNING "Python не найден в архиве, устанавливаем через uv..."
    "$HOME/.local/bin/uv" python install 3.10 >/dev/null 2>&1
    check_status "Установка Python 3.10"
fi

print_color $INFO "\n=== РАЗВЕРТЫВАНИЕ БЭКЕНДА ==="

# Развертывание бэкенда
print_color $CYAN "Копирование файлов бэкенда..."
sudo mkdir -p "$DEPLOY_DIR"
cp -r "$TRANSFER_DIR/backend/" "$DEPLOY_DIR/backend/" 2>/dev/null
check_status "Копирование бэкенда"

cd "$DEPLOY_DIR/backend"

# Установка зависимостей бэкенда
print_color $CYAN "Установка зависимостей бэкенда..."
show_progress 5 "Установка Python пакетов"
uv sync >/dev/null 2>&1

if [ -d "$TRANSFER_DIR/wheels" ]; then
    uv run pip install --no-index --find-links="$TRANSFER_DIR/wheels" -r "$TRANSFER_DIR/wheels/requirements.txt" >/dev/null 2>&1
fi
check_status "Установка зависимостей бэкенда"

print_color $INFO "\n=== РАЗВЕРТЫВАНИЕ ФРОНТЕНДА ==="

# Развертывание фронтенда
print_color $CYAN "Копирование файлов фронтенда..."
sudo mkdir -p "$DEPLOY_DIR/frontend"
sudo cp -r "$TRANSFER_DIR/frontend/"* "$DEPLOY_DIR/frontend/" 2>/dev/null
sudo chown -R $USER:$USER "$DEPLOY_DIR/frontend"
check_status "Копирование фронтенда"

# Создание .env файла для фронтенда
print_color $CYAN "Создание конфигурации фронтенда..."
cat > "$DEPLOY_DIR/frontend/.env" <<EOF
# API Configuration
VITE_API_URL=$API_URL
VITE_API_TIMEOUT=30000

# Application Configuration
VITE_APP_TITLE=$FRONTEND_TITLE
VITE_APP_VERSION=1.0.0

# Environment
VITE_ENVIRONMENT=production
VITE_DEBUG=false
EOF
check_status "Создание .env файла фронтенда"

print_color $INFO "\n=== НАСТРОЙКА APACHE ==="

# Создание конфигурации Apache для фронтенда
print_color $CYAN "Создание конфигурации Apache..."
sudo tee /etc/apache2/sites-available/frontend.conf >/dev/null <<EOF
<VirtualHost *:$APACHE_PORT>
    ServerName $SERVER_NAME
    DocumentRoot $DEPLOY_DIR/frontend

    <Directory $DEPLOY_DIR/frontend>
        AllowOverride All
        Require all granted
        Options Indexes FollowSymLinks

        # SPA поддержка
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>

    # Прокси для API
    ProxyPreserveHost On
    ProxyPass /api/ http://$BACKEND_HOST:$BACKEND_PORT/
    ProxyPassReverse /api/ http://$BACKEND_HOST:$BACKEND_PORT/

    ErrorLog \${APACHE_LOG_DIR}/frontend_error.log
    CustomLog \${APACHE_LOG_DIR}/frontend_access.log combined
</VirtualHost>
EOF

# Изменение порта Apache если нужно
if [ "$APACHE_PORT" != "80" ]; then
    sudo sed -i "s/Listen 80/Listen $APACHE_PORT/" /etc/apache2/ports.conf
fi

# Активация сайта
sudo a2ensite frontend.conf >/dev/null 2>&1
sudo a2dissite 000-default >/dev/null 2>&1
check_status "Настройка Apache"

# Перезапуск Apache
print_color $CYAN "Перезапуск Apache..."
sudo systemctl restart apache2
check_status "Перезапуск Apache"

print_color $INFO "\n=== СОЗДАНИЕ SYSTEMD СЕРВИСА ДЛЯ БЭКЕНДА ==="

# Создание systemd сервиса для бэкенда
print_color $CYAN "Создание systemd сервиса..."
sudo tee /etc/systemd/system/fastapi-app.service >/dev/null <<EOF
[Unit]
Description=FastAPI Application
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$DEPLOY_DIR/backend
Environment=PATH=$DEPLOY_DIR/backend/.venv/bin
ExecStart=$DEPLOY_DIR/backend/.venv/bin/python src/main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable fastapi-app >/dev/null 2>&1
check_status "Создание systemd сервиса"

print_color $INFO "\n=== ЗАПУСК ПРИЛОЖЕНИЯ ==="

# Запуск бэкенда
print_color $CYAN "Запуск бэкенда..."
sudo systemctl start fastapi-app
sleep 2
if sudo systemctl is-active --quiet fastapi-app; then
    check_status "Запуск бэкенда"
else
    print_color $WARNING "⚠ Бэкенд не запустился автоматически"
fi

print_color $SUCCESS "\n🎉 РАЗВЕРТЫВАНИЕ ЗАВЕРШЕНО УСПЕШНО! 🎉\n"

# Информация о развертывании
print_color $CYAN "=== ИНФОРМАЦИЯ О РАЗВЕРТЫВАНИИ ==="
echo
print_color $INFO "📂 Пути:"
echo "   Бэкенд: $DEPLOY_DIR/backend"
echo "   Фронтенд: $DEPLOY_DIR/frontend"
echo
print_color $INFO "🌐 Доступ к приложению:"
echo "   Фронтенд: http://$SERVER_NAME:$APACHE_PORT"
echo "   API: http://$BACKEND_HOST:$BACKEND_PORT"
echo
print_color $INFO "🗄️  База данных:"
echo "   Хост: $DB_HOST:$DB_PORT"
echo "   База: $DB_NAME"
echo "   Пользователь: $DB_USER"
echo "   Пароль: $DB_PASSWORD"
echo
print_color $INFO "🔧 Управление сервисами:"
echo "   Статус бэкенда: sudo systemctl status fastapi-app"
echo "   Перезапуск бэкенда: sudo systemctl restart fastapi-app"
echo "   Статус Apache: sudo systemctl status apache2"
echo "   Перезапуск Apache: sudo systemctl restart apache2"
echo "   Статус PostgreSQL: sudo systemctl status postgresql"
echo
print_color $INFO "📋 Логи:"
echo "   Бэкенд: sudo journalctl -u fastapi-app -f"
echo "   Apache: sudo tail -f /var/log/apache2/frontend_error.log"
echo "   PostgreSQL: sudo tail -f /var/log/postgresql/postgresql-*.log"
echo

# Сохранение информации в файл
INFO_FILE="$DEPLOY_DIR/deployment-info.txt"
cat > "$INFO_FILE" <<EOF
Информация о развертывании
Дата: $(date)

Пути:
- Бэкенд: $DEPLOY_DIR/backend
- Фронтенд: $DEPLOY_DIR/frontend

Доступ:
- Фронтенд: http://$SERVER_NAME:$APACHE_PORT
- API: http://$BACKEND_HOST:$BACKEND_PORT

База данных:
- Хост: $DB_HOST:$DB_PORT
- База: $DB_NAME
- Пользователь: $DB_USER
- Пароль: $DB_PASSWORD

Команды управления:
- Статус бэкенда: sudo systemctl status fastapi-app
- Перезапуск бэкенда: sudo systemctl restart fastapi-app
- Статус Apache: sudo systemctl status apache2
- Статус PostgreSQL: sudo systemctl status postgresql

Логи:
- Бэкенд: sudo journalctl -u fastapi-app -f
- Apache: sudo tail -f /var/log/apache2/frontend_error.log
EOF

print_color $SUCCESS "💾 Информация сохранена в файл: $INFO_FILE"

print_color $PRIMARY "\n✨ Приложение готово к использованию! ✨"
