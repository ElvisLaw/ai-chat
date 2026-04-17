# Settings Singleton

## Overview

统一配置入口，确保配置在应用创建前已加载。

## Interface

### get_settings()

```python
def get_settings() -> Settings:
    """获取 Settings 单例。

    首次调用时自动加载 .env 文件，之后返回同一实例。

    Returns:
        Settings 单例。
    """
```

### Settings 扩展字段

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `cors_origins` | `str \| list` | `"*"` | CORS 允许的源 |
| `api_host` | `str` | `"0.0.0.0"` | API 服务地址 |
| `api_port` | `int` | `8000` | API 服务端口 |
