## Why

`chat.py` 的两个路由是 `async def`，但底层调用的 `send_message()` / `stream_message()` 是同步阻塞的 HTTP 调用。在高并发场景下，同步 SDK 会阻塞 FastAPI 的事件循环，导致所有并发请求被迫排队，吞吐量大幅下降。

## What Changes

- **service.py**: `chat()` 和 `stream()` 方法改为在事件循环的线程池中执行同步 SDK 调用（`asyncio.to_thread()`）
- **client 接口不变**: `BaseLLMClient` 的 `send_message()` / `stream_message()` 保持同步签名不变
- 路由层（`chat.py`）保持 `async def`，无需改动
- 不引入新的 async 客户端，复用现有同步 SDK

## Capabilities

### New Capabilities
- `async-llm-invocation`: 异步化 LLM 调用——通过线程池执行同步 SDK，不阻塞事件循环

### Modified Capabilities
- 无（仅实现层面改动，不改变 API 行为）

## Impact

- `src/ai_chat/conversation/service.py`: 添加 `asyncio.to_thread()` 封装 chat 和 stream 方法
- `src/ai_chat/api/routes/chat.py`: 无改动
- `src/ai_chat/clients/openai_client.py`: 无改动
- `src/ai_chat/clients/anthropic_client.py`: 无改动
- 外部行为不变：API 接口、响应格式、错误处理均保持一致
