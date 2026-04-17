## Why

当前配置加载存在时序问题：

1. `server.py:42` 在 `create_app()` 时读取 `CORS_ORIGINS`
2. `server.py:23` 在 lifespan 中才执行 `load_config()`
3. `server.py:70` 默认 `app` 在模块导入时就创建

这导致 `.env` 中的 `CORS_ORIGINS`、`API_HOST`、`API_PORT` 可能根本没生效，因为 load_config() 还没被调用。

## What Changes

- 统一配置入口：使用 Settings 单例，在第一次访问时自动加载 .env
- 移除单独的 `load_config()` 调用（改为自动加载）
- 移除 `create_app()` 中的 `os.getenv` 调用，改用 Settings 属性
- 确保应用创建前配置已加载

## Capabilities

### Modified Capabilities

- `settings`: 改为单例模式，模块导入时自动加载配置
- `server`: 改用 Settings 获取配置，移除手动 load_config 调用

## Impact

- 修改 `src/ai_chat/settings.py` — 单例模式
- 修改 `src/ai_chat/api/server.py` — 使用 Settings 获取配置
