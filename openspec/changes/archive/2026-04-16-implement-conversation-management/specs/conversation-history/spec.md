# Conversation History

## Overview

对话历史的存储、查询和管理功能。

## Interface

### ConversationStore

内存会话存储接口。

```python
class ConversationStore:
    """会话存储接口。"""

    def create(self) -> Conversation:
        """创建新会话。"""

    def get(self, conversation_id: str) -> Conversation | None:
        """获取会话。"""

    def save(self, conversation: Conversation) -> None:
        """保存会话。"""

    def delete(self, conversation_id: str) -> bool:
        """删除会话。"""

    def list(self) -> list[Conversation]:
        """列出所有会话（按 updated_at 倒序）。"""
```

## Behavior

- `create()`: 创建新会话，返回包含空消息列表的 Conversation
- `get()`: 根据 ID 查找会话，未找到返回 None
- `save()`: 更新会话的 updated_at 时间戳
- `delete()`: 删除会话，成功返回 True，不存在返回 False
- `list()`: 返回所有会话，按最后更新时间倒序

## Implementation

使用内存字典存储，会话 ID 为键：

```python
class InMemoryConversationStore(ConversationStore):
    """内存会话存储。"""

    def __init__(self):
        self._store: dict[str, Conversation] = {}

    def create(self) -> Conversation:
        conv = Conversation()
        self._store[conv.id] = conv
        return conv
```

## Limits

- 单会话消息数量限制：100 条（超出时触发警告）
- 存储限制：无（内存允许范围内）
