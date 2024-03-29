import uvicorn
from src.main import app

server = uvicorn.run(
    app=app,
    host="127.0.0.1",
    port=8000,
    log_level="info",
    reload_dirs="./src/",
)
