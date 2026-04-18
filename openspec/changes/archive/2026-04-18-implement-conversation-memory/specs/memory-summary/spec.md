## ADDED Requirements

### Requirement: Memory Summary

系统 SHALL 提供对话摘要功能，在长对话场景下保留关键信息。

#### Scenario: Auto summary trigger
- **WHEN** 对话消息数超过摘要阈值（默认 15 条）且总 Token 数超过 3000
- **AND** 对话尚未被摘要过
- **THEN** 系统 SHALL 调用 LLM 生成对话摘要

#### Scenario: Summary preservation
- **WHEN** 对话被摘要后
- **THEN** 系统 SHALL 将摘要保存为对话的第一条消息（role: system）
- **AND** 系统 SHALL 标记该对话已摘要，防止重复摘要

#### Scenario: Summary format
- **WHEN** 系统生成摘要时
- **THEN** 摘要 SHALL 包含对话的核心主题、用户目标和关键结论
- **AND** 摘要长度 SHALL 不超过 500 字

#### Scenario: Summary content
- **WHEN** 需要重建对话上下文时
- **THEN** 系统 SHALL 返回摘要 + 最近的消息（保留最新 5 条以维持上下文）

#### Scenario: Subsequent summarization
- **WHEN** 已摘要的对话新增消息再次触发摘要条件时
- **THEN** 系统 SHALL 基于原始摘要 + 新消息生成增量摘要
- **AND** 系统 SHALL 替换而非追加摘要
