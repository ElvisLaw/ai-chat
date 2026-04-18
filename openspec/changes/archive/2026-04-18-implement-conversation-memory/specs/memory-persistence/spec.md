## ADDED Requirements

### Requirement: Memory Persistence

系统 SHALL 提供对话历史的持久化存储，支持跨服务重启恢复。

#### Scenario: Conversation save
- **WHEN** 对话发生变更（新增消息）时
- **THEN** 系统 SHALL 将对话序列化为 JSON 并保存到磁盘

#### Scenario: Conversation load
- **WHEN** 服务启动时
- **THEN** 系统 SHALL 从磁盘恢复最近对话的状态
- **AND** 系统 SHALL 在首次加载历史会话时按需加载

#### Scenario: Storage location
- **WHEN** 系统需要持久化对话时
- **THEN** 系统 SHALL 使用 `~/.ai-chat/conversations/` 目录存储

#### Scenario: Conversation file naming
- **WHEN** 保存对话时
- **THEN** 文件名 SHALL 使用 `{conversation_id}.json` 格式

#### Scenario: Conversation delete
- **WHEN** 用户删除对话时
- **THEN** 系统 SHALL 删除对应的持久化文件

#### Scenario: Empty directory handling
- **WHEN** 持久化目录不存在时
- **THEN** 系统 SHALL 自动创建目录结构

#### Scenario: List conversations
- **WHEN** 用户请求查看会话列表时
- **THEN** 系统 SHALL 列出所有持久化的对话文件（按最后修改时间倒序）

#### Scenario: Persistence failure handling
- **WHEN** 持久化操作失败时
- **THEN** 系统 SHALL 记录错误但不影响内存中的对话运行
- **AND** 系统 SHALL 在下次消息到来时重试持久化
