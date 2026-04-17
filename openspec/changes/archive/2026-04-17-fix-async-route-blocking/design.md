## Context

FastAPI 路由层使用 `async def`，但 LLM 客户端（OpenAI SDK `OpenAI`、Anthropic SDK `Anthropic`）的 `send_message()` / `stream_message()` 是同步阻塞调用。高并发时，同步 HTTP 请求会阻塞事件循环，导致其他请求无法并发处理。

## Goals / Non-Goals

**Goals:**
- 解除事件循环阻塞，提高并发吞吐量
- 不改变外部 API 行为（接口、响应格式、错误处理不变）
- 最小改动：仅修改 `service.py`，不引入新客户端或重构客户端代码

**Non-Goals:**
- 不换用 async 客户端库（改动过大）
- 不修改 `BaseLLMClient` 接口
- 不修改 `chat.py` 路由层

## Decisions

### Decision: 使用 `asyncio.to_thread()` 封装同步 SDK 调用

**选择理由：**

`asyncio.to_thread()` 将同步函数派发到默认线程池（`ThreadPoolExecutor`）异步执行，且在 async 函数中可以直接 `await` 其返回的协程。对于当前改动范围，这是最小侵入的解法。

```python
# service.py - chat() 方法
response = await asyncio.to_thread(
    client.send_message, messages=messages_for_llm, model=model
)
```

对于 `stream_message()`，由于是生成器，需要额外处理：

```python
# service.py - stream() 方法
def generate():
    for chunk in client.stream_message(messages=messages_for_llm, model=model):
        yield chunk

gen, conv_id = generate(), conv.id
return await asyncio.to_thread(lambda: list(gen)), conv_id  # 不可行

# 正确做法：直接返回异步生成器
async def async_generate():
    for chunk in await asyncio.to_thread(
        client.stream_message, messages=messages_for_llm, model=model
    ):
        yield chunk
```

实际上 `stream_message` 是同步生成器，无法直接用 `to_thread` 包装。最简方案是在路由层处理：

```python
# chat.py - chat_stream()
async def chat_stream(request):
    generator, conv_id = _chat_service.stream(...)
    # 同步生成器在 to_thread 中运行
    async for chunk in asyncio.to_thread(lambda: list(generator)):
        yield f"data: {chunk}\n\n"
```

**备选方案对比：**

| 方案 | 优点 | 缺点 |
|------|------|------|
| A. `asyncio.to_thread()` | 最小改动 | 线程开销，对生成器处理复杂 |
| B. 改 `def` 路由 | 简单直接 | 失去 async 能力，StreamingResponse 需特殊处理 |
| C. 换 async 客户端 | 最干净 | 需重写 client，改动大 |

**结论：** 方案 A 配合路由层生成器处理，平衡了改动量和效果。

## Risks / Trade-offs

- **[Risk]** 线程池争用 → [Mitigation] 默认线程池大小为 `min(32, os.cpu_count() + 4)`，通常足够；后续可配置
- **[Trade-off]** 线程切换开销 → 同步改异步本身有 overhead，但阻塞损失更大
- **[Risk]** 生成器跨线程 → [Mitigation] 流式场景下直接在 `to_thread` 内迭代收集后 yield（复杂度可接受）
