"""对话摘要单元测试。"""

from unittest.mock import MagicMock, patch

import pytest

from app.conversation import Conversation
from app.conversation.memory import MemorySummarizer
from app.conversation.models import Role


class TestMemorySummarizer:
    """MemorySummarizer 测试。"""

    def setup_method(self) -> None:
        """每个测试方法前创建模拟的 LLM 客户端工厂。"""
        self._mock_client = MagicMock()
        self._mock_factory = MagicMock(return_value=self._mock_client)
        self._summarizer = MemorySummarizer(self._mock_factory)

    def _create_conversation_with_messages(self, message_count: int) -> Conversation:
        """创建带有指定数量消息的会话。"""
        conv = Conversation()
        for i in range(message_count):
            conv.add_message(Role.user, f"User message {i}")
            conv.add_message(Role.assistant, f"Assistant reply {i}")
        return conv

    def test_should_summarize_not_yet_summarized_under_threshold(self) -> None:
        """测试消息数低于阈值时不触发摘要。"""
        conv = self._create_conversation_with_messages(5)
        assert not self._summarizer.should_summarize(conv)

    def test_should_summarize_already_summarized(self) -> None:
        """测试已摘要的对话不再触发摘要。"""
        conv = self._create_conversation_with_messages(20)
        conv.is_summarized = True
        assert not self._summarizer.should_summarize(conv)

    def test_summarize_generates_summary(self) -> None:
        """测试摘要生成。"""
        self._mock_client.send_message.return_value = "这是对话摘要"

        conv = self._create_conversation_with_messages(10)
        self._summarizer.summarize(conv)

        self._mock_client.send_message.assert_called_once()
        assert conv.is_summarized is True

    def test_summarize_replaces_existing_summary(self) -> None:
        """测试摘要替换已有摘要。"""
        self._mock_client.send_message.return_value = "新摘要内容"

        conv = Conversation()
        conv.add_message(Role.system, "旧摘要")
        conv.add_message(Role.user, "User message")
        conv.is_summarized = True

        self._summarizer.summarize(conv)

        # 第一条消息应该是新的摘要
        assert conv.messages[0].role == Role.system
        assert conv.messages[0].content == "新摘要内容"
        assert conv.is_summarized is True

    def test_summarize_inserts_summary_if_no_system_message(self) -> None:
        """测试在无系统消息时插入摘要。"""
        self._mock_client.send_message.return_value = "新摘要"

        conv = Conversation()
        conv.add_message(Role.user, "User message")
        conv.add_message(Role.assistant, "Assistant reply")

        self._summarizer.summarize(conv)

        # 第一条消息应该是摘要
        assert conv.messages[0].role == Role.system
        assert conv.messages[0].content == "新摘要"

    def test_estimate_tokens(self) -> None:
        """测试 Token 估算。"""
        text = "Hello, world!"
        tokens = self._summarizer._estimate_tokens(text)
        assert tokens == len(text) // 4
