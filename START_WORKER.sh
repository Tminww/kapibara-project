#!/bin/bash
cd backend;
uv sync;
source .venv/bin/activate;
cd src;
celery -A celery_worker worker --loglevel=info;