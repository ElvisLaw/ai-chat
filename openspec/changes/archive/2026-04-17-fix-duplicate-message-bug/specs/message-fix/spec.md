# Message Fix

## Overview

修复多轮对话中消息重复发送的问题。

## Problem

当前实现中，消息被重复添加到消息历史：
1. `ChatService` 将消息添加到会话历史
2. `ChatService` 组装完整历史
3. `ChatService` 将当前消息作为单独参数传递
4. LLM 客户端再次追加用户消息

## Solution

### ChatService

传递完整消息历史给 LLM 客户端：

```python
def chat(self, message: str, ...) -> tuple[str, str]:
    conv.add_message(Role.user, message)
    messages_for_llm = conv.get_messages_for_llm(system_prompt)
    # 传递完整历史，不传单独 message
    response = client.send_message(messages=messages_for_llm)
```

### LLM Clients

接收 `messages` 参数（消息历史数组），不再追加 user 消息：

```python
def send_message(self, messages: list[dict], **kwargs) -> str:
    # 直接使用 messages，不再追加
    response = self._client.chat.completions.create(
        model=kwargs.pop("model", self._model),
        messages=messages,
        ...
    )
```

## Files to Modify

- `src/ai_chat/conversation/service.py`
- `src/ai_chat/clients/openai_client.py`
- `src/ai_chat/clients/anthropic_client.py`
