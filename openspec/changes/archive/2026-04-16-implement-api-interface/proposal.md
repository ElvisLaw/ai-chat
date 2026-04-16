## Why

AI Chat 应用需要通过 Web API 接口供前端调用。用户通过浏览器与 AI 对话，前端需要调用后端 API 获取 LLM 响应。需要一个轻量、高效的 HTTP 接口层。

## What Changes

- 新增 FastAPI Web 服务框架
- 实现聊天完成接口（同步/流式）
- 实现健康检查接口
- 实现模型切换接口
- 支持 CORS 跨域配置

## Capabilities

### New Capabilities
- `api-server`: FastAPI 服务主入口
- `chat-endpoint`: 聊天完成 API 端点
- `health-endpoint`: 健康检查端点
- `stream-response`: SSE 流式响应支持

### Modified Capabilities
<!-- 暂无修改现有功能 -->

## Impact

- `src/ai_chat/` - 新增 api/ 子模块
- `requirements.txt` - 新增 fastapi, uvicorn 依赖
- `openspec/specs/` - 暂无影响
