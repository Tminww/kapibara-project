#!/bin/bash

# Скрипт для замены адресов во всех файлах dist/

OLD_IP="127.0.0.1"
# Новый IP (адрес сервера)
NEW_IP="192.168.1.100"

OLD_PRAVO="publication.pravo.gov.ru"

# Новый адрес для pravo.gov.ru
NEW_PRAVO="new.pravo.gov.ru"

# Путь к папке dist
DIST_DIR="../frontend/dist"

# Проверка наличия папки
if [[ ! -d "$DIST_DIR" ]]; then
  echo "Папка $DIST_DIR не найдена!"
  exit 1
fi

echo "Меняем 127.0.0.1 → $NEW_IP"
grep -rl "$OLD_IP" "$DIST_DIR" | xargs sed -i "s|$OLD_IP|$NEW_IP|g"

echo "Меняем $OLD_PRAVO → $NEW_PRAVO"
grep -rl "$OLD_PRAVO" "$DIST_DIR" | xargs sed -i "s|$OLD_PRAVO|$NEW_PRAVO|g"

echo "✅ Замены выполнены во всех файлах в $DIST_DIR!"
