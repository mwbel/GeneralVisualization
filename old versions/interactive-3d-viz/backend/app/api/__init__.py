"""
API路由模块
"""

from fastapi import APIRouter

# 创建主路由器
router = APIRouter()

# 导入各个子路由
from .endpoints import visualization, code_generation, health, upload, download_history

# 注册子路由
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(visualization.router, prefix="/visualization", tags=["visualization"])
router.include_router(code_generation.router, prefix="/code", tags=["code-generation"])
router.include_router(upload.router, prefix="/upload", tags=["upload"])
router.include_router(download_history.router, prefix="/download", tags=["download-history"])