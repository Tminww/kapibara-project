#!/bin/bash
# Скрипт для развертывания FastAPI и фронтенда на Astra Linux SE 1.7 без БД и веб-сервера

# Параметры
ARCHIVE_PATH=$(pwd)
TRANSFER_DIR=$ARCHIVE_PATH
DEPLOY_DIR=$ARCHIVE_PATH/deploy

mkdir -p "$DEPLOY_DIR"

# Установка системных зависимостей для Python и pytesseract
echo "Установка системных зависимостей..."
sudo apt update
sudo apt upgrade -y
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev \
    libreadline-dev libffi-dev curl libbz2-dev libpq-dev tesseract-ocr libtesseract-dev || {
    echo "Ошибка: Не удалось установить системные зависимости"
    exit 1
}

# Установка Python 3.10
echo "Установка Python 3.10..."
cd "$TRANSFER_DIR/python"
tar -xf Python-3.10.12.tar.xz
cd Python-3.10.12
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall || {
    echo "Ошибка: Не удалось установить Python 3.10"
    exit 1
}

# Установка uv
echo "Установка uv..."
cd "$TRANSFER_DIR/uv"
tar -xzf uv.tar.gz
# sudo mv uv /usr/local/bin/
chmod +x /usr/local/bin/uv || {
    echo "Ошибка: Не удалось установить uv"
    exit 1
}

# Развертывание бэкенда
echo "Развертывание бэкенда..."
sudo mkdir -p "$DEPLOY_DIR"
sudo rsync -a --exclude='.venv' "$TRANSFER_DIR/backend/" "$DEPLOY_DIR/"
sudo chown -R $USER:$USER "$DEPLOY_DIR"
cd "$DEPLOY_DIR"
uv venv
source .venv/bin/activate
uv pip install --no-index --find-links="$TRANSFER_DIR/wheels" -r "$TRANSFER_DIR/wheels/requirements.txt" || {
    echo "Ошибка: Не удалось установить зависимости бэкенда"
    exit 1
}

# Развертывание фронтенда
echo "Развертывание фронтенда..."
sudo mkdir -p "$DEPLOY_DIR/frontend"
sudo cp -r "$TRANSFER_DIR/frontend/"* "$DEPLOY_DIR/frontend/"
sudo chown -R $USER:$USER "$DEPLOY_DIR/frontend" || {
    echo "Ошибка: Не удалось развернуть фронтенд"
    exit 1
}

echo "Развертывание завершено. Бэкенд: $DEPLOY_DIR, фронтенд: $DEPLOY_DIR/frontend"
echo "Для проверки бэкенда:"
echo "  cd $DEPLOY_DIR"
echo "  source .venv/bin/activate"
echo "  uvicorn main:app --host 0.0.0.0 --port 8000"
echo "Для проверки фронтенда откройте $DEPLOY_DIR/frontend/index.html в браузере"