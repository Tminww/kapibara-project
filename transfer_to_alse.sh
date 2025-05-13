#!/bin/bash
# Скрипт для подготовки архива с проектом FastAPI на Ubuntu 22.04

# Параметры
TRANSFER_DIR="$HOME/transfer"
BACKEND_DIR="/home/tminww/kapibara-prod/backend"
FRONTEND_DIR="/home/tminww/kapibara-prod/frontend"
PYTHON_VERSION="3.10.12"

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

# Скачивание Python 3.10
wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz -O "$TRANSFER_DIR/python/Python-$PYTHON_VERSION.tar.xz" || {
    echo "Ошибка: Не удалось скачать Python $PYTHON_VERSION"
    exit 1
}

# Скачивание uv
curl -LsSf https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz -o "$TRANSFER_DIR/uv/uv.tar.gz" || {
    echo "Ошибка: Не удалось скачать uv"
    exit 1
}

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
uv pip freeze > requirements.txt || {
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
pip wheel -r requirements.txt -w "$TRANSFER_DIR/wheels" || {
    echo "Ошибка: Не удалось создать колесики зависимостей"
    exit 1
}
cp requirements.txt "$TRANSFER_DIR/wheels/" || {
    echo "Ошибка: Не удалось скопировать requirements.txt"
    exit 1
}


rsync -a --exclude='.venv' "$BACKEND_DIR/" "$TRANSFER_DIR/backend/" || {
    echo "Ошибка: Не удалось переместить backend"
    exit 1
}

# Сбор зависимостей
cd "$FRONTEND_DIR" || {
    echo "Ошибка: Не удалось перейти в $FRONTEND_DIR"
    exit 1
}

# Проверка наличия uv
if ! command -v bun >/dev/null 2>&1; then
    echo "Ошибка: Bun не установлен. Установите с помощью: curl -fsSL https://bun.sh/install | bash"
    exit 1
fi

bun install || {
    echo "Ошибка: Не удалось установить зависимости bun"
    exit 1
}

bun run build --outDir "$TRANSFER_DIR/frontend/" || {
    echo "Ошибка: Не удалось собрать проект bun"
    exit 1
}



# Создание финального архива
cd "$TRANSFER_DIR" || {
    echo "Ошибка: Не удалось перейти в $TRANSFER_DIR"
    exit 1
}
tar -czf fastapi_project_transfer.tar.gz python uv wheels backend frontend deploy_on_alse.sh || {
    echo "Ошибка: Не удалось создать финальный архив"
    exit 1
}

echo "Архив готов: $TRANSFER_DIR/fastapi_project_transfer.tar.gz"