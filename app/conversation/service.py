"""聊天服务模块。"""

import asyncio
import logging
from typing import Any, Callable, Iterator

from .memory import ConversationBuffer, MemorySummarizer
from .models import Role, Conversation
from .store import ConversationStore
from ..settings import get_settings


logger = logging.getLogger(__name__)


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
        self._buffer = ConversationBuffer()
        self._summarizer = MemorySummarizer(llm_client_factory)

    def _maybe_summarize(self, conversation: Conversation, provider: str) -> None:
        """检查并执行摘要。

        Args:
            conversation: 会话对象。
            provider: LLM 提供商。
        """
        if self._summarizer.should_summarize(conversation):
            try:
                self._summarizer.summarize(conversation, provider)
                logger.info(f"Conversation {conversation.id} summarized")
            except Exception as e:
                logger.error(f"Failed to summarize conversation {conversation.id}: {e}")

    async def chat(
        self,
        message: str,
        provider: str = "openai",
        conversation_id: str | None = None,
        system_prompt: str | None = None,
        model: str | None = None,
    ) -> tuple[str, str]:
        """处理聊天请求（异步模式，通过线程池执行同步 SDK）。

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

        # 消息缓冲管理
        self._buffer.buffer_messages(conv)

        # 检查消息数量限制
        if len(conv.messages) > self.MAX_MESSAGES_PER_CONVERSATION:
            raise ValueError(
                f"会话消息数量超过限制 ({self.MAX_MESSAGES_PER_CONVERSATION})"
            )

        # 获取 LLM 客户端
        client = self._llm_client_factory(provider)

        # 如果没有指定模型，使用 provider 的默认模型
        if model is None:
            model = get_settings().get_default_model(provider)

        messages_for_llm = conv.get_messages_for_llm(system_prompt)

        response = await asyncio.to_thread(
            client.send_message,
            messages=messages_for_llm,
            model=model,
        )

        # 添加助手回复
        conv.add_message(Role.assistant, response)

        # 持久化保存
        self._store.save(conv)

        # 检查是否需要摘要（摘要可能修改 messages）
        self._maybe_summarize(conv, provider)

        # 如果生成了摘要，再次保存
        if conv.is_summarized:
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
        """处理流式聊天请求（在线程池执行同步 SDK，不阻塞事件循环）。

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

        # 消息缓冲管理
        self._buffer.buffer_messages(conv)

        # 检查消息数量限制
        if len(conv.messages) > self.MAX_MESSAGES_PER_CONVERSATION:
            raise ValueError(
                f"会话消息数量超过限制 ({self.MAX_MESSAGES_PER_CONVERSATION})"
            )

        # 调用 LLM
        client = self._llm_client_factory(provider)

        # 如果没有指定模型，使用 provider 的默认模型
        if model is None:
            model = get_settings().get_default_model(provider)

        messages_for_llm = conv.get_messages_for_llm(system_prompt)

        def generate() -> Iterator[str]:
            full_response = ""
            for chunk in client.stream_message(
                messages=messages_for_llm,
                model=model,
            ):
                full_response += chunk
                yield chunk
            # 保存助手回复
            conv.add_message(Role.assistant, full_response)
            # 持久化保存
            self._store.save(conv)
            # 检查是否需要摘要（摘要可能修改 messages）
            self._maybe_summarize(conv, provider)
            # 如果生成了摘要，再次保存
            if conv.is_summarized:
                self._store.save(conv)

        return generate(), conv.id
