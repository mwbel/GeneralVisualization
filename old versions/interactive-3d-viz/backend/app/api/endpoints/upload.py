"""
文件上传API端点
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
import pandas as pd
from typing import Dict, Any
from ...core.config import settings

router = APIRouter()

@router.post("/", response_model=Dict[str, Any])
async def upload_file(file: UploadFile = File(...)):
    """
    上传文件并返回文件信息
    """
    try:
        # 检查文件类型
        allowed_extensions = {'.csv', '.json', '.xlsx', '.txt'}
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件类型。支持的类型: {', '.join(allowed_extensions)}"
            )
        
        # 生成唯一文件名
        file_id = str(uuid.uuid4())
        filename = f"{file_id}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        # 确保上传目录存在
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # 保存文件
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 分析文件内容
        file_info = {
            "file_id": file_id,
            "filename": file.filename,
            "size": len(content),
            "type": file_extension,
            "path": file_path
        }
        
        # 如果是CSV文件，尝试读取并分析结构
        if file_extension == '.csv':
            try:
                df = pd.read_csv(file_path)
                file_info.update({
                    "rows": len(df),
                    "columns": list(df.columns),
                    "column_count": len(df.columns),
                    "preview": df.head(5).to_dict('records')
                })
            except Exception as e:
                file_info["analysis_error"] = str(e)
        
        return {
            "success": True,
            "message": "文件上传成功",
            "file_info": file_info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@router.get("/{file_id}")
async def get_file_info(file_id: str):
    """
    获取已上传文件的信息
    """
    # 查找文件
    for ext in ['.csv', '.json', '.xlsx', '.txt']:
        file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
        if os.path.exists(file_path):
            file_stats = os.stat(file_path)
            return {
                "file_id": file_id,
                "path": file_path,
                "size": file_stats.st_size,
                "type": ext,
                "exists": True
            }
    
    raise HTTPException(status_code=404, detail="文件未找到")

@router.delete("/{file_id}")
async def delete_file(file_id: str):
    """
    删除已上传的文件
    """
    deleted = False
    for ext in ['.csv', '.json', '.xlsx', '.txt']:
        file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
        if os.path.exists(file_path):
            os.remove(file_path)
            deleted = True
            break
    
    if not deleted:
        raise HTTPException(status_code=404, detail="文件未找到")
    
    return {"success": True, "message": "文件删除成功"}