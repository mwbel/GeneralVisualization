"""
下载历史管理服务
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

class DownloadHistoryService:
    """下载历史管理服务"""
    
    def __init__(self):
        self.history_file = Path("data/download_history.json")
        self.history_file.parent.mkdir(exist_ok=True)
        
    def _load_history(self) -> List[Dict[str, Any]]:
        """加载下载历史"""
        if not self.history_file.exists():
            return []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_history(self, history: List[Dict[str, Any]]) -> None:
        """保存下载历史"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def add_download_record(
        self,
        filename: str,
        code: str,
        dependencies: List[str],
        options: Dict[str, Any],
        file_size: int,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> str:
        """添加下载记录"""
        history = self._load_history()
        
        record = {
            "id": f"download_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(history)}",
            "filename": filename,
            "code_preview": code[:200] + "..." if len(code) > 200 else code,
            "dependencies": dependencies,
            "options": options,
            "file_size": file_size,
            "success": success,
            "error_message": error_message,
            "timestamp": datetime.now().isoformat(),
            "download_count": 1
        }
        
        history.insert(0, record)  # 最新的在前面
        
        # 保持最多100条记录
        if len(history) > 100:
            history = history[:100]
        
        self._save_history(history)
        return record["id"]
    
    def get_download_history(
        self,
        limit: int = 50,
        offset: int = 0,
        filter_success: Optional[bool] = None
    ) -> Dict[str, Any]:
        """获取下载历史"""
        history = self._load_history()
        
        # 过滤
        if filter_success is not None:
            history = [h for h in history if h["success"] == filter_success]
        
        # 分页
        total = len(history)
        history = history[offset:offset + limit]
        
        return {
            "records": history,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    
    def get_download_stats(self) -> Dict[str, Any]:
        """获取下载统计信息"""
        history = self._load_history()
        
        if not history:
            return {
                "total_downloads": 0,
                "successful_downloads": 0,
                "failed_downloads": 0,
                "success_rate": 0.0,
                "most_common_dependencies": [],
                "most_common_options": {},
                "average_file_size": 0,
                "recent_activity": []
            }
        
        total_downloads = len(history)
        successful_downloads = sum(1 for h in history if h["success"])
        failed_downloads = total_downloads - successful_downloads
        success_rate = (successful_downloads / total_downloads) * 100 if total_downloads > 0 else 0
        
        # 统计最常用的依赖
        dependency_count = {}
        for record in history:
            for dep in record.get("dependencies", []):
                dependency_count[dep] = dependency_count.get(dep, 0) + 1
        
        most_common_dependencies = sorted(
            dependency_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # 统计最常用的选项
        option_count = {}
        for record in history:
            for key, value in record.get("options", {}).items():
                if isinstance(value, bool) and value:
                    option_count[key] = option_count.get(key, 0) + 1
        
        # 平均文件大小
        file_sizes = [h.get("file_size", 0) for h in history if h.get("file_size")]
        average_file_size = sum(file_sizes) / len(file_sizes) if file_sizes else 0
        
        # 最近活动（最近7天）
        from datetime import datetime, timedelta
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_activity = []
        
        for record in history:
            try:
                record_time = datetime.fromisoformat(record["timestamp"])
                if record_time >= seven_days_ago:
                    recent_activity.append({
                        "date": record_time.strftime("%Y-%m-%d"),
                        "filename": record["filename"],
                        "success": record["success"]
                    })
            except (ValueError, KeyError):
                continue
        
        return {
            "total_downloads": total_downloads,
            "successful_downloads": successful_downloads,
            "failed_downloads": failed_downloads,
            "success_rate": round(success_rate, 2),
            "most_common_dependencies": most_common_dependencies,
            "most_common_options": option_count,
            "average_file_size": round(average_file_size, 2),
            "recent_activity": recent_activity[:20]  # 最近20条活动
        }
    
    def delete_download_record(self, record_id: str) -> bool:
        """删除下载记录"""
        history = self._load_history()
        original_length = len(history)
        
        history = [h for h in history if h["id"] != record_id]
        
        if len(history) < original_length:
            self._save_history(history)
            return True
        return False
    
    def clear_download_history(self) -> bool:
        """清空下载历史"""
        try:
            self._save_history([])
            return True
        except Exception:
            return False
    
    def get_download_record(self, record_id: str) -> Optional[Dict[str, Any]]:
        """获取特定的下载记录"""
        history = self._load_history()
        for record in history:
            if record["id"] == record_id:
                return record
        return None
    
    def update_download_count(self, record_id: str) -> bool:
        """更新下载次数"""
        history = self._load_history()
        
        for record in history:
            if record["id"] == record_id:
                record["download_count"] = record.get("download_count", 0) + 1
                record["last_downloaded"] = datetime.now().isoformat()
                self._save_history(history)
                return True
        return False

# 创建全局实例
download_history_service = DownloadHistoryService()