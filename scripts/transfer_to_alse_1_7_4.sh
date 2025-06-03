#!/bin/bash
# Скрипт для подготовки архива с проектом FastAPI на Ubuntu 22.04

# Параметры
TRANSFER_DIR="$HOME/transfer"
BASE_DIR="$(pwd)"
BACKEND_DIR="$BASE_DIR/backend"
FRONTEND_DIR="$BASE_DIR/frontend"
PYTHON_VERSION="3.10.12"

echo $BASE_DIR
# Проверка наличия BACKEND_DIR
if [ ! -d "$BACKEND_DIR" ]; then
    echo "Ошибка: Директория $BACKEND_DIR не существует"
    exit 1
fi

# Создание директорий
mkdir -p "$TRANSFER_DIR"/{python,uv,wheels,backend,frontend} || {
    echo "Ошибка: Не удалось создать директории в $TRANSFER_DIR. Проверяю права доступа..."
    TRANSFER_DIR="/tmp/transfer"
    mkdir -p "$TRANSFER_DIR"/{python,uv,wheels,project} || {
        echo "Ошибка: Не удалось создать директории даже в /tmp/transfer"
        exit 1
    }
}

# Установка Python 3.10 через uv
echo "Установка Python 3.10 через uv..."
uv python install 3.10


# Скачивание uv бинарника
echo "Скачивание uv..."
mkdir -p "$TRANSFER_DIR/uv"
curl -LsSf https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz -o "$TRANSFER_DIR/uv/uv.tar.gz"

# Скачивание uv бинарника
echo "Скачивание bun..."
mkdir -p "$TRANSFER_DIR/bun"
curl -LsSf https://github.com/oven-sh/bun/releases/latest/download/bun-linux-x64.zip -o "$TRANSFER_DIR/bun/bun.zip"

# Скачивание Python 3.10 через uv
echo "Подготовка Python 3.10..."
UV_PYTHON_PATH=$(uv python find 3.10)
if [ -z "$UV_PYTHON_PATH" ]; then
    echo "Python 3.10 не найден через uv, устанавливаем..."
    uv python install 3.10
    UV_PYTHON_PATH=$(uv python find 3.10)
fi

# Копирование установленного Python
UV_PYTHON_DIR=$(dirname $(dirname "$UV_PYTHON_PATH"))
echo $UV_PYTHON_DIR
cp -r "$UV_PYTHON_DIR" "$TRANSFER_DIR/python/"

cp deploy_on_alse.sh "$TRANSFER_DIR/" || {
    echo "Ошибка: Не удалось скопировать deploy_on_alse.sh"
    exit 1
}


# Сбор зависимостей
cd "$BACKEND_DIR" || {
    echo "Ошибка: Не удалось перейти в $BACKEND_DIR"
    exit 1
}

# Проверка наличия uv
if ! command -v uv >/dev/null 2>&1; then
    echo "Ошибка: uv не установлен. Установите с помощью: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Экспорт зависимостей
uv run pip freeze > requirements.txt || {
    echo "Ошибка: Не удалось экспортировать зависимости"
    exit 1
}

# Активация виртуального окружения
source .venv/bin/activate || {
    echo "Ошибка: Не удалось активировать виртуальное окружение в $BACKEND_DIR/.venv"
    exit 1
}

# Проверка наличия pip
if ! command -v pip >/dev/null 2>&1; then
    echo "pip не найден в виртуальном окружении. Устанавливаю..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py || {
        echo "Ошибка: Не удалось скачать get-pip.py"
        exit 1
    }
    python get-pip.py || {
        echo "Ошибка: Не удалось установить pip"
        exit 1
    }
    rm get-pip.py
fi

# Создание колесиков с помощью pip wheel
uv run pip wheel -r requirements.txt -w "$TRANSFER_DIR/wheels" || {
    echo "Ошибка: Не удалось создать колесики зависимостей"
    exit 1
}
cp requirements.txt "$TRANSFER_DIR/wheels/" || {
    echo "Ошибка: Не удалось скопировать requirements.txt"
    exit 1
}

cd "$BACKEND_DIR" || {
    echo "Ошибка: Не удалось перейти в $BACKEND_DIR"
    exit 1
}
rsync -a --exclude='.venv' "$BACKEND_DIR/" "$TRANSFER_DIR/backend" || {
    echo "Ошибка: Не удалось переместить backend"
    exit 1
}

# Сбор зависимостей
cd "$FRONTEND_DIR" || {
    echo "Ошибка: Не удалось перейти в $FRONTEND_DIR"
    exit 1
}


cp -r . "$TRANSFER_DIR/frontend/" || {
    echo "Ошибка: Не удалось переместить фронтенд"
    exit 1
}

# mkdir -p "$TRANSFER_DIR/redis"
# cd $TRANSFER_DIR/redis
# sudo apt download redis redis-server redis-tools liblzf1

# Создание финального архива
cd "$TRANSFER_DIR" || {
    echo "Ошибка: Не удалось перейти в $TRANSFER_DIR"
    exit 1
}
tar -czf fastapi_project_transfer.tar.gz python uv bun wheels backend frontend redis deploy_on_alse.sh || {
    echo "Ошибка: Не удалось создать финальный архив"
    exit 1
}

echo "Архив готов: $TRANSFER_DIR/fastapi_project_transfer.tar.gz"