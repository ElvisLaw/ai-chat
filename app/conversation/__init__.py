"""对话管理模块。

提供多轮对话支持，包括消息模型、会话存储和聊天服务。
"""

from .models import Role, Message, Conversation
from .store import (
    ConversationStore,
    InMemoryConversationStore,
    FileConversationStore,
    ConversationStoreFactory,
)
from .service import ChatService

__all__ = [
    "Role",
    "Message",
    "Conversation",
    "ConversationStore",
    "InMemoryConversationStore",
    "FileConversationStore",
    "ConversationStoreFactory",
    "ChatService",
]
