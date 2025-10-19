"""
FastAPI Main Application
AI助手后端API服务主程序
"""

import time
from typing import Dict, List, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict

from config import settings, MODEL_CONFIGS
from adapters import (
    QwenAdapter,
    ErnieAdapter,
    GLMAdapter,
    SparkAdapter,
    KimiAdapter,
    DoubaoAdapter
)

# 创建FastAPI应用
app = FastAPI(
    title="AI Assistant API",
    description="电子书AI助手API服务，支持多个中国主流大模型",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求限流存储（简单实现）
request_tracker: Dict[str, List[float]] = {}


# 请求模型
class ChatRequest(BaseModel):
    """聊天请求模型"""
    model_config = ConfigDict(protected_namespaces=())
    
    model_type: str  # qwen, ernie, glm, spark, kimi, doubao
    api_key: str
    messages: List[Dict[str, str]]
    config: Dict[str, Any] = {}
    stream: bool = False


class ChatResponse(BaseModel):
    """聊天响应模型"""
    content: str
    model: str
    usage: Dict[str, Any] = {}


# 中间件：请求限流
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """简单的请求限流中间件"""
    client_ip = request.client.host
    current_time = time.time()
    
    # 清理过期记录
    if client_ip in request_tracker:
        request_tracker[client_ip] = [
            t for t in request_tracker[client_ip]
            if current_time - t < 60
        ]
    else:
        request_tracker[client_ip] = []
    
    # 检查限流
    if len(request_tracker[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=429,
            detail="请求过于频繁，请稍后再试"
        )
    
    # 记录请求
    request_tracker[client_ip].append(current_time)
    
    response = await call_next(request)
    return response


def get_adapter(model_type: str, api_key: str, config: Dict[str, Any]):
    """根据模型类型获取对应的适配器"""
    adapters = {
        "qwen": QwenAdapter,
        "ernie": ErnieAdapter,
        "glm": GLMAdapter,
        "spark": SparkAdapter,
        "kimi": KimiAdapter,
        "doubao": DoubaoAdapter
    }
    
    adapter_class = adapters.get(model_type)
    if not adapter_class:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的模型类型: {model_type}"
        )
    
    return adapter_class(api_key, config)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI Assistant API",
        "version": "1.0.0",
        "supported_models": list(MODEL_CONFIGS.keys())
    }


@app.get("/api/models")
async def list_models():
    """获取支持的模型列表"""
    return MODEL_CONFIGS


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """聊天接口"""
    try:
        # 获取适配器
        adapter = get_adapter(request.model_type, request.api_key, request.config)
        
        # 流式响应
        if request.stream:
            async def generate():
                try:
                    async for chunk in adapter.stream_chat(request.messages):
                        yield f"data: {chunk}\n\n"
                    yield "data: [DONE]\n\n"
                except Exception as e:
                    # 记录详细错误但不暴露给用户
                    print(f"[ERROR] Stream chat error: {type(e).__name__}: {str(e)}")
                    yield "data: [ERROR: 生成回复时发生错误]\n\n"
            
            return StreamingResponse(
                generate(),
                media_type="text/event-stream"
            )
        
        # 非流式响应
        result = await adapter.chat(request.messages)
        return ChatResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 记录详细错误到日志，但不暴露给用户
        print(f"[ERROR] Chat API error: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail="服务器内部错误，请稍后重试")


@app.post("/api/test-connection")
async def test_connection(request: ChatRequest):
    """测试连接"""
    try:
        adapter = get_adapter(request.model_type, request.api_key, request.config)
        
        # 发送简单的测试消息
        test_messages = [
            {"role": "user", "content": "你好"}
        ]
        
        result = await adapter.chat(test_messages)
        return {
            "status": "success",
            "message": "连接成功",
            "model": result.get("model", "unknown")
        }
        
    except Exception as e:
        # 记录详细错误到日志，但不暴露给用户
        print(f"[ERROR] Connection test error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="连接测试失败，请检查API密钥和网络连接"
        )


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": time.time()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
