## Context

当前的 AI Chat 应用只能处理单轮对话，每次请求都是独立的，无法记住之前的对话上下文。用户期望能够进行连续的多轮对话，AI 能够理解对话历史并基于上下文进行回复。

现有 API 接口（`/chat`, `/chat/stream`）只接收单条消息，没有会话概念。需要扩展为支持多轮对话。

## Goals / Non-Goals

**Goals:**
- 实现对话管理模块，支持多轮对话
- 提供消息模型（Message、Conversation）
- 提供对话历史存储和检索能力
- ChatService 封装对话逻辑和上下文管理

**Non-Goals:**
- 不实现持久化存储（对话数据仅存在内存中）
- 不实现用户认证和会话隔离
- 不实现对话摘要或压缩（后续可扩展）

## Decisions

### 1. 内存存储 vs 持久化存储

**决定**: 内存存储（初期）

**理由**:
- 简化实现复杂度，快速上线
- 适合个人使用场景
- 后续可通过接口抽象支持多种存储后端

**替代方案**:
- SQLite/文件持久化：增加复杂度，但适合生产环境
- Redis：需要额外部署，适合分布式场景

### 2. 数据模型设计

**决定**: 使用 Pydantic 模型 + 内存字典存储

```python
class Role(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

class Message(BaseModel):
    role: Role
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    messages: list[Message] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**理由**: Pydantic 提供验证和序列化，与现有代码风格一致

### 3. 对话历史传递方式

**决定**: 客户端传递 conversation_id，服务端返回新的 conversation_id

**理由**:
- 无状态 API 设计，便于扩展
- 客户端管理会话 ID，简化服务端逻辑
- 支持 SSE 流式响应

### 4. API 扩展

**修改 `/chat` 和 `/chat/stream`**:
- 请求新增 `conversation_id`（可选，None 表示新对话）
- 响应新增 `conversation_id`（用于继续对话）

**理由**: 最小化 API 变更，向后兼容

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| 对话数据丢失（内存重启） | 记录为后续持久化任务 |
| 对话过长导致上下文溢出 | 限制单会话消息数量（如 100 条） |
| 内存占用增长 | 定期清理过期会话 |

## Open Questions

1. 是否需要实现会话过期机制（如 24 小时后自动删除）？
2. 是否需要限制单用户会话数量？
3. 是否需要支持对话元数据（标题、标签）？
