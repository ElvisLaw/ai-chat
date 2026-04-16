## ADDED Requirements

### Requirement: Chat Completion Endpoint

API SHALL 提供聊天完成接口，接收消息并返回 LLM 响应。

#### Scenario: POST chat with valid request

- **WHEN** POST /chat 收到有效请求 `{"message": "hello"}` 时
- **THEN** SHALL 调用 LLM 客户端并返回 `{"response": "AI 回复内容"}`

#### Scenario: POST chat without message

- **WHEN** POST /chat 收到空消息时
- **THEN** SHALL 返回状态码 400 和错误信息

#### Scenario: POST chat with provider specified

- **WHEN** POST /chat 收到 `{"message": "hi", "provider": "openai"}` 时
- **THEN** SHALL 使用指定提供商的客户端发送请求

### Requirement: Request Validation

API SHALL 验证请求参数的有效性。

#### Scenario: Missing required field

- **WHEN** POST /chat 缺少 `message` 字段时
- **THEN** SHALL 返回 422 Unprocessable Entity 和验证错误详情

### Requirement: Error Handling

API SHALL 妥善处理 LLM 调用错误。

#### Scenario: LLM API returns error

- **WHEN** LLM API 调用失败时
- **THEN** SHALL 返回 500 Internal Server Error 和错误信息（不暴露内部细节）
