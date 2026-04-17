"""Agent 服务封装。"""

from typing import Any, Iterator

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from langgraph.prebuilt import create_react_agent

from .tools import calculator, get_datetime


class AgentService:
    """LangChain Agent 服务封装。"""

    def __init__(
        self,
        llm: Any,
        tools: list[Any] | None = None,
    ):
        """初始化 Agent 服务。

        Args:
            llm: LangChain 聊天模型实例。
            tools: 工具列表，默认为 [calculator, get_datetime]。
        """
        self._llm = llm
        self._tools = tools or [calculator, get_datetime]
        self._agent = create_react_agent(
            model=llm,
            tools=self._tools,
        )

    def chat(self, message: str, **kwargs: Any) -> tuple[str, str]:
        """处理聊天请求。

        Args:
            message: 用户消息。
            **kwargs: 其他参数。

        Returns:
            tuple[str, str]: (AI 回复, conversation_id 对于 Agent 模式为固定值)
        """
        result = self._agent.invoke(
            {"messages": [HumanMessage(content=message)]},
            **kwargs,
        )

        # 从结果中提取最终响应
        response = ""
        for msg in result.get("messages", []):
            if isinstance(msg, AIMessage) and msg.content:
                response = msg.content

        return response, "agent"

    def stream(self, message: str, **kwargs: Any) -> tuple[Iterator[str], str]:
        """处理流式聊天请求。

        Args:
            message: 用户消息。
            **kwargs: 其他参数。

        Returns:
            tuple[Iterator[str], str]: (响应流, conversation_id)
        """

        def generate() -> Iterator[str]:
            for event in self._agent.stream(
                {"messages": [HumanMessage(content=message)]},
                **kwargs,
            ):
                # 提取消息内容
                if "messages" in event:
                    for msg in event["messages"]:
                        if hasattr(msg, "content") and msg.content:
                            yield msg.content

        return generate(), "agent"
