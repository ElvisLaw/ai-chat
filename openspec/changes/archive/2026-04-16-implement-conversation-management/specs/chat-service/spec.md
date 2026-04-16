# Chat Service

## Overview

聊天服务主类，封装对话逻辑和 LLM 调用。

## ChatService

### Initialization

```python
class ChatService:
    """聊天服务。"""

    def __init__(
        self,
        store: ConversationStore,
        llm_client_factory: Callable[[str], LLMClient],
    ):
        """初始化聊天服务。

        Args:
            store: 会话存储实例。
            llm_client_factory: LLM 客户端工厂函数，接受 provider 返回客户端。
        """
```

### Methods

#### chat

处理同步聊天请求。

```python
def chat(
    self,
    message: str,
    provider: str = "openai",
    conversation_id: str | None = None,
    system_prompt: str | None = None,
    model: str | None = None,
) -> tuple[str, str]:
    """处理聊天请求。

    Args:
        message: 用户消息。
        provider: LLM 提供商。
        conversation_id: 会话 ID（None 表示新会话）。
        system_prompt: 系统提示词。
        model: 模型名称。

    Returns:
        tuple[str, str]: (AI 回复, conversation_id)
    """
```

#### stream

处理流式聊天请求。

```python
def stream(
    self,
    message: str,
    provider: str = "openai",
    conversation_id: str | None = None,
    system_prompt: str | None = None,
    model: str | None = None,
) -> tuple[Iterator[str], str]:
    """处理流式聊天请求。

    Returns:
        tuple[Iterator[str], str]: (响应流, conversation_id)
    """
```

## Behavior

1. **新会话流程** (`conversation_id` is None):
   - 创建新会话
   - 保存用户消息到会话
   - 调用 LLM 获取回复
   - 保存回复到会话
   - 返回回复和新 conversation_id

2. **继续会话流程** (`conversation_id` is not None):
   - 获取已有会话
   - 保存用户消息到会话
   - 调用 LLM（传入历史消息）
   - 保存回复到会话
   - 返回回复和原 conversation_id

3. **错误处理**:
   - 会话不存在：创建新会话
   - LLM 调用失败：抛出异常，已保存的消息不回滚

## Integration

与现有 API 路由集成：

```python
from ai_chat.conversation import ChatService, InMemoryConversationStore

store = InMemoryConversationStore()
chat_service = ChatService(store=store, llm_client_factory=create_llm_client)

# 在 API 路由中使用
response, conv_id = chat_service.chat(
    message=request.message,
    provider=request.provider or "openai",
    conversation_id=request.conversation_id,
)
```
