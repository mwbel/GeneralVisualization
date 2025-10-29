from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# 这里按你的目录导入新端点（使用绝对包路径）
from backend.app.api.endpoints.visualmind_generate import router as visualmind_router
from backend.app.api.resolve_or_generate import router as ai_visualizer_router

app = FastAPI()

# 允许前端直接调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# 挂载静态目录，供浏览器直接访问现有与生成页面
app.mount("/app", StaticFiles(directory="app", html=True), name="app")

# 挂载端点
app.include_router(visualmind_router, prefix="/api/v1", tags=["visualmind"])  # 旧端点
app.include_router(ai_visualizer_router, prefix="/api", tags=["ai_visualizer"])  # 新端点：/api/resolve_or_generate

@app.get("/healthz")
def healthz():
    return {"ok": True}
