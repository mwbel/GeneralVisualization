"""
下载历史管理API端点
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ...services.download_history_service import download_history_service

router = APIRouter()

@router.get("/history")
async def get_download_history(
    limit: int = Query(50, ge=1, le=100, description="返回记录数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    filter_success: Optional[bool] = Query(None, description="过滤成功/失败的下载")
):
    """获取下载历史"""
    try:
        result = download_history_service.get_download_history(
            limit=limit,
            offset=offset,
            filter_success=filter_success
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取下载历史失败: {str(e)}")

@router.get("/history/stats")
async def get_download_stats():
    """获取下载统计信息"""
    try:
        stats = download_history_service.get_download_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取下载统计失败: {str(e)}")

@router.get("/history/{record_id}")
async def get_download_record(record_id: str):
    """获取特定的下载记录"""
    try:
        record = download_history_service.get_download_record(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="下载记录不存在")
        return record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取下载记录失败: {str(e)}")

@router.delete("/history/{record_id}")
async def delete_download_record(record_id: str):
    """删除下载记录"""
    try:
        success = download_history_service.delete_download_record(record_id)
        if not success:
            raise HTTPException(status_code=404, detail="下载记录不存在")
        return {"message": "下载记录已删除"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除下载记录失败: {str(e)}")

@router.delete("/history")
async def clear_download_history():
    """清空下载历史"""
    try:
        success = download_history_service.clear_download_history()
        if not success:
            raise HTTPException(status_code=500, detail="清空下载历史失败")
        return {"message": "下载历史已清空"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清空下载历史失败: {str(e)}")

@router.post("/history/{record_id}/download")
async def update_download_count(record_id: str):
    """更新下载次数（当用户重新下载时调用）"""
    try:
        success = download_history_service.update_download_count(record_id)
        if not success:
            raise HTTPException(status_code=404, detail="下载记录不存在")
        return {"message": "下载次数已更新"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新下载次数失败: {str(e)}")