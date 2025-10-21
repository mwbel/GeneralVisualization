"""
应用配置设置
"""

import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """应用配置类"""
    
    # 基础配置
    APP_NAME: str = "Interactive 3D Visualization API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS配置
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # OpenAI配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4"
    
    # Claude配置
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY", "")
    
    # 文件存储配置
    UPLOAD_DIR: str = "uploads"
    STATIC_DIR: str = "static"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # 代码执行配置
    CODE_EXECUTION_TIMEOUT: int = 30  # 秒
    MAX_CODE_LENGTH: int = 10000  # 字符
    
    # 安全配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建全局设置实例
settings = Settings()