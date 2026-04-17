"""会话存储接口和实现。"""

from abc import ABC, abstractmethod
from datetime import datetime

from .models import Conversation


class ConversationStore(ABC):
    """会话存储抽象接口。"""

    @abstractmethod
    def create(self) -> Conversation:
        """创建新会话。

        Returns:
            新创建的会话。
        """

    @abstractmethod
    def get(self, conversation_id: str) -> Conversation | None:
        """获取会话。

        Args:
            conversation_id: 会话 ID。

        Returns:
            会话对象，不存在则返回 None。
        """

    @abstractmethod
    def save(self, conversation: Conversation) -> None:
        """保存会话。

        Args:
            conversation: 会话对象。
        """

    @abstractmethod
    def delete(self, conversation_id: str) -> bool:
        """删除会话。

        Args:
            conversation_id: 会话 ID。

        Returns:
            删除成功返回 True，不存在返回 False。
        """

    @abstractmethod
    def list(self) -> list[Conversation]:
        """列出所有会话。

        Returns:
            会话列表，按最后更新时间倒序。
        """


class InMemoryConversationStore(ConversationStore):
    """内存会话存储实现。"""

    def __init__(self):
        """初始化内存存储。"""
        self._store: dict[str, Conversation] = {}

    def create(self) -> Conversation:
        """创建新会话。"""
        conv = Conversation()
        self._store[conv.id] = conv
        return conv

    def get(self, conversation_id: str) -> Conversation | None:
        """获取会话。"""
        return self._store.get(conversation_id)

    def save(self, conversation: Conversation) -> None:
        """保存会话。"""
        conversation.updated_at = datetime.utcnow()
        self._store[conversation.id] = conversation

    def delete(self, conversation_id: str) -> bool:
        """删除会话。"""
        if conversation_id in self._store:
            del self._store[conversation_id]
            return True
        return False

    def list(self) -> list[Conversation]:
        """列出所有会话。"""
        return sorted(
            self._store.values(),
            key=lambda c: c.updated_at,
            reverse=True
        )
