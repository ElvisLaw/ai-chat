"""对话记忆模块。

提供对话缓冲和摘要功能，管理长对话的生命周期。
"""

import logging
from typing import Any, Callable

from .models import Conversation, Role
from ..settings import get_settings


logger = logging.getLogger(__name__)


class MemorySummarizer:
    """对话摘要生成器。"""

    def __init__(
        self,
        llm_client_factory: Callable[[str], Any],
    ):
        """初始化摘要生成器。

        Args:
            llm_client_factory: LLM 客户端工厂函数。
        """
        self._llm_client_factory = llm_client_factory

    def _estimate_tokens(self, text: str) -> int:
        """估算文本的 Token 数。

        Args:
            text: 文本内容。

        Returns:
            估算的 Token 数。
        """
        return len(text) // 4

    def _generate_summary_prompt(self, conversation: Conversation) -> str:
        """生成摘要提示词。

        Args:
            conversation: 会话对象。

        Returns:
            摘要提示词。
        """
        settings = get_settings()
        max_chars = settings.memory_summary_max_chars

        # 获取对话内容（排除 system 消息）
        messages_content = []
        for msg in conversation.messages:
            if msg.role != Role.system:
                messages_content.append(f"{msg.role.value}: {msg.content}")

        content = "\n".join(messages_content)

        return f"""请为以下对话生成简洁摘要，保留核心主题、用户目标和关键结论。

要求：
- 摘要不超过 {max_chars} 字符（约 {max_chars // 4} 字）
- 使用中文
- 包含：对话主题、用户意图、关键结论

对话内容：
{content}

摘要："""

    def _generate_summary(self, conversation: Conversation, provider: str = "openai") -> str:
        """生成对话摘要。

        Args:
            conversation: 会话对象。
            provider: LLM 提供商。

        Returns:
            生成的摘要。
        """
        settings = get_settings()
        model = settings.get_default_model(provider)

        prompt = self._generate_summary_prompt(conversation)

        client = self._llm_client_factory(provider)

        response = client.send_message(
            messages=[{"role": "user", "content": prompt}],
            model=model,
        )

        return response.strip()

    def summarize(self, conversation: Conversation, provider: str = "openai") -> None:
        """对会话进行摘要。

        Args:
            conversation: 会话对象。
            provider: LLM 提供商。
        """
        summary = self._generate_summary(conversation, provider)

        # 将摘要保存为第一条 system 消息
        summary_message = conversation.messages[0] if (
            conversation.messages and conversation.messages[0].role == Role.system
        ) else None

        if summary_message:
            summary_message.content = summary
        else:
            from .models import Message
            conversation.messages.insert(0, Message(role=Role.system, content=summary))

        conversation.is_summarized = True

    def should_summarize(self, conversation: Conversation) -> bool:
        """判断是否需要摘要。

        Args:
            conversation: 会话对象。

        Returns:
            是否需要摘要。
        """
        if conversation.is_summarized:
            return False

        settings = get_settings()

        message_count = len([m for m in conversation.messages if m.role != Role.system])
        total_tokens = self._estimate_tokens(
            "".join(m.content for m in conversation.messages)
        )

        return (
            message_count >= settings.memory_summarize_threshold_messages
            and total_tokens >= settings.memory_summarize_threshold_tokens
        )


class ConversationBuffer:
    """对话缓冲管理器。"""

    def __init__(self):
        """初始化缓冲管理器。"""
        self._settings = get_settings()

    def _estimate_tokens(self, text: str) -> int:
        """估算文本的 Token 数。

        Args:
            text: 文本内容。

        Returns:
            估算的 Token 数。
        """
        return len(text) // 4

    def _trim_by_count(self, conversation: Conversation) -> None:
        """按消息数量清理对话。

        保留系统消息和最新的缓冲条消息。

        Args:
            conversation: 会话对象。
        """
        max_size = self._settings.memory_buffer_size
        system_messages = [m for m in conversation.messages if m.role == Role.system]
        other_messages = [m for m in conversation.messages if m.role != Role.system]

        # 如果超过限制，保留最新的消息
        if len(other_messages) > max_size:
            other_messages = other_messages[-max_size:]

        conversation.messages = system_messages + other_messages

    def _trim_by_tokens(self, conversation: Conversation) -> None:
        """按 Token 数量清理对话。

        删除最早的 user 消息直到满足 Token 限制。

        Args:
            conversation: 会话对象。
        """
        max_tokens = self._settings.memory_max_tokens

        # 预先计算当前总 Token 数
        total_tokens = self._estimate_tokens(
            "".join(m.content for m in conversation.messages)
        )
        if total_tokens <= max_tokens:
            return

        # 找到需要删除的 user 消息（从后往前删除，避免索引偏移）
        to_remove = []
        accumulated_tokens = 0
        for i, msg in enumerate(conversation.messages):
            if msg.role == Role.user:
                accumulated_tokens += self._estimate_tokens(msg.content)
                to_remove.append(i)
                if total_tokens - accumulated_tokens <= max_tokens:
                    break

        # 反向删除
        for i in reversed(to_remove):
            conversation.messages.pop(i)

    def buffer_messages(self, conversation: Conversation) -> None:
        """对消息进行缓冲管理。

        Args:
            conversation: 会话对象。
        """
        # 先按数量清理
        self._trim_by_count(conversation)
        # 再按 Token 数量清理
        self._trim_by_tokens(conversation)
