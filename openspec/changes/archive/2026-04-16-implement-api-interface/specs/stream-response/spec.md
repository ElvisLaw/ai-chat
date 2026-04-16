## ADDED Requirements

### Requirement: Streaming Chat Endpoint

API SHALL 提供流式聊天端点，通过 SSE 返回响应。

#### Scenario: POST chat/stream with valid request

- **WHEN** POST /chat/stream 收到有效请求时
- **THEN** SHALL 返回 SSE 流，逐步发送响应内容

#### Scenario: SSE format

- **WHEN** 流式响应发送数据块时
- **THEN** SHALL 使用格式 `data: <content>\n\n`

#### Scenario: Stream completion

- **WHEN** 响应内容发送完毕后
- **THEN** SHALL 发送 `data: [DONE]\n\n` 表示结束

### Requirement: Streaming Error Handling

流式接口 SHALL 妥善处理错误。

#### Scenario: Stream interrupted by error

- **WHEN** 流式响应过程中 LLM API 报错时
- **THEN** SHALL 发送错误信息后关闭流，不中断连接
