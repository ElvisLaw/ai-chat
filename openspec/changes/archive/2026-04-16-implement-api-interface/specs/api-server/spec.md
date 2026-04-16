## ADDED Requirements

### Requirement: API Server Initialization

API 服务器 SHALL 使用 FastAPI 框架构建，提供 HTTP 接口。

#### Scenario: Server starts successfully

- **WHEN** 调用 `uvicorn.run()` 启动服务时
- **THEN** 服务器 SHALL 在配置端口监听请求

#### Scenario: Server loads configuration

- **WHEN** 服务器启动时
- **THEN** SHALL 从环境变量或 Settings 加载配置（host, port, cors_origins）

### Requirement: CORS Configuration

API SHALL 支持跨域请求，允许前端 JavaScript 调用。

#### Scenario: CORS headers in response

- **WHEN** 前端从不同域名发送请求时
- **THEN** 服务器 SHALL 在响应中添加 CORS 头（Access-Control-Allow-Origin）

### Requirement: Health Check Endpoint

API SHALL 提供健康检查端点。

#### Scenario: Health check returns status

- **WHEN** GET /health 请求到达时
- **THEN** 服务器 SHALL 返回 JSON `{"status": "ok"}` 和状态码 200
