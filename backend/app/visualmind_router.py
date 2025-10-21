from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from .services.visualmind_service import VisualMindService

router = APIRouter()
service = VisualMindService()

@router.post("/generate")
async def visualmind_generate(payload: Dict[str, Any]):
    """统一的可视化生成端点，返回 {status, html, code, kind}"""
    try:
        prompt = str(payload.get("prompt", "")).strip()
        if not prompt:
            raise HTTPException(status_code=400, detail="prompt 不能为空")
        result = service.generate(prompt)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))