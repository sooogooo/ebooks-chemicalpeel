# AI Assistant API 服务

电子书AI助手后端API服务，支持中国主流大模型。

## 功能特性

- 🤖 支持6个中国主流大模型
  - 通义千问 (阿里云)
  - 文心一言 (百度)
  - 讯飞星火
  - 智谱GLM
  - Kimi (月之暗面)
  - 豆包 (字节跳动)

- 🔄 流式和非流式响应
- 🛡️ 请求限流保护
- 🌐 CORS跨域支持
- 📝 统一的API接口

## 快速开始

### 1. 安装依赖

```bash
cd api
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的API密钥。

### 3. 启动服务

```bash
# 开发模式（自动重载）
python main.py

# 或使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

服务将在 http://localhost:8001 启动。

## API接口文档

### 1. 获取模型列表

```http
GET /api/models
```

**响应示例：**
```json
{
  "qwen": {
    "name": "通义千问",
    "models": ["qwen-turbo", "qwen-plus", "qwen-max"],
    "default": "qwen-turbo"
  },
  ...
}
```

### 2. 聊天接口

```http
POST /api/chat
```

**请求体：**
```json
{
  "model_type": "qwen",
  "api_key": "your_api_key",
  "messages": [
    {"role": "user", "content": "什么是刷酸？"}
  ],
  "config": {
    "model": "qwen-turbo",
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 2000
  },
  "stream": false
}
```

**响应示例（非流式）：**
```json
{
  "content": "刷酸是指...",
  "model": "qwen-turbo",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 50,
    "total_tokens": 60
  }
}
```

**流式响应：**
设置 `"stream": true` 时，返回 `text/event-stream` 格式：
```
data: 刷酸

data: 是指

data: [DONE]
```

### 3. 测试连接

```http
POST /api/test-connection
```

请求体格式同聊天接口，用于测试API密钥是否有效。

### 4. 健康检查

```http
GET /api/health
```

## 架构设计

### 目录结构

```
api/
├── adapters/           # 大模型适配器
│   ├── __init__.py
│   ├── base.py        # 基础适配器类
│   ├── qwen.py        # 通义千问
│   ├── ernie.py       # 文心一言
│   ├── spark.py       # 讯飞星火
│   ├── glm.py         # 智谱GLM
│   ├── kimi.py        # Kimi
│   └── doubao.py      # 豆包
├── main.py            # FastAPI主程序
├── config.py          # 配置管理
├── requirements.txt   # Python依赖
├── .env.example       # 环境变量模板
└── README.md          # 本文档
```

### 适配器模式

所有大模型适配器都继承自 `BaseAdapter`，实现统一接口：

```python
class BaseAdapter(ABC):
    @abstractmethod
    async def chat(self, messages, **kwargs):
        """同步聊天接口"""
        pass
    
    @abstractmethod
    async def stream_chat(self, messages, **kwargs):
        """流式聊天接口"""
        pass
```

### 添加新的大模型适配器

1. 在 `adapters/` 目录创建新的适配器文件
2. 继承 `BaseAdapter` 并实现必要方法
3. 在 `adapters/__init__.py` 中导入
4. 在 `config.py` 的 `MODEL_CONFIGS` 中添加配置
5. 在 `main.py` 的 `get_adapter()` 中添加映射

示例：

```python
# adapters/newmodel.py
from .base import BaseAdapter

class NewModelAdapter(BaseAdapter):
    def get_default_model(self):
        return "model-name"
    
    async def chat(self, messages, **kwargs):
        # 实现聊天逻辑
        pass
    
    async def stream_chat(self, messages, **kwargs):
        # 实现流式聊天逻辑
        pass
```

## 部署指南

### Docker部署

创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

构建和运行：

```bash
docker build -t ai-assistant-api .
docker run -p 8001:8001 --env-file .env ai-assistant-api
```

### 云服务部署

推荐使用以下平台：
- 阿里云函数计算
- 腾讯云云函数
- AWS Lambda (配合API Gateway)
- Vercel / Railway

## 安全建议

1. **API密钥保护**：不要在代码中硬编码API密钥
2. **请求限流**：默认每分钟60次请求，可在 `.env` 中调整
3. **CORS配置**：仅允许信任的源访问
4. **HTTPS**：生产环境使用HTTPS
5. **日志管理**：不要记录敏感信息

## 常见问题

### Q: 如何获取各个大模型的API密钥？

- **通义千问**: https://dashscope.aliyun.com/
- **文心一言**: https://cloud.baidu.com/product/wenxinworkshop
- **讯飞星火**: https://xinghuo.xfyun.cn/
- **智谱GLM**: https://open.bigmodel.cn/
- **Kimi**: https://platform.moonshot.cn/
- **豆包**: https://www.volcengine.com/product/doubao

### Q: 为什么需要后端API服务？

虽然可以直接从前端调用大模型API，但使用后端代理有以下好处：
1. 保护API密钥不暴露在前端代码中
2. 统一接口，简化前端开发
3. 实现请求限流和安全控制
4. 添加缓存和日志功能

### Q: 可以同时使用多个大模型吗？

可以。前端可以选择不同的模型，API服务会自动路由到对应的适配器。

## 许可证

本项目与主电子书项目使用相同的许可证。
