"""聊天服务模块。"""

from typing import Callable, Iterator, Any

from .models import Role, Conversation
from .store import ConversationStore


class ChatService:
    """聊天服务主类，封装对话逻辑和 LLM 调用。"""

    MAX_MESSAGES_PER_CONVERSATION = 100

    def __init__(
        self,
        store: ConversationStore,
        llm_client_factory: Callable[[str], Any],
    ):
        """初始化聊天服务。

        Args:
            store: 会话存储实例。
            llm_client_factory: LLM 客户端工厂函数，接受 provider 返回客户端。
        """
        self._store = store
        self._llm_client_factory = llm_client_factory

    def chat(
        self,
        message: str,
        provider: str = "openai",
        conversation_id: str | None = None,
        system_prompt: str | None = None,
        model: str | None = None,
    ) -> tuple[str, str]:
        """处理聊天请求（同步模式）。

        Args:
            message: 用户消息。
            provider: LLM 提供商。
            conversation_id: 会话 ID（None 表示新会话）。
            system_prompt: 系统提示词。
            model: 模型名称。

        Returns:
            tuple[str, str]: (AI 回复, conversation_id)
        """
        # 获取或创建会话
        if conversation_id:
            conv = self._store.get(conversation_id)
            if conv is None:
                conv = self._store.create()
        else:
            conv = self._store.create()

        # 添加用户消息
        conv.add_message(Role.user, message)

        # 检查消息数量限制
        if len(conv.messages) > self.MAX_MESSAGES_PER_CONVERSATION:
            raise ValueError(
                f"会话消息数量超过限制 ({self.MAX_MESSAGES_PER_CONVERSATION})"
            )

        # 获取 LLM 客户端
        client = self._llm_client_factory(provider)

        # 如果没有指定模型，使用默认模型
        if model is None:
            from ai_chat.settings import Settings
            model = Settings().model

        messages_for_llm = conv.get_messages_for_llm(system_prompt)

        response = client.send_message(
            message=message,
            system_prompt=system_prompt,
            model=model,
            conversation_messages=messages_for_llm if len(conv.messages) > 1 else None,
        )

        # 添加助手回复
        conv.add_message(Role.assistant, response)
        self._store.save(conv)

        return response, conv.id

    def stream(
        self,
        message: str,
        provider: str = "openai",
        conversation_id: str | None = None,
        system_prompt: str | None = None,
        model: str | None = None,
    ) -> tuple[Iterator[str], str]:
        """处理流式聊天请求。

        Args:
            message: 用户消息。
            provider: LLM 提供商。
            conversation_id: 会话 ID（None 表示新会话）。
            system_prompt: 系统提示词。
            model: 模型名称。

        Returns:
            tuple[Iterator[str], str]: (响应流, conversation_id)
        """
        # 获取或创建会话
        if conversation_id:
            conv = self._store.get(conversation_id)
            if conv is None:
                conv = self._store.create()
        else:
            conv = self._store.create()

        # 添加用户消息
        conv.add_message(Role.user, message)

        # 检查消息数量限制
        if len(conv.messages) > self.MAX_MESSAGES_PER_CONVERSATION:
            raise ValueError(
                f"会话消息数量超过限制 ({self.MAX_MESSAGES_PER_CONVERSATION})"
            )

        # 调用 LLM
        client = self._llm_client_factory(provider)
        messages_for_llm = conv.get_messages_for_llm(system_prompt)

        def generate() -> Iterator[str]:
            full_response = ""
            for chunk in client.stream_message(
                message=message,
                system_prompt=system_prompt,
                model=model,
                conversation_messages=messages_for_llm if len(conv.messages) > 1 else None,
            ):
                full_response += chunk
                yield chunk

            # 保存助手回复
            conv.add_message(Role.assistant, full_response)
            self._store.save(conv)

        return generate(), conv.id
