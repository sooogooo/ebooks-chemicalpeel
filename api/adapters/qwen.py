"""
Qwen (通义千问) Adapter
阿里云通义千问大模型适配器
"""

import json
import httpx
from typing import Dict, List, Any, AsyncGenerator
from .base import BaseAdapter


class QwenAdapter(BaseAdapter):
    """通义千问适配器"""
    
    API_BASE_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    
    def get_default_model(self) -> str:
        return "qwen-turbo"
    
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """同步聊天接口"""
        if not self.validate_messages(messages):
            raise ValueError("Invalid messages format")
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        
        payload = {
            "model": self.model_name,
            "input": {
                "messages": messages
            },
            "parameters": {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "max_tokens": self.max_tokens,
                "result_format": "message"
            }
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.API_BASE_URL,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            return {
                "content": result["output"]["choices"][0]["message"]["content"],
                "model": self.model_name,
                "usage": result.get("usage", {})
            }
    
    async def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        """流式聊天接口"""
        if not self.validate_messages(messages):
            raise ValueError("Invalid messages format")
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'X-DashScope-SSE': 'enable'
        }
        
        payload = {
            "model": self.model_name,
            "input": {
                "messages": messages
            },
            "parameters": {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "max_tokens": self.max_tokens,
                "result_format": "message",
                "incremental_output": True
            }
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                'POST',
                self.API_BASE_URL,
                headers=headers,
                json=payload
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith('data:'):
                        try:
                            data_str = line[5:].strip()
                            if data_str:
                                data = json.loads(data_str)
                                if 'output' in data and 'choices' in data['output']:
                                    choice = data['output']['choices'][0]
                                    if 'message' in choice and 'content' in choice['message']:
                                        content = choice['message']['content']
                                        if content:
                                            yield content
                        except json.JSONDecodeError:
                            continue
