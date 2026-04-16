## Context

AI Chat 需要 Web API 接口供前端调用。使用 FastAPI 构建轻量 REST API。

## Goals / Non-Goals

**Goals:**
- 提供 /chat 聊天完成接口
- 提供 /chat/stream 流式响应接口
- 提供 /health 健康检查
- 支持 CORS 跨域

**Non-Goals:**
- 不实现用户认证（后续 auth change 处理）
- 不实现数据库（对话历史存储后续处理）
- 不实现 WebSocket（当前只需 SSE 流式响应）

## Decisions

### Decision 1: 使用 FastAPI 而非 Flask

FastAPI 原生支持：
- 自动 request/response 验证（Pydantic）
- 自动文档生成（Swagger UI）
- 异步支持
- 类型安全

**Why:** 比 Flask 更现代，Pydantic 集成更好。

### Decision 2: 流式响应使用 SSE

```python
@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def generate():
        for chunk in client.stream_message(request.message):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```

**Why:** SSE 简单易用，浏览器原生支持，前端实现方便。

### Decision 3: 使用依赖注入获取 LLM 客户端

```python
@router.post("/chat")
async def chat(request: ChatRequest, client: BaseLLMClient = Depends(get_llm_client)):
    return {"response": client.send_message(request.message)}
```

**Why:** 解耦清晰，便于测试和切换实现。

### Decision 4: CORS 配置通过环境变量

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Why:** 灵活配置，生产环境可限制域名。
