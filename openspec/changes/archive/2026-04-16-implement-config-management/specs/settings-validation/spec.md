## ADDED Requirements

### Requirement: Settings Model Validation

配置模型 SHALL 使用 Pydantic 验证配置字段的完整性和类型正确性。

#### Scenario: Settings model accepts valid configuration

- **WHEN** 提供有效的 `OPENAI_API_KEY` 和 `ANTHROPIC_API_KEY` 时
- **THEN** Settings 模型 SHALL 成功创建实例

#### Scenario: Settings model allows partial configuration

- **WHEN** 只提供 `OPENAI_API_KEY` 而不提供 `ANTHROPIC_API_KEY` 时
- **THEN** Settings 模型 SHALL 仍然成功创建实例（API Key 为 None）

#### Scenario: Settings model validates required fields

- **WHEN** 尝试创建一个空的 Settings 实例时
- **THEN** Settings 模型 SHALL 不会抛出异常，因为所有字段都是可选的

### Requirement: Configuration Completeness Check

配置模块 SHALL 提供检查配置完整性的方法。

#### Scenario: Check if OpenAI is configured

- **WHEN** 调用 `settings.is_openai_configured()` 时
- **THEN** 如果 `openai_api_key` 存在且非空，SHALL 返回 `True`

#### Scenario: Check if Anthropic is configured

- **WHEN** 调用 `settings.is_anthropic_configured()` 时
- **THEN** 如果 `anthropic_api_key` 存在且非空，SHALL 返回 `True`
