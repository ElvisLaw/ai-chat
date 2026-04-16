## Why

当前的 AI Chat 应用只能处理单轮对话，无法记住之前的对话上下文。多轮对话能力是聊天机器人的基础功能，用户期望能够进行连续的、上下文相关的交流。

## What Changes

- 新增 `src/ai_chat/conversation/` 模块，包含对话管理相关代码
- 实现消息模型（Message、Conversation）
- 实现对话历史管理（存储、检索、管理对话历史）
- 实现聊天服务主类（ChatService），封装对话逻辑
- API 端点支持传递 conversation_id 以继续历史对话

## Capabilities

### New Capabilities

- `message-models`: 消息数据模型（Message、Role、Conversation），使用 Pydantic 定义
- `conversation-history`: 对话历史管理（创建会话、保存消息、查询历史）
- `chat-service`: 聊天服务主类，封装 LLM 调用和对话上下文管理

### Modified Capabilities

- `chat-endpoint` (已有): 扩展支持 conversation_id 参数，实现多轮对话

## Impact

- **新增目录**: `src/ai_chat/conversation/` - 对话管理模块
- **修改文件**:
  - `src/ai_chat/api/models.py` - 新增 conversation_id 字段
  - `src/ai_chat/api/routes/chat.py` - 支持多轮对话
- **依赖**: 无新依赖，基于现有 LLM 客户端和 API 接口
