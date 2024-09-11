sudo systemctl stop postgresql.service
sudo docker-compose up -d --build
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install poetry 
poetry install
mkdir src/log
alembic upgrade head
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload