"""CLI LLM 客户端工厂。"""

from typing import Any, Callable

from ..clients import create_llm_client
from ..settings import Settings


def create_llm_client_factory(settings: Settings) -> Callable[[str], Any]:
    """创建 LLM 客户端工厂函数。

    Args:
        settings: 应用设置实例。

    Returns:
        工厂函数，接受 provider 名称返回 LLM 客户端实例。
    """

    def factory(provider: str) -> Any:
        if provider == "openai":
            return create_llm_client(
                "openai",
                settings.openai_api_key,
                base_url=settings.openai_base_url,
            )
        elif provider == "anthropic":
            return create_llm_client(
                "anthropic",
                settings.anthropic_api_key,
            )
        elif provider == "agent":
            return create_llm_client(
                "agent",
                settings.openai_api_key,
                model=settings.get_default_model("openai"),
                base_url=settings.openai_base_url,
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    return factory
