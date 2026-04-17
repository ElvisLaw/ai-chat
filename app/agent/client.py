"""Agent 客户端 - 实现 BaseLLMClient 接口。"""

import asyncio
from typing import Any, Iterator

from ..clients.base import BaseLLMClient
from .service import AgentService


class AgentClient(BaseLLMClient):
    """Agent 客户端，实现 BaseLLMClient 接口。"""

    def __init__(self, agent_service: AgentService, **kwargs: Any):
        """初始化 Agent 客户端。

        Args:
            agent_service: AgentService 实例。
            **kwargs: 其他参数（忽略）。
        """
        self._agent_service = agent_service

    def send_message(self, messages: list[dict[str, Any]], **kwargs: Any) -> str:
        """发送消息并获取回复。

        Args:
            messages: 消息列表。
            **kwargs: 其他参数。

        Returns:
            AI 回复文本。
        """
        # 提取最后一条用户消息
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        response, _ = self._agent_service.chat(user_message)
        return response

    def stream_message(self, messages: list[dict[str, Any]], **kwargs: Any) -> Iterator[str]:
        """流式发送消息。

        Args:
            messages: 消息列表。
            **kwargs: 其他参数。

        Returns:
            回复 token 生成器。
        """
        # 提取最后一条用户消息
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        generator, _ = self._agent_service.stream(user_message)
        return generator


def create_agent_client(
    api_key: str | None = None,
    model: str | None = None,
    base_url: str | None = None,
    **kwargs: Any,
) -> AgentClient:
    """创建 Agent 客户端。

    Args:
        api_key: API key。
        model: 模型名称。
        base_url: 可选的 API base URL（例如用于 MiniMax）。
        **kwargs: 其他参数。

    Returns:
        AgentClient 实例。
    """
    from langchain_openai import ChatOpenAI

    llm_kwargs: dict[str, Any] = {"model": model or "gpt-4"}
    if api_key:
        llm_kwargs["api_key"] = api_key
    if base_url:
        llm_kwargs["base_url"] = base_url

    llm = ChatOpenAI(**llm_kwargs)
    agent_service = AgentService(llm=llm)
    return AgentClient(agent_service=agent_service)
