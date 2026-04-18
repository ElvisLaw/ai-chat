"""对话记忆集成测试。

测试持久化、缓冲和摘要的完整流程。
"""

import tempfile
import shutil
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from app.conversation import FileConversationStore, ChatService
from app.conversation.models import Role, Message
from app.conversation.memory import ConversationBuffer, MemorySummarizer
from app.settings import get_settings


class FakeStreamingClient:
    """模拟流式 LLM 客户端。"""

    def __init__(self, response: str = "Fake response"):
        self._response = response

    def stream_message(self, messages: list[dict], **kwargs):
        """模拟流式响应。"""
        for chunk in self._response:
            yield chunk

    def send_message(self, messages: list[dict], **kwargs):
        """模拟非流式响应。"""
        return f"Summary: {messages[-1]['content'][:50]}..."


class TestConversationMemoryIntegration:
    """对话记忆集成测试。"""

    def setup_method(self) -> None:
        """每个测试方法前创建临时目录和存储。"""
        self._temp_dir = tempfile.mkdtemp()
        self._store = FileConversationStore(base_dir=Path(self._temp_dir))
        self._settings = get_settings()

    def teardown_method(self) -> None:
        """每个测试方法后清理临时目录。"""
        shutil.rmtree(self._temp_dir, ignore_errors=True)

    def test_persistence_survives_restart(self) -> None:
        """测试持久化在服务重启后仍然保留。"""
        # 创建会话并添加消息
        conv = self._store.create()
        conv.add_message(Role.user, "Hello")
        conv.add_message(Role.assistant, "Hi there!")
        conv.add_message(Role.user, "How are you?")
        self._store.save(conv)
        conv_id = conv.id

        # 模拟服务重启 - 创建新的 store 实例
        new_store = FileConversationStore(base_dir=Path(self._temp_dir))

        # 验证数据完整保留
        loaded = new_store.get(conv_id)
        assert loaded is not None
        assert len(loaded.messages) == 3
        assert loaded.messages[0].content == "Hello"
        assert loaded.messages[1].content == "Hi there!"
        assert loaded.messages[2].content == "How are you?"

    def test_buffer_trim_by_count(self) -> None:
        """测试按消息数量缓冲清理。"""
        conv = self._store.create()

        # 添加超过缓冲限制的消息
        for i in range(25):
            conv.add_message(Role.user, f"Message {i}")

        buffer = ConversationBuffer()
        buffer.buffer_messages(conv)

        # 应该只保留最新的 20 条消息
        user_messages = [m for m in conv.messages if m.role == Role.user]
        assert len(user_messages) == 20
        # 最新的消息应该在最后
        assert user_messages[-1].content == "Message 24"

    def test_buffer_trim_by_tokens(self) -> None:
        """测试按 Token 数量缓冲清理。"""
        conv = self._store.create()

        # 添加长消息直到超过 Token 限制
        long_content = "x" * 2000  # ~500 tokens
        for i in range(10):
            conv.add_message(Role.user, f"Message {i}: {long_content}")

        buffer = ConversationBuffer()
        buffer.buffer_messages(conv)

        # 应该删除一些消息以满足 Token 限制
        total_tokens = sum(len(m.content) // 4 for m in conv.messages)
        assert total_tokens <= self._settings.memory_max_tokens

    def test_summarization_triggers_correctly(self) -> None:
        """测试摘要触发条件判断。"""
        conv = self._store.create()
        conv.add_message(Role.system, "You are a helpful assistant.")

        # 添加未达到阈值的消息
        for i in range(5):
            conv.add_message(Role.user, f"Short message {i}")

        summarizer = MemorySummarizer(llm_client_factory=lambda p: FakeStreamingClient())
        assert not summarizer.should_summarize(conv)

        # 添加更多消息达到阈值（需要 > 15 消息且 > 3000 tokens）
        # "x" * 600 ≈ 150 tokens，每个消息约 609 chars
        for i in range(20):
            conv.add_message(Role.user, f"Message {i}" + "x" * 600)

        # 现在应该有 25 条用户消息，> 3000 tokens
        assert summarizer.should_summarize(conv)

    def test_summarization_preserves_key_info(self) -> None:
        """测试摘要保留关键信息。"""
        conv = self._store.create()
        conv.add_message(Role.system, "You are a helpful assistant.")
        conv.add_message(Role.user, "I want to learn Python programming")
        conv.add_message(Role.assistant, "Great! Let's start with variables and data types.")
        conv.add_message(Role.user, "What about functions?")
        conv.add_message(Role.assistant, "Functions are blocks of reusable code...")

        summarizer = MemorySummarizer(llm_client_factory=lambda p: FakeStreamingClient())
        summarizer.summarize(conv, provider="openai")

        # 摘要后 is_summarized 应该为 True
        assert conv.is_summarized is True

        # 摘要内容应该在 system 消息中
        system_msg = conv.messages[0]
        assert system_msg.role == Role.system
        assert len(system_msg.content) > 0

    def test_full_memory_flow(self) -> None:
        """测试完整的记忆流程：创建 -> 添加消息 -> 缓冲 -> 摘要 -> 持久化。"""
        # 1. 创建服务
        service = ChatService(
            store=self._store,
            llm_client_factory=lambda p: FakeStreamingClient("Integration test response")
        )

        # 2. 创建新对话（需要迭代生成器才能保存消息）
        generator, conversation_id = service.stream(message="Start a Python learning session")
        list(generator)  # 迭代以触发保存
        conversation = self._store.get(conversation_id)
        assert conversation is not None

        # 3. 添加多条消息
        for i in range(20):
            generator, _ = service.stream(message=f"Message {i}")
            list(generator)  # 迭代以触发保存

        # 4. 验证消息已保存
        conversation = self._store.get(conversation_id)
        assert len(conversation.messages) > 0

        # 5. 模拟服务重启，验证数据持久化
        new_store = FileConversationStore(base_dir=Path(self._temp_dir))
        loaded = new_store.get(conversation_id)
        assert loaded is not None
        assert len(loaded.messages) == len(conversation.messages)

    def test_list_conversations_includes_summarized(self) -> None:
        """测试列出会话时包含已摘要的会话。"""
        conv1 = self._store.create()
        conv1.add_message(Role.user, "Conversation 1")
        self._store.save(conv1)

        conv2 = self._store.create()
        conv2.add_message(Role.user, "Conversation 2")
        conv2.is_summarized = True
        self._store.save(conv2)

        conversations = self._store.list()
        assert len(conversations) == 2

        ids = [c.id for c in conversations]
        assert conv1.id in ids
        assert conv2.id in ids

    def test_delete_removes_file(self) -> None:
        """测试删除会话同时删除文件。"""
        conv = self._store.create()
        conv.add_message(Role.user, "To be deleted")
        self._store.save(conv)

        file_path = self._store._get_file_path(conv.id)
        assert file_path.exists()

        deleted = self._store.delete(conv.id)
        assert deleted is True
        assert not file_path.exists()

        # 再次删除应返回 False
        deleted_again = self._store.delete(conv.id)
        assert deleted_again is False
