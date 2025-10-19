"""
Base Adapter Class
所有大模型适配器的基类
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, AsyncGenerator


class BaseAdapter(ABC):
    """大模型适配器基类"""
    
    def __init__(self, api_key: str, config: Dict[str, Any] = None):
        """
        初始化适配器
        
        Args:
            api_key: API密钥
            config: 额外配置参数
        """
        self.api_key = api_key
        self.config = config or {}
        self.model_name = self.config.get('model', self.get_default_model())
        self.temperature = self.config.get('temperature', 0.7)
        self.top_p = self.config.get('top_p', 0.9)
        self.max_tokens = self.config.get('max_tokens', 2000)
    
    @abstractmethod
    def get_default_model(self) -> str:
        """获取默认模型名称"""
        pass
    
    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        同步聊天接口
        
        Args:
            messages: 消息列表，格式为 [{"role": "user/assistant/system", "content": "..."}]
            **kwargs: 其他参数
            
        Returns:
            包含回复内容的字典
        """
        pass
    
    @abstractmethod
    async def stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        """
        流式聊天接口
        
        Args:
            messages: 消息列表
            **kwargs: 其他参数
            
        Yields:
            流式返回的文本片段
        """
        pass
    
    def validate_messages(self, messages: List[Dict[str, str]]) -> bool:
        """
        验证消息格式
        
        Args:
            messages: 消息列表
            
        Returns:
            是否有效
        """
        if not messages or not isinstance(messages, list):
            return False
        
        for msg in messages:
            if not isinstance(msg, dict):
                return False
            if 'role' not in msg or 'content' not in msg:
                return False
            if msg['role'] not in ['user', 'assistant', 'system']:
                return False
        
        return True
    
    def build_headers(self) -> Dict[str, str]:
        """构建请求头"""
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
