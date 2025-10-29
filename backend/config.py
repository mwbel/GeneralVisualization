import os
from typing import List, Set

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Static mount for front-end pages
STATIC_APP_DIR = os.path.join(PROJECT_ROOT, "app")

# Registry path
REGISTRY_PATH = os.path.join(BASE_DIR, "registry", "registry.json")

# Generated output directory (relative to app)
GENERATED_DIR = os.path.join(PROJECT_ROOT, "app", "modules", "ai_visualizer", "generated")

# Logging
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Allowed spec values
ALLOWED_CHARTS: Set[str] = {"pdf", "cdf", "hist", "line", "scatter", "surface3d"}
ALLOWED_LIBS: Set[str] = {"plotly", "threejs"}

# CORS origins for local dev
CORS_ORIGINS: List[str] = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://127.0.0.1:8001",
    "http://localhost:8001",
]

# Model config placeholders
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
MODEL_TEMPERATURE = float(os.environ.get("MODEL_TEMPERATURE", "0.2"))