"""对话缓冲单元测试。"""

from unittest.mock import patch

import pytest

from app.conversation import Conversation
from app.conversation.memory import ConversationBuffer
from app.conversation.models import Role


class TestConversationBuffer:
    """ConversationBuffer 测试。"""

    def setup_method(self) -> None:
        """每个测试方法前创建缓冲管理器。"""
        self._buffer = ConversationBuffer()

    def _create_conversation_with_messages(self, count: int, role: Role = Role.user) -> Conversation:
        """创建带有指定数量消息的会话。"""
        conv = Conversation()
        for i in range(count):
            conv.add_message(role, f"Message {i}")
        return conv

    def test_estimate_tokens(self) -> None:
        """测试 Token 估算。"""
        text = "Hello, world!"
        tokens = self._buffer._estimate_tokens(text)
        assert tokens == len(text) // 4

    def test_trim_by_count_under_limit(self) -> None:
        """测试消息数在限制内时不清理。"""
        conv = self._create_conversation_with_messages(10)
        original_count = len(conv.messages)
        self._buffer._trim_by_count(conv)
        assert len(conv.messages) == original_count

    def test_trim_by_count_over_limit(self) -> None:
        """测试消息数超过限制时清理。"""
        # 默认 buffer_size=20
        conv = self._create_conversation_with_messages(25)
        self._buffer._trim_by_count(conv)
        assert len(conv.messages) <= 20

    def test_trim_by_count_preserves_system_messages(self) -> None:
        """测试清理时保留系统消息。"""
        conv = Conversation()
        conv.add_message(Role.system, "System prompt")
        for i in range(25):
            conv.add_message(Role.user, f"Message {i}")
        conv.add_message(Role.assistant, "Reply")

        self._buffer._trim_by_count(conv)

        # 系统消息应该保留
        system_count = sum(1 for m in conv.messages if m.role == Role.system)
        assert system_count == 1

    def test_trim_by_tokens_under_limit(self) -> None:
        """测试 Token 数在限制内时不清理。"""
        conv = self._create_conversation_with_messages(5)
        original_count = len(conv.messages)
        self._buffer._trim_by_tokens(conv)
        assert len(conv.messages) == original_count

    def test_trim_by_tokens_removes_oldest_user_messages(self) -> None:
        """测试按 Token 清理时删除最早的用户消息。"""
        conv = Conversation()
        # 添加足够长的消息以超过限制（默认 4000 tokens）
        # 每个消息 2000 chars = ~500 tokens, 10 个 = ~5000 tokens
        long_content = "x" * 2000
        for _ in range(10):
            conv.add_message(Role.user, long_content)

        initial_count = len(conv.messages)
        self._buffer._trim_by_tokens(conv)

        # 应该删除了一些 user 消息
        assert len(conv.messages) < initial_count

    def test_buffer_messages_trims_both_count_and_tokens(self) -> None:
        """测试缓冲管理同时处理数量和 Token 限制。"""
        conv = Conversation()
        conv.add_message(Role.system, "System")
        # 添加超过 20 条消息
        for i in range(30):
            conv.add_message(Role.user, f"Message {i}")

        self._buffer.buffer_messages(conv)

        # 应该被清理到限制内
        assert len(conv.messages) <= 21  # 1 system + 20 others
