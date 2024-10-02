# Установка на Ubuntu

## Запуск Backend

```bash
sudo systemctl stop postgresql.service
sudo docker-compose up -d --build &&
cd backend &&
python3 -m venv .venv &&
source .venv/bin/activate &&
pip install poetry &&
poetry install &&
rm -rf src/log &&
mkdir src/log &&
alembic upgrade head &&
uvicorn src.main:app --port 8000 --reload
```
