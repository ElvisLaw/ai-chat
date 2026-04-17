## ADDED Requirements

### Requirement: Dependency Injection via FastAPI Depends()

所有需要 `ChatService` 的路由 SHALL 通过 FastAPI `Depends()` 注入获取，而非模块级全局变量。依赖的创建和管理由应用 `lifespan` 统一负责。

#### Scenario: Chat service is injected via Depends

- **WHEN** `POST /chat` 或 `POST /chat/stream` 被调用时
- **THEN** 路由处理函数通过 `Depends(get_chat_service)` 获取 `ChatService` 实例
- **AND** 该实例来自 `app.state`，由 `lifespan` 入口阶段创建

### Requirement: Store and Service created in lifespan

`ConversationStore` 和 `ChatService` 实例 SHALL 在 FastAPI 应用的 `lifespan` 进入阶段（`yield` 之前）创建，并存入 `app.state`。

#### Scenario: Resources are created before request handling

- **WHEN** FastAPI 应用启动时
- **THEN** `lifespan` 的进入阶段创建 `InMemoryConversationStore` 实例
- **AND** 创建 `ChatService(store=store, ...)` 并存入 `app.state`
- **AND** 此后才开始处理请求

### Requirement: Backward Compatible API

外部 API 端点（`/health`、`/chat`、`/chat/stream`）的请求格式、响应格式和错误处理 SHALL 与修改前完全一致。

#### Scenario: API behavior unchanged

- **WHEN** 任何外部客户端调用 `/chat` 或 `/chat/stream`
- **THEN** 响应格式为 `{"response": "...", "conversation_id": "..."}` 或流式 SSE
- **AND** 错误响应格式和状态码与修改前一致
