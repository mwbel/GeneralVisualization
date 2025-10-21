"""
健康检查API端点
"""

from fastapi import APIRouter
from datetime import datetime
from app.core.config import settings

router = APIRouter()

@router.get("/")
async def health_check():
    """基础健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
        "service": settings.APP_NAME
    }

@router.get("/detailed")
async def detailed_health_check():
    """详细健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
        "service": settings.APP_NAME,
        "environment": {
            "debug": settings.DEBUG,
            "host": settings.HOST,
            "port": settings.PORT
        },
        "features": {
            "openai_configured": bool(settings.OPENAI_API_KEY),
            "claude_configured": bool(settings.CLAUDE_API_KEY)
        }
    }