## ADDED Requirements

### Requirement: async-llm-invocation

`ChatService.chat()` 和 `ChatService.stream()` 方法在执行 LLM 客户端调用时，必须将同步 SDK 调用派发到线程池执行，不应阻塞调用方的事件循环。

#### Scenario: chat() 方法异步执行同步 SDK

- **WHEN** 调用方 `await chat_service.chat(message=..., provider=..., ...)`
- **THEN** `client.send_message()` 在线程池中执行，不阻塞调用方事件循环
- **AND** 返回值类型和内容不变：`tuple[str, str]` 即 `(response, conversation_id)`

#### Scenario: stream() 方法异步执行同步 SDK

- **WHEN** 调用方 `await chat_service.stream(message=..., provider=..., ...)`
- **THEN** `client.stream_message()` 在线程池中执行，不阻塞调用方事件循环
- **AND** 返回生成器类型不变，仍可逐块 yield 内容块

#### Scenario: 外部 API 行为不变

- **WHEN** 任何外部调用方调用 `/chat` 或 `/chat/stream` 端点
- **THEN** 响应格式、错误处理、conversation_id 管理均与修改前完全一致
- **AND** 不引入新的错误类型
