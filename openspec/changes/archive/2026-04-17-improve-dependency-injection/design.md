## Context

FastAPI 路由在 `chat.py` 模块级直接实例化 `_store = InMemoryConversationStore()` 和 `_chat_service = ChatService(...)`。导入即创建，导致：
- 无法在测试时替换 store 实现
- 后续接入 Redis 等有连接生命周期资源时，连接管理与应用生命周期不同步
- 依赖关系不透明，代码审查困难

## Goals / Non-Goals

**Goals:**
- 将 store/service 的创建移到 `create_app()` 的 `lifespan` 中
- 路由通过 `Depends()` 获取 service，实现依赖注入
- 不改变任何外部 API 端点的请求/响应格式

**Non-Goals:**
- 不引入 IoC 容器或第三方 DI 框架（如 `punq`、`dependency-injector`）
- 不改变 `ChatService`/`InMemoryConversationStore` 内部实现
- 不处理 Redis/数据库的接入（留待后续 capability）

## Decisions

### Decision: 使用 `app.state` + FastAPI `Depends()`

**方案 A（采用）:** `app.state` 存资源 + `Depends()` 注入

```python
# server.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    store = InMemoryConversationStore()
    service = ChatService(store=store, llm_client_factory=_make_client_factory)
    app.state.store = store
    app.state.chat_service = service
    yield
    # cleanup if needed

def get_chat_service(state: Request.state) -> ChatService:
    return state.chat_service

# chat.py
@router.post("")
async def chat(request: ChatRequest, service: ChatService = Depends(get_chat_service)):
    ...
```

**方案 B:** FastAPI `Annotated[..., Depends(get_chat_service)]` 作为函数参数

**方案 C:** 第三方 IoC 容器（punq/dependency-injector）

**选择 A 的理由:** 最小改动，不需要引入额外依赖，利用 FastAPI 原生的 `app.state` + `Depends` 机制足够应对当前和近期的扩展需求。

### Decision: 资源在 `lifespan` 中创建

所有需要按请求共享的资源（store、service）都在 `lifespan` 的进入阶段创建，存入 `app.state`。lifespan 的 `yield` 之后可以执行清理逻辑（目前 `InMemoryConversationStore` 不需要，未来 Redis 等需要）。

### Decision: `llm_client_factory` 通过闭包引用 `get_settings`

`_get_llm_client` 依赖 `get_settings()` 获取配置。由于 `get_settings()` 本身就是单例，不需要额外注入。

```python
def _make_client_factory(provider: str):
    def create():
        return _get_llm_client(provider)
    return create
```

## Risks / Trade-offs

- **[Trade-off]** 所有请求共享同一个 store 实例 → 并发写入安全（`InMemoryConversationStore` 内部有锁），但水平扩展时无法共享（需后续 Redis 支持）
- **[Risk]** `app.state` 是直接赋值，非类型安全 → 通过 `Depends` 函数访问可以减少隐式类型问题，但 IDE 支持有限

## Migration Plan

1. 在 `server.py` 中实现 `lifespan`，创建 `app.state.chat_service`
2. 在 `chat.py` 添加 `get_chat_service()` 依赖函数，移除全局变量
3. 将 `_get_llm_client` 移到 `server.py` 或 `dependencies` 模块
4. 验证 `/health`、`/chat`、`/chat/stream` 行为不变
5. 原有全局变量删除
