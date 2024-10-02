#!/bin/bash

# Определяем директорию, где находится этот скрипт
CURRENT_SCRIPT_PATH="$(dirname "$(realpath "$0")")"

# Определяем путь к Python-скрипту, который нужно запустить
RUN_PARSER_SCRIPT_PATH="$CURRENT_SCRIPT_PATH/backend/run_parser.sh"

chmod +x $RUN_PARSER_SCRIPT_PATH

# Запланированное время для задачи cron (например, каждую минуту)
# `* * * * *` — каждый minute
# `*/5 * * * *` — каждые 5 минут
# `0 * * * *` — каждый час (в начале)
# `0 0 * * *` — каждый день в полночь
CRON_SCHEDULE="*/10 * * * *"

# Создание уникального лог-файла с датой и временем
CRON_LOG_DIR="$CURRENT_SCRIPT_PATH/backend/logs"

mkdir $CRON_LOG_DIR

CRON_LOG_FILE="$CRON_LOG_DIR/cron.log"


# Полная строка для crontab
CRON_JOB="$CRON_SCHEDULE $RUN_PARSER_SCRIPT_PATH >> $CRON_LOG_FILE 2>&1"

# Проверка, существует ли уже такая запись в crontab
crontab -l | grep -F "$CRON_JOB" > /dev/null

if [ $? -eq 0 ]; then
    echo "Crontab уже содержит запись для $CRON_JOB"
else
    # Добавление новой задачи в crontab
    (crontab -l; echo "$CRON_JOB") | crontab -
    echo "Запись добавлена в crontab: $CRON_JOB"
fi