## Why

当前 AI Chat 只支持简单的内存会话存储（`InMemoryConversationStore`），会话数据在服务重启后丢失，且长对话会无限累积消息导致性能问题。需要实现对话记忆功能，支持持久化和智能摘要。

## What Changes

- 新增会话持久化存储（JSON 文件）
- 新增对话摘要功能（自动压缩长对话）
- 新增基于 Token 数量的对话长度管理
- 支持会话历史跨重启持久化

## Capabilities

### New Capabilities
- `memory-buffer`: 对话缓冲 - 管理长对话消息，自动清理超出会话长度限制的消息
- `memory-summary`: 对话摘要 - 当对话超过阈值时自动生成摘要，保留关键信息
- `memory-persistence`: 记忆持久化 - 将对话历史保存到文件系统，支持跨会话恢复

### Modified Capabilities
- `conversation-store`: 扩展 `ConversationStore` 接口，支持持久化实现

## Impact

- `app/conversation/store.py` - 新增持久化存储实现
- `app/conversation/memory.py` - 新增对话记忆模块（摘要、缓冲）
- `app/conversation/models.py` - 可能需要添加摘要字段
- 依赖：无新增外部依赖
