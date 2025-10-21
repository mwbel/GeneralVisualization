"""
3D可视化API端点
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime

from ...models.visualization import (
    VisualizationRequest,
    VisualizationResponse,
    VisualizationExample,
    VisualizationType,
    HTMLGenerationRequest,
    HTMLGenerationResponse
)
from ...services.visualization_service import VisualizationService

router = APIRouter()

# Initialize visualization service
visualization_service = VisualizationService()

@router.post("/generate", response_model=VisualizationResponse)
async def generate_visualization(request: VisualizationRequest):
    """Generate 3D visualization"""
    try:
        response = await visualization_service.generate_visualization(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/examples", response_model=List[VisualizationExample])
async def get_visualization_examples():
    """Get visualization examples"""
    try:
        examples = await visualization_service.get_examples()
        return examples
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-html", response_model=HTMLGenerationResponse)
async def generate_html_visualization(request: HTMLGenerationRequest):
    """Generate complete HTML visualization page from natural language prompt"""
    try:
        response = await visualization_service.generate_html_visualization(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))