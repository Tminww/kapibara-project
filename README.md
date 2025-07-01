# Запуск проекта в продакшен-среде на Astra Linux 1.7

## 📦 Распаковка проекта

```bash
./7zz ./kapibara.zip
```

## ⚙️ Установка и настройка Docker

```bash
cd ./kapibara/scripts
./install-docker.sh
./load-docker-images.sh
```

Проверь, что Docker-образы загружены:

```bash
docker images
```

---

## 🛠️ Настройка переменных окружения

### `kapibara/backend/.env.prod`

- Укажите собственный IP-адрес сервера **CURRENT_IP**
- Укажите URL для publication.pravo.gov.ru **EXTERNAL_URL** — например:

```env
EXTERNAL_URL=http://publication.pravo.gov.ru
CURRENT_IP=10.0.16.123
```

### `kapibara/frontend/.env`

- Укажите адрес сервера **Заменять только IP x.x.x.x!!**:

```env
VITE_PROD_PATH='http://127.0.0.1:80/api'
```

---

## 🐳 Запуск docker-compose в продакшене

```bash
docker-compose --file docker-compose.prod.yml up -d
```

Контейнеры будут запущены в фоновом режиме.

---

## 🧰 Администрирование

Используйте **LazyDocker** для мониторинга и управления:

```bash
lazydocker
```

---

## 📌 Примечания

- Убедитесь, что порты, указанные в `docker-compose.prod.yml`, открыты на сервере.
- После изменения `.env`-файлов можно перезапустить сервисы:

```bash
docker-compose --file docker-compose.prod.yml down
docker-compose --file docker-compose.prod.yml up -d
```

## ПОДДЕРЖКА

- В случае изменения исходного кода, а не переменных окружения придется заново пересобирать образы на машине с интернетом.
- Для этого используется файл docker-compose.inner.yml с флагом --build

```bash
docker-compose --file docker-compose.inner.yml up -d --build
```

И после этого в дирректории scripts запускается скрипт на сохранение новых образов

```bash
cd scripts/
./save-docker-images.sh
```
