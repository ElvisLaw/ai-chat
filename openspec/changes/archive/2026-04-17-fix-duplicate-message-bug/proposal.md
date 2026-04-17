## Why

多轮对话实现中存在 bug：用户消息被重复发送给 LLM 模型。第二轮对话开始，模型会收到重复输入，导致回答质量下降和 token 成本浪费。

## What Changes

修复消息重复发送的问题：

- 修改 `ChatService.chat()` 和 `ChatService.stream()` 方法，不再将用户消息作为单独参数传递
- 改为直接传递已组装好的完整消息历史（包括当前用户消息）给 LLM 客户端
- 修改 `OpenAIClient` 和 `AnthropicClient` 的 `send_message()` 和 `stream_message()` 方法，移除重复追加 user 消息的逻辑

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `chat-service`: 修复 chat() 和 stream() 方法的消息组装逻辑
- `openai-client`: 移除 send_message/stream_message 中重复追加 user 消息
- `anthropic-client`: 移除 send_message/stream_message 中重复追加 user 消息

## Impact

- 修改 `src/ai_chat/conversation/service.py` — 消息组装逻辑
- 修改 `src/ai_chat/clients/openai_client.py` — 移除重复 user 消息追加
- 修改 `src/ai_chat/clients/anthropic_client.py` — 移除重复 user 消息追加
