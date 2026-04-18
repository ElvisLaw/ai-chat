## MODIFIED Requirements

### Requirement: Conversation Store Contract

系统 SHALL 通过统一的 `ConversationStore` 抽象支持不同的会话存储实现，并向聊天服务、API 和 CLI 暴露一致的会话管理能力。

#### Scenario: Configurable store selection
- **WHEN** 应用根据配置创建会话存储时
- **THEN** 系统 SHALL 通过工厂根据 `CONVERSATION_STORE_TYPE` 选择对应实现
- **AND** `memory` SHALL 解析为内存存储实现
- **AND** `file` SHALL 解析为文件存储实现

#### Scenario: Unknown store type
- **WHEN** 配置了未知的存储类型
- **THEN** 系统 SHALL 返回明确错误，说明可用的存储类型列表

#### Scenario: List conversations through the store contract
- **WHEN** API 或 CLI 请求列出会话时
- **THEN** 存储实现 SHALL 返回 `Conversation` 列表
- **AND** 列表 SHALL 按 `updated_at` 倒序排列

#### Scenario: Delete conversation through the store contract
- **WHEN** API 或 CLI 请求删除指定会话时
- **THEN** 存储实现 SHALL 删除对应会话
- **AND** 删除成功时 SHALL 返回 `True`
- **AND** 会话不存在时 SHALL 返回 `False`

#### Scenario: Persistence-compatible contract
- **WHEN** 聊天服务切换到底层持久化存储实现时
- **THEN** 聊天服务 SHALL 无需修改调用方式即可继续使用 `create`、`get`、`save`、`list` 和 `delete` 接口