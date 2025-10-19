"""
Doubao (豆包) Adapter
字节跳动豆包大模型适配器
"""

import json
import httpx
from typing import Dict, List, Any, AsyncGenerator
from .base import BaseAdapter


class DoubaoAdapter(BaseAdapter):
    """豆包适配器"""
    
    API_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    
    def get_default_model(self) -> str:
        return "doubao-lite-4k"
    
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
            "messages": messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "stream": False
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
                "content": result["choices"][0]["message"]["content"],
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
        }
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "stream": True
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
                    if line.startswith('data: '):
                        try:
                            data_str = line[6:].strip()
                            if data_str and data_str != '[DONE]':
                                data = json.loads(data_str)
                                if 'choices' in data and len(data['choices']) > 0:
                                    delta = data['choices'][0].get('delta', {})
                                    content = delta.get('content', '')
                                    if content:
                                        yield content
                        except json.JSONDecodeError:
                            continue
