## Why

`chat.py:12-16` 在模块级创建全局 `_store`（`InMemoryConversationStore`）和 `_chat_service`，在导入时即实例化。这导致：
- 存储、配置、生命周期与导入时机强耦合
- 单元测试难以 mock 或替换 store
- 后续接入 Redis、数据库、限流、审计日志需要修改全局状态
- 路由层的依赖关系不透明，难以推理

## What Changes

- **server.py**: 在 `create_app()` 的 `lifespan` 中创建 `store` 和 `chat_service`，存入 `app.state`
- **chat.py**: 路由改用 `Depends(get_chat_service)` 获取 service，移除模块级全局变量
- **依赖获取函数**: 提供 `get_store()`、`get_chat_service()` 等 FastAPI 依赖函数
- **向后兼容**: 外部 API 端点不变，响应格式不变

## Capabilities

### New Capabilities
- `dependency-injection`: 使用 FastAPI `Depends()` 注入 `ChatService` 和 `ConversationStore`，替代模块级全局变量
- `lifecycle-managed-resources`: 在应用 `lifespan` 中管理 store/service 的创建和销毁，便于后续接入有连接生命周期资源（Redis、DB）

### Modified Capabilities
- 无（仅实现重构，不改变 API 行为）

## Impact

- `src/ai_chat/api/server.py`: 在 lifespan 中创建 store/service，存入 `app.state`
- `src/ai_chat/api/routes/chat.py`: 移除全局变量，改用 `Depends(get_chat_service)`
- `src/ai_chat/conversation/service.py`: 无改动
- `src/ai_chat/conversation/store.py`: 无改动
- 测试覆盖可受益于此 DI 结构（可注入 mock store）
