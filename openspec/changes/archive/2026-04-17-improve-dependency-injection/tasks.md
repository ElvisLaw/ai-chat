## 1. server.py — 迁移 lifespan 和依赖函数

- [x] 1.1 在 `lifespan` 入口阶段创建 `InMemoryConversationStore` 实例，存入 `app.state.store`
- [x] 1.2 在 `lifespan` 入口阶段创建 `ChatService`，存入 `app.state.chat_service`
- [x] 1.3 将 `_get_llm_client` 从 `chat.py` 移入 `server.py` 作为模块级私有函数
- [x] 1.4 实现 `get_chat_service(state: Request.state) -> ChatService` 依赖函数
- [x] 1.5 更新 `uvicorn.run` 使用 `app` 而非 `create_app()` 以保留 lifespan

## 2. chat.py — 移除全局变量，改用 Depends

- [x] 2.1 删除模块级的 `_store = InMemoryConversationStore()`
- [x] 2.2 删除模块级的 `_chat_service = ChatService(...)`
- [x] 2.3 导入 `Depends` 和 `get_chat_service`
- [x] 2.4 `chat()` 路由添加 `service: ChatService = Depends(get_chat_service)` 参数
- [x] 2.5 `chat_stream()` 路由添加 `service: ChatService = Depends(get_chat_service)` 参数
- [x] 2.6 路由内使用 `service` 而非全局 `_chat_service`

## 3. Verify

- [x] 3.1 启动 API 并验证 `/health` 返回 `{"status":"ok"}` ✓
- [x] 3.2 测试 `POST /chat`：发送 `{"message":"hello"}`，验证返回包含 `response` 和 `conversation_id` ✓
- [x] 3.3 测试 `POST /chat/stream`：发送 `{"message":"count to 3"}`，验证 SSE 流式响应 ✓
