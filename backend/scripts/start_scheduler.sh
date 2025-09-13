#!/bin/bash

# Адаптация вашего оригинального скрипта для Docker окружения
SCRIPT_DIR=$(pwd)
BASE_DIR=$(dirname $SCRIPT_DIR)
BACKEND_DIR="/code"  # В Docker это будет /code
LOGFILE="/var/log/cron/cron.log"

# Функция логирования
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $1" >> "$LOGFILE"
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $1"
}

log "=== Starting scheduler task ==="
log "Backend directory: $BACKEND_DIR"

echo $BACKEND_DIR 
cd $BACKEND_DIR

# В Docker контейнере активируем виртуальное окружение
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
    log "Activating virtual environment at $BACKEND_DIR/.venv"
    source .venv/bin/activate
    log "Virtual environment activated"
else
    log "No .venv found, trying uv environment..."
    # Fallback на uv, если .venv не найден
    if command -v uv >/dev/null 2>&1; then
        log "Using uv environment"
        export PATH="/root/.local/bin:$PATH"
    else
        log "ERROR: Neither .venv nor uv found"
        exit 1
    fi
fi

cd "$BACKEND_DIR/src/"
log "Current directory: $(pwd)"
log "Python executable: $(which python3)"

# Запускаем вашу задачу точно как в оригинале
log "Executing: python3 -m scripts.run_scheduler_task"

python3 -m scripts.run_scheduler_task