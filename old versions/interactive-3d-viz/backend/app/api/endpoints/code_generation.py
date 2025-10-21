"""
AI代码生成API端点
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from typing import List, Dict, Any

from ...models.visualization import (
    CodeGenerationRequest,
    CodeGenerationResponse,
    VisualizationType
)
from ...services.ai_service import AICodeGenerationService
from ...services.download_service import DownloadService
from ...services.template_service import template_service

router = APIRouter()

# Initialize services
ai_service = AICodeGenerationService()
download_service = DownloadService()

@router.post("/generate", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    """Generate Python code based on natural language prompt"""
    try:
        response = await ai_service.generate_code(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/download")
async def download_code(request: dict):
    """Download generated code as a ZIP file with configurable options"""
    try:
        code = request.get("code", "")
        dependencies = request.get("dependencies", [])
        filename = request.get("filename", "visualization")
        
        # Extract download options
        options = request.get("options", {})
        
        # Create package with enhanced options
        zip_path = await download_service.create_code_package(
            code=code,
            dependencies=dependencies,
            filename=filename,
            include_requirements=options.get("include_requirements", True),
            include_readme=options.get("include_readme", True),
            include_sample_data=options.get("include_sample_data", False),
            include_setup_script=options.get("include_setup_script", True),
            include_docker=options.get("include_docker", False),
            include_jupyter_notebook=options.get("include_jupyter_notebook", False),
            python_version=options.get("python_version", "3.8"),
            package_format=options.get("package_format", "zip")
        )
        
        # Return file response
        return FileResponse(
            path=zip_path,
            filename=f"{filename}.zip",
            media_type="application/zip"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{filename}")
async def get_download_file(filename: str):
    """Get a previously created download file"""
    try:
        file_path = await download_service.get_download_file(filename)
        if not file_path:
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/zip"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/downloads/history")
async def get_download_history():
    """Get download history"""
    try:
        history = await download_service.get_download_history()
        return {"downloads": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def get_code_templates():
    """Get available code templates"""
    try:
        templates = await ai_service.get_available_templates()
        return {"templates": templates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates/categories")
async def get_template_categories():
    """Get available template categories"""
    try:
        categories = template_service.get_categories()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates/category/{category}")
async def get_templates_by_category(category: str):
    """Get templates by category"""
    try:
        templates = template_service.get_templates_by_category(category)
        return {"templates": templates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates/search")
async def search_templates(
    q: str = "", 
    category: str = "", 
    difficulty: str = "",
    page: int = 1,
    page_size: int = 12
):
    """Search templates by query, category, or difficulty with pagination"""
    try:
        result = template_service.search_templates(
            query=q if q else None,
            category=category if category else None,
            difficulty=difficulty if difficulty else None,
            page=page,
            page_size=page_size
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates/{template_id}")
async def get_template_by_id(template_id: str):
    """Get a specific template by ID"""
    try:
        template = template_service.get_template_by_id(template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        return {"template": template}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/templates/{template_id}/customize")
async def customize_template(template_id: str, customization: dict):
    """Customize a template with user parameters"""
    try:
        customized_code = template_service.customize_template(template_id, customization)
        if not customized_code:
            raise HTTPException(status_code=404, detail="Template not found")
        return {"code": customized_code}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))