# Установка на Ubuntu

`cd backend`
`python3 -m venv .venv`
`source .venv/bin/activate`
`pip install poetry`
`poetry install`
`mkdir src/log`
`alembic upgrade head`
`uvicorn src.main:app --port 8000 --reload`
