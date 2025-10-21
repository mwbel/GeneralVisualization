from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from services.visualmind_service import VisualMindService

router = APIRouter()
service = VisualMindService()

@router.post("/generate")
async def generate(payload: Dict[str, Any]):
    """VisualMind风格的生成端点，返回 {status, html, code, kind}"""
    try:
        prompt = str(payload.get("prompt", "")).strip()
        if not prompt:
            raise HTTPException(status_code=400, detail="prompt 不能为空")
        return service.generate(prompt)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))