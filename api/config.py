"""
API Configuration
API服务配置管理
"""

import os
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Settings(BaseModel):
    """API服务配置"""
    
    # 服务配置
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8001"))
    
    # CORS配置
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:8000,https://sooogooo.github.io"
    ).split(",")
    
    # 大模型API配置（可选）
    QWEN_API_KEY: str = os.getenv("QWEN_API_KEY", "")
    ERNIE_API_KEY: str = os.getenv("ERNIE_API_KEY", "")
    ERNIE_SECRET_KEY: str = os.getenv("ERNIE_SECRET_KEY", "")
    SPARK_API_KEY: str = os.getenv("SPARK_API_KEY", "")
    GLM_API_KEY: str = os.getenv("GLM_API_KEY", "")
    KIMI_API_KEY: str = os.getenv("KIMI_API_KEY", "")
    DOUBAO_API_KEY: str = os.getenv("DOUBAO_API_KEY", "")
    
    # 请求限流配置
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    class Config:
        env_file = ".env"


# 全局配置实例
settings = Settings()


# 模型配置映射
MODEL_CONFIGS = {
    "qwen": {
        "name": "通义千问",
        "models": ["qwen-turbo", "qwen-plus", "qwen-max"],
        "default": "qwen-turbo"
    },
    "ernie": {
        "name": "文心一言",
        "models": ["ernie-bot", "ernie-bot-turbo", "ernie-bot-4"],
        "default": "ernie-bot-turbo"
    },
    "glm": {
        "name": "智谱GLM",
        "models": ["glm-4", "glm-4-flash", "glm-3-turbo"],
        "default": "glm-4"
    },
    "spark": {
        "name": "讯飞星火",
        "models": ["spark-lite", "spark-pro", "spark-max"],
        "default": "spark-lite"
    },
    "kimi": {
        "name": "Kimi",
        "models": ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"],
        "default": "moonshot-v1-8k"
    },
    "doubao": {
        "name": "豆包",
        "models": ["doubao-lite-4k", "doubao-pro-4k", "doubao-pro-32k"],
        "default": "doubao-lite-4k"
    }
}
