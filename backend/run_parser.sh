#!/bin/bash

# Определяем директорию, где находится этот скрипт
CURRENT_SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Определяем путь к Python-скрипту, который нужно запустить
PARSER_SCRIPT_RELATIVE_PATH="./src/parser/main.py"

CRON_LOG_DIR_RELATIVE_PATH="./logs"

CRON_LOG_FILE="$CRON_LOG_DIR_RELATIVE_PATH/cron.log"

cd $CURRENT_SCRIPT_DIR

source .venv/bin/activate

echo 'Запуск скрипта: $(date +"%Y-%m-%d-%H-%M-%S")'
python3 $PARSER_SCRIPT_RELATIVE_PATH >> $CRON_LOG_FILE 2>&1

echo "Завершение работы скрипта: $(date +"%Y-%m-%d-%H-%M-%S")"


