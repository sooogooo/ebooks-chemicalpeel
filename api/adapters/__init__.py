"""
LLM Adapters Package
支持多个中国主流大模型的适配器
"""

from .base import BaseAdapter
from .qwen import QwenAdapter
from .ernie import ErnieAdapter
from .glm import GLMAdapter
from .spark import SparkAdapter
from .kimi import KimiAdapter
from .doubao import DoubaoAdapter

__all__ = [
    'BaseAdapter',
    'QwenAdapter',
    'ErnieAdapter',
    'GLMAdapter',
    'SparkAdapter',
    'KimiAdapter',
    'DoubaoAdapter',
]
