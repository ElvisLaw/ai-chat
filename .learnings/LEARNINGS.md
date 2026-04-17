# Learnings Log

## [LRN-20260416-001] best_practice

**Logged**: 2026-04-16T21:30:00+08:00
**Priority**: high
**Status**: pending
**Area**: config

### Summary
Pydantic v2 中 BaseSettings 已迁移到 pydantic-settings 包

### Details
在实现对话管理功能时，发现 `from pydantic import BaseSettings` 会报错：`PydanticImportError: BaseSettings has been moved to the pydantic-settings package`。

Pydantic v2 (2.13+) 将 BaseSettings 从主包移除了。需要安装 pydantic-settings 并从 pydantic_settings 导入。

### Suggested Action
1. 安装依赖：`pip install pydantic-settings`
2. 修改导入：`from pydantic_settings import BaseSettings, SettingsConfigDict`
3. 使用 `validation_alias` 而非 `env` 在 Field 中指定环境变量

### Metadata
- Source: error
- Related Files: app/settings.py
- Tags: pydantic, settings, migration

---

## [LRN-20260416-002] best_practice

**Logged**: 2026-04-16T21:35:00+08:00
**Priority**: high
**Status**: pending
**Area**: openspec

### Summary
OpenSpec 流程缺少端到端集成验证步骤

### Details
在 implement-conversation-management 流程中，实现了完整的功能代码，但部署后发现：
1. Settings 类无法读取环境变量（因为没安装 pydantic-settings）
2. LLM 客户端不支持多轮对话参数 conversation_messages
3. API 端点调用时 model 参数为空导致 400 错误

这些都是因为 OpenSpec 流程只关注新功能本身，忽略了现有组件的兼容性验证。

### Suggested Action
在 OpenSpec tasks.md 中增加"集成验证"环节：
```markdown
## 7. 集成验证
- [ ] 7.1 启动服务验证 /health 端点
- [ ] 7.2 测试 /chat 端点单轮对话
- [ ] 7.3 测试多轮对话（使用 conversation_id）
- [ ] 7.4 验证 Settings 能正确读取环境变量
- [ ] 7.5 验证 LLM 客户端支持新参数
```

### Metadata
- Source: conversation
- Related Files: openspec/changes/implement-conversation-management/tasks.md
- Tags: openspec, integration, testing

---

## [LRN-20260416-003] best_practice

**Logged**: 2026-04-16T21:40:00+08:00
**Priority**: medium
**Status**: pending
**Area**: backend

### Summary
LLM 客户端接口变更需要支持多轮对话上下文

### Details
在实现多轮对话时，需要将历史消息传递给 LLM 客户端。原 OpenAI 和 Anthropic 客户端只支持单条消息，需要扩展支持 conversation_messages 参数。

解决方案：在 send_message 和 stream_message 中增加 conversation_messages 参数，用于传递历史对话上下文。

### Suggested Action
未来修改 LLM 客户端时，确保接口设计考虑到多轮对话场景。可以在设计阶段就明确接口参数。

### Metadata
- Source: error
- Related Files: app/clients/openai_client.py, app/clients/anthropic_client.py
- Tags: llm, multi-turn, conversation

---
