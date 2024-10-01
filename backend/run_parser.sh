#!/bin/bash


# Определяем директорию, где находится этот скрипт
CURRENT_SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Определяем путь к Python-скрипту, который нужно запустить
PARSER_SCRIPT_RELATIVE_PATH="./src/parser/main.py"

CRON_LOG_DIR="$SCRIPT_PARSER_PATH/logs"

CRON_LOG_FILE="$CRON_LOG_DIR/cron.log"

echo $(pwd)
cd $CURRENT_SCRIPT_DIR
echo $(pwd)

echo "начинаю запуск скрипта"
source .venv/bin/activate
python3 $PARSER_SCRIPT_RELATIVE_PATH >> "tmp.log" 2>&1

echo "Скрипт завершен"


