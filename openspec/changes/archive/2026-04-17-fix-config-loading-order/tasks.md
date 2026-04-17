## 1. 修改 Settings

- [x] 1.1 添加 `get_settings()` 单例函数
- [x] 1.2 添加 `cors_origins` 配置字段
- [x] 1.3 添加 `api_host` 和 `api_port` 配置字段

## 2. 修改 server.py

- [x] 2.1 使用 `get_settings()` 获取配置
- [x] 2.2 移除 `os.getenv` 调用
- [x] 2.3 移除 lifespan 中的 `load_config()` 调用
- [x] 2.4 移除 `create_app()` 中的 `load_config` 导入

## 3. 集成验证

- [x] 3.1 验证 .env 中配置的 CORS_ORIGINS 生效
- [x] 3.2 验证 .env 中配置的 API_HOST/API_PORT 生效
- [x] 3.3 验证模块导入时配置已加载
