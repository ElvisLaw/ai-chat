"""FileConversationStore 单元测试。"""

import tempfile
from pathlib import Path

import pytest

from app.conversation import FileConversationStore, Conversation
from app.conversation.models import Role, Message


class TestFileConversationStore:
    """FileConversationStore 测试。"""

    def setup_method(self) -> None:
        """每个测试方法前创建临时目录。"""
        self._temp_dir = tempfile.mkdtemp()
        self._store = FileConversationStore(base_dir=Path(self._temp_dir))

    def teardown_method(self) -> None:
        """每个测试方法后清理临时目录。"""
        import shutil
        shutil.rmtree(self._temp_dir, ignore_errors=True)

    def test_create_conversation(self) -> None:
        """测试创建会话。"""
        conv = self._store.create()
        assert conv.id is not None
        assert len(conv.messages) == 0

    def test_save_and_get_conversation(self) -> None:
        """测试保存和获取会话。"""
        conv = self._store.create()
        conv.add_message(Role.user, "Hello")
        conv.add_message(Role.assistant, "Hi there!")
        self._store.save(conv)

        loaded = self._store.get(conv.id)
        assert loaded is not None
        assert len(loaded.messages) == 2
        assert loaded.messages[0].content == "Hello"
        assert loaded.messages[1].content == "Hi there!"

    def test_delete_conversation(self) -> None:
        """测试删除会话。"""
        conv = self._store.create()
        conv_id = conv.id
        self._store.save(conv)

        deleted = self._store.delete(conv_id)
        assert deleted is True

        loaded = self._store.get(conv_id)
        assert loaded is None

    def test_delete_nonexistent_conversation(self) -> None:
        """测试删除不存在的会话。"""
        deleted = self._store.delete("nonexistent-id")
        assert deleted is False

    def test_list_conversations(self) -> None:
        """测试列出所有会话。"""
        conv1 = self._store.create()
        conv1.add_message(Role.user, "First")
        self._store.save(conv1)

        conv2 = self._store.create()
        conv2.add_message(Role.user, "Second")
        self._store.save(conv2)

        conversations = self._store.list()
        assert len(conversations) == 2

    def test_list_conversations_sorted_by_updated_at(self) -> None:
        """测试会话列表按更新时间倒序。"""
        import time

        conv1 = self._store.create()
        self._store.save(conv1)

        time.sleep(0.01)  # 确保时间戳不同

        conv2 = self._store.create()
        self._store.save(conv2)

        conversations = self._store.list()
        # 后创建的应该在前面
        assert conversations[0].id == conv2.id
        assert conversations[1].id == conv1.id

    def test_get_nonexistent_conversation(self) -> None:
        """测试获取不存在的会话。"""
        loaded = self._store.get("nonexistent-id")
        assert loaded is None

    def test_file_path_format(self) -> None:
        """测试文件路径格式。"""
        conv = self._store.create()
        file_path = self._store._get_file_path(conv.id)
        assert file_path.parent == Path(self._temp_dir)
        assert file_path.name == f"{conv.id}.json"

    def test_conversation_is_summarized_field(self) -> None:
        """测试 is_summarized 字段持久化。"""
        conv = self._store.create()
        conv.is_summarized = True
        self._store.save(conv)

        loaded = self._store.get(conv.id)
        assert loaded is not None
        assert loaded.is_summarized is True
