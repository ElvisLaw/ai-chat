## Context

当前配置加载流程：
```
模块导入 → create_app() → lifespan 启动 → load_config()
                ↑
        此时 os.getenv 还没 .env 的值
```

## Goals / Non-Goals

**Goals:**
- 配置在应用创建前已加载
- 所有配置通过 Settings 统一访问
- 移除手动 load_config() 调用

**Non-Goals:**
- 不改变 Settings 的字段定义
- 不添加新配置项

## Decisions

### 方案：Settings 单例 + 自动加载

**决定**：使用 Python 模块级单例，模块导入时自动加载。

```python
# settings.py
_settings_instance = None

def get_settings() -> Settings:
    """获取 Settings 单例（自动加载 .env）。"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
```

**server.py 改进**：
```python
from ..settings import get_settings

def create_app() -> FastAPI:
    settings = get_settings()  # 此时 .env 已加载
    cors_origins = settings.cors_origins  # 替代 os.getenv
```

## Risks / Trade-offs

无显著风险。配置加载是幂等的，早加载比晚加载更安全。
