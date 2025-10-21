from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.endpoints.visualmind_generate import router as visualmind_router

app = FastAPI()

# 允许前端直接调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# 挂载新端点：最终路径 /api/v1/generate
app.include_router(visualmind_router, prefix="/api/v1", tags=["visualmind"])

# 健康检查（可选）
@app.get("/healthz")
def healthz():
    return {"ok": True}
