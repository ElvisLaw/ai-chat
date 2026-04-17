## Why

当前默认模型选择逻辑存在多个问题：
1. `settings.py` 中 `model` 是全局默认值 `gpt-4`
2. `chat()` 方法有默认模型逻辑，但 `stream()` 方法没有
3. Anthropic provider 也被错误地默认成 `gpt-4`
4. 应该按 provider 维度设置默认模型

## What Changes

- 修改 `Settings` 类，按 provider 维度定义默认模型
- 修改 `ChatService` 的 `chat()` 和 `stream()` 方法，统一使用 provider 默认模型
- 移除全局 `MODEL` 配置，改用 provider-specific 配置

## Capabilities

### Modified Capabilities

- `settings`: 改为按 provider 定义默认模型
- `chat-service`: 统一获取 provider 默认模型逻辑

## Impact

- 修改 `src/ai_chat/settings.py` — 默认模型配置
- 修改 `src/ai_chat/conversation/service.py` — 获取默认模型的逻辑
