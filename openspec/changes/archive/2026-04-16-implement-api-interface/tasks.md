## 1. API Server Module

- [x] 1.1 创建 `src/ai_chat/api/__init__.py` - API 模块初始化
- [x] 1.2 创建 `src/ai_chat/api/server.py` - FastAPI 应用主入口
- [x] 1.3 配置 CORS 中间件
- [x] 1.4 添加 /health 健康检查端点

## 2. Request/Response Models

- [x] 2.1 创建 `src/ai_chat/api/models.py` - Pydantic 请求/响应模型
- [x] 2.2 实现 ChatRequest 模型
- [x] 2.3 实现 ChatResponse 模型

## 3. Chat Endpoint

- [x] 3.1 创建 `src/ai_chat/api/routes/chat.py` - 聊天路由
- [x] 3.2 实现 POST /chat 端点（同步）
- [x] 3.3 实现 POST /chat/stream 端点（流式 SSE）
- [x] 3.4 添加 LLM 客户端依赖注入

## 4. Dependencies

- [x] 4.1 添加 fastapi 到 requirements.txt
- [x] 4.2 添加 uvicorn 到 requirements.txt

## 5. Verification

- [x] 5.1 验证 API 服务器可启动
- [x] 5.2 验证 /health 端点返回正确
- [x] 5.3 验证 /chat 端点可接收请求
- [x] 5.4 验证 /chat/stream 端点返回 SSE 流
