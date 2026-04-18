"""会话存储接口和实现。"""

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path

from .models import Conversation


logger = logging.getLogger(__name__)


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
        conversation.updated_at = datetime.now(timezone.utc)
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


class FileConversationStore(ConversationStore):
    """文件会话存储实现。"""

    def __init__(self, base_dir: Path | None = None):
        """初始化文件存储。

        Args:
            base_dir: 存储目录，默认为 ~/.ai-chat/conversations/
        """
        if base_dir is None:
            base_dir = Path.home() / ".ai-chat" / "conversations"
        self._base_dir = base_dir
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        """确保存储目录存在。"""
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, conversation_id: str) -> Path:
        """获取会话文件路径。

        Args:
            conversation_id: 会话 ID。

        Returns:
            会话文件路径。
        """
        return self._base_dir / f"{conversation_id}.json"

    def _load(self, conversation_id: str) -> Conversation | None:
        """从文件加载会话。

        Args:
            conversation_id: 会话 ID。

        Returns:
            会话对象，不存在则返回 None。
        """
        file_path = self._get_file_path(conversation_id)
        if not file_path.exists():
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Conversation.model_validate(data)
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Failed to load conversation {conversation_id}: {e}")
            return None

    def _save(self, conversation: Conversation) -> None:
        """保存会话到文件。

        Args:
            conversation: 会话对象。
        """
        self._ensure_dir()
        file_path = self._get_file_path(conversation.id)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(conversation.model_dump(mode="json"), f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save conversation {conversation.id}: {e}")
            raise

    def create(self) -> Conversation:
        """创建新会话。"""
        conv = Conversation()
        self._save(conv)
        return conv

    def get(self, conversation_id: str) -> Conversation | None:
        """获取会话。"""
        return self._load(conversation_id)

    def save(self, conversation: Conversation) -> None:
        """保存会话。"""
        conversation.updated_at = datetime.now(timezone.utc)
        self._save(conversation)

    def delete(self, conversation_id: str) -> bool:
        """删除会话。"""
        file_path = self._get_file_path(conversation_id)
        if file_path.exists():
            try:
                file_path.unlink()
                return True
            except Exception as e:
                logger.error(f"Failed to delete conversation {conversation_id}: {e}")
                return False
        return False

    def list(self) -> list[Conversation]:
        """列出所有会话。"""
        self._ensure_dir()
        conversations = []
        for file_path in self._base_dir.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                conv = Conversation.model_validate(data)
                conversations.append(conv)
            except (json.JSONDecodeError, Exception) as e:
                logger.warning(f"Failed to load conversation from {file_path}: {e}")
                continue
        return sorted(conversations, key=lambda c: c.updated_at, reverse=True)


class ConversationStoreFactory:
    """会话存储工厂。"""

    _stores: dict[str, type[ConversationStore]] = {
        "memory": InMemoryConversationStore,
        "file": FileConversationStore,
    }

    @classmethod
    def register(cls, name: str, store_class: type[ConversationStore]) -> None:
        """注册存储类型。

        Args:
            name: 存储类型名称。
            store_class: 存储类。
        """
        cls._stores[name] = store_class

    @classmethod
    def create(cls, name: str = "memory", **kwargs) -> ConversationStore:
        """创建存储实例。

        Args:
            name: 存储类型名称。
            **kwargs: 传递给存储构造函数的参数。

        Returns:
            存储实例。
        """
        if name not in cls._stores:
            raise ValueError(f"Unknown store type: {name}. Available: {list(cls._stores.keys())}")
        return cls._stores[name](**kwargs)
