import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import STATIC_APP_DIR, CORS_ORIGINS, LOG_DIR, LOG_FILE
from backend.api.resolve_or_generate import router as resolve_router
from backend.api.registry_ops import load_registry

# Ensure log dir
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=2_000_000, backupCount=2, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI(title="GeneralVisualization Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static mount for front-end pages under /app
if not os.path.isdir(STATIC_APP_DIR):
    raise RuntimeError(f"未找到前端目录: {STATIC_APP_DIR}")
app.mount("/app", StaticFiles(directory=STATIC_APP_DIR, html=True), name="app")

# Routers
app.include_router(resolve_router)


@app.get("/api/health")
def health() -> Dict[str, object]:
    return {"ok": True, "ts": __import__('time').time()}


@app.get("/api/preview")
def preview(url: str) -> Dict[str, object]:
    if not url or not url.startswith("app/"):
        raise HTTPException(status_code=400, detail="url 必须以 app/ 开头")
    file_path = os.path.join(os.path.dirname(STATIC_APP_DIR), url) if url.startswith("app/") else os.path.join(STATIC_APP_DIR, url)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    return {"ok": True, "url": url}


@app.get("/api/registry")
def get_registry_endpoint():
    # Expose full registry for convenience; filtered version exists in router
    return load_registry()