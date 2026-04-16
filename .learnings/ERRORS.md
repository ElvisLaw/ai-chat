# Errors Log

## [ERR-20260416-001] pydantic_import

**Logged**: 2026-04-16T21:25:00+08:00
**Priority**: high
**Status**: resolved
**Area**: config

### Summary
`from pydantic import BaseSettings` 报错，BaseSettings 已迁移到 pydantic-settings

### Error
```
pydantic.errors.PydanticImportError: `BaseSettings` has been moved to the `pydantic-settings` package. See https://docs.pydantic.dev/2.13/migration/#basesettings-has-moved-to-pydantic-settings for more details.
```

### Context
- 操作：运行 Python 代码导入 Settings 类
- 环境：Pydantic 2.13.1，Python 3.13

### Suggested Fix
1. 安装：`pip install pydantic-settings`
2. 修改导入语句

### Resolution
- **Resolved**: 2026-04-16T21:30:00+08:00
- **Commit**: 手动修复
- **Notes**: 使用 `from pydantic_settings import BaseSettings, SettingsConfigDict`

---

## [ERR-20260416-002] settings_env_not_loaded

**Logged**: 2026-04-16T21:35:00+08:00
**Priority**: high
**Status**: resolved
**Area**: config

### Summary
Settings 类创建后 openai_api_key 为 None，无法读取 .env 文件

### Error
```
Settings(openai_api_key=None)
```

### Context
- 操作：创建 Settings 实例并检查 openai_api_key
- 原因：使用 Field 的 env 参数在 Pydantic v2 中需要使用 validation_alias

### Suggested Fix
使用 `validation_alias` 替代 Field 中的 `env` 参数

### Resolution
- **Resolved**: 2026-04-16T21:40:00+08:00
- **Notes**: 修改 Field 定义使用 validation_alias="ENV_VAR_NAME"

---

## [ERR-20260416-003] llm_unknown_model

**Logged**: 2026-04-16T21:45:00+08:00
**Priority**: high
**Status**: resolved
**Area**: backend

### Summary
调用 MiniMax API 时 model 参数为空导致 400 错误

### Error
```
'error': {'type': 'bad_request_error', 'message': "invalid params, unknown model '' (2013)"}
```

### Context
- 操作：POST /chat 端点
- 原因：model 参数为 None 时没有使用默认模型

### Suggested Fix
在 ChatService 调用 LLM 前，检查 model 是否为 None，如果是则使用 Settings().model

### Resolution
- **Resolved**: 2026-04-16T21:50:00+08:00
- **Notes**: 在 service.py 中添加默认模型逻辑

---
