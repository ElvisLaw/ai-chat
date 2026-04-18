## ADDED Requirements

### Requirement: Memory Buffer

系统 SHALL 提供对话消息缓冲功能，管理长对话的生命周期。

#### Scenario: Buffer initialization
- **WHEN** 对话服务初始化时
- **THEN** 系统 SHALL 创建一个空的内存缓冲

#### Scenario: Message addition
- **WHEN** 用户发送消息时
- **THEN** 系统 SHALL 将消息添加到对话缓冲的末尾

#### Scenario: Buffer size limit
- **WHEN** 对话消息数量超过配置的缓冲上限（默认 20 条）
- **THEN** 系统 SHALL 自动删除最旧的消息（保留系统消息）

#### Scenario: Token limit exceeded
- **WHEN** 对话的总 Token 数超过配置的 Token 上限（默认 4000 tokens）
- **THEN** 系统 SHALL 删除最早的 user 消息直到满足 Token 限制

#### Scenario: Get recent messages
- **WHEN** 需要获取对话历史时
- **THEN** 系统 SHALL 返回缓冲中的所有消息（按顺序）
