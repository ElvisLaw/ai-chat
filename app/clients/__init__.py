"""LLM 客户端模块。

提供统一的接口来调用 OpenAI GPT 和 Anthropic Claude 模型。
"""

from .anthropic_client import AnthropicClient
from .base import BaseLLMClient, ConfigurationError, LLMError
from .factory import create_anthropic_client, create_llm_client, create_openai_client
from .openai_client import OpenAIClient

__all__ = [
    "BaseLLMClient",       # LLM 客户端抽象基类
    "LLMError",           # LLM 客户端错误基类
    "ConfigurationError",  # 配置错误（API Key 缺失等）
    "OpenAIClient",       # OpenAI GPT 客户端实现
    "AnthropicClient",    # Anthropic Claude 客户端实现
    "create_llm_client",         # 创建 LLM 客户端的工厂函数
    "create_openai_client",      # 创建 OpenAI 客户端的便捷函数
    "create_anthropic_client",   # 创建 Anthropic 客户端的便捷函数
]
