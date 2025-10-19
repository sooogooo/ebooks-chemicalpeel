"""
Ernie (文心一言) Adapter
百度文心一言大模型适配器
"""

import json
import httpx
from typing import Dict, List, Any, AsyncGenerator
from .base import BaseAdapter


class ErnieAdapter(BaseAdapter):
    """文心一言适配器"""
    
    TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
    API_BASE_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat"
    
    def __init__(self, api_key: str, config: Dict[str, Any] = None):
        super().__init__(api_key, config)
        # 文心一言使用 API Key 和 Secret Key
        self.api_key = api_key
        self.secret_key = config.get('secret_key', '') if config else ''
        self.access_token = None
    
    def get_default_model(self) -> str:
        return "ernie-bot-turbo"
    
    async def get_access_token(self) -> str:
        """获取access_token"""
        if self.access_token:
            return self.access_token
        
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(self.TOKEN_URL, params=params)
            response.raise_for_status()
            result = response.json()
            self.access_token = result.get("access_token")
            return self.access_token
    
    def get_model_endpoint(self) -> str:
        """获取模型端点"""
        model_endpoints = {
            "ernie-bot": "completions",
            "ernie-bot-turbo": "eb-instant",
            "ernie-bot-4": "completions_pro",
        }
        return model_endpoints.get(self.model_name, "eb-instant")
    
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """同步聊天接口"""
        if not self.validate_messages(messages):
            raise ValueError("Invalid messages format")
        
        access_token = await self.get_access_token()
        endpoint = self.get_model_endpoint()
        url = f"{self.API_BASE_URL}/{endpoint}?access_token={access_token}"
        
        payload = {
            "messages": messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_output_tokens": self.max_tokens
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            
            return {
                "content": result.get("result", ""),
                "model": self.model_name,
                "usage": result.get("usage", {})
            }
    
    async def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        """流式聊天接口"""
        if not self.validate_messages(messages):
            raise ValueError("Invalid messages format")
        
        access_token = await self.get_access_token()
        endpoint = self.get_model_endpoint()
        url = f"{self.API_BASE_URL}/{endpoint}?access_token={access_token}"
        
        payload = {
            "messages": messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_output_tokens": self.max_tokens,
            "stream": True
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream('POST', url, json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith('data: '):
                        try:
                            data_str = line[6:].strip()
                            if data_str:
                                data = json.loads(data_str)
                                if 'result' in data:
                                    content = data['result']
                                    if content:
                                        yield content
                        except json.JSONDecodeError:
                            continue
