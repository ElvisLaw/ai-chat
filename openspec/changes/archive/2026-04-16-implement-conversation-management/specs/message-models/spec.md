# Message Models

## Overview

定义对话消息和会话的数据模型。

## Data Models

### Role

枚举类型，表示消息发送者角色。

| 值 | 说明 |
|----|------|
| `user` | 用户消息 |
| `assistant` | AI 助手消息 |
| `system` | 系统消息 |

### Message

消息模型。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `role` | `Role` | 是 | 消息角色 |
| `content` | `str` | 是 | 消息内容 |
| `timestamp` | `datetime` | 否 | 创建时间，默认当前时间 |

### Conversation

会话模型。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | `str` | 是 | 会话 ID（UUID hex） |
| `messages` | `list[Message]` | 是 | 消息列表 |
| `created_at` | `datetime` | 是 | 创建时间 |
| `updated_at` | `datetime` | 是 | 最后更新时间 |

## Usage

```python
from ai_chat.conversation.models import Role, Message, Conversation

# 创建消息
msg = Message(role=Role.user, content="你好")
print(msg)

# 创建会话
conv = Conversation()
conv.messages.append(msg)
print(conv.id)
```
