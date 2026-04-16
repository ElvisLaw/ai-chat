## Why

配置管理是 AI Chat 应用的基础设施。合理的配置管理可以：
- 集中管理 API keys 和敏感信息
- 支持多环境配置（开发、测试、生产）
- 通过 Pydantic 实现配置验证，确保类型安全

## What Changes

- 创建 `src/ai_chat/config.py` - 环境变量加载和配置管理
- 创建 `src/ai_chat/settings.py` - Pydantic 配置模型，验证配置完整性
- 创建 `.env.example` - API Key 模板文件，方便开发者快速配置

## Capabilities

### New Capabilities
- `config-management`: 环境变量加载和配置管理
- `settings-validation`: Pydantic 模型验证配置完整性

## Impact

- `src/ai_chat/config.py`: 新增配置加载模块
- `src/ai_chat/settings.py`: 新增配置验证模型
- `.env.example`: 新增环境变量模板
