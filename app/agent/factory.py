"""Agent 工厂函数。"""

from typing import Any

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from .tools import calculator, get_datetime


def create_langchain_agent(model_name: str = "gpt-4", **model_kwargs: Any):
    """创建 LangChain Agent。

    Args:
        model_name: 模型名称，格式为 "provider:model"。
        **model_kwargs: 传递给模型的额外参数。

    Returns:
        配置好的 Agent 执行器。
    """
    # 使用 ChatOpenAI
    llm = ChatOpenAI(model=model_name, **model_kwargs)

    # 获取工具
    tools = [calculator, get_datetime]

    # 创建 agent
    agent = create_agent(
        model=llm,
        tools=tools,
    )

    return agent


def create_agent_with_settings(settings: Any):
    """使用 Settings 创建 Agent。

    Args:
        settings: 应用 Settings 实例。

    Returns:
        配置好的 Agent。
    """
    model_name = settings.model or "gpt-4"
    return create_langchain_agent(model_name=model_name)
