## Context

多轮对话实现中，用户消息被重复发送给 LLM。当前流程：

1. `service.py:57` — 用户消息添加到会话
2. `service.py:73` — 组装完整历史消息（已包含用户消息）
3. 同时把 `message` 作为单独参数传递
4. `openai_client.py:72-74` — 再次追加 user 消息
5. `anthropic_client.py:57-58` — 再次追加 user 消息

## Goals / Non-Goals

**Goals:**
- 修复消息重复发送问题
- 保持 API 兼容

**Non-Goals:**
- 不改变现有接口
- 不添加新功能

## Decisions

### 方案：传递完整消息历史

**决定**：在 `ChatService` 中组装完整消息历史，直接传递给 LLM 客户端，不在客户端再次追加。

```python
# service.py
def chat(self, message, ...):
    conv.add_message(Role.user, message)
    messages_for_llm = conv.get_messages_for_llm(system_prompt)
    # 直接传递完整历史，不传单独 message
    response = client.send_message(messages=messages_for_llm)
```

**理由**：
- 消息历史由 ChatService 统一管理
- 避免职责混乱
- 简化客户端逻辑

### 接口变更

**ChatService**：
- `send_message(message, ...)` 改为 `send_message(messages, ...)`

**LLM 客户端**：
- 移除 `message` 参数
- 接收完整的消息历史数组

## Risks / Trade-offs

无显著风险。这是纯粹的 bug 修复。
