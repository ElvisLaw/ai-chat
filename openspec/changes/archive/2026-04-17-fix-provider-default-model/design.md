## Context

当前默认模型配置：
- `Settings.model` = "gpt-4" (全局默认值)
- `ChatService.chat()` 使用 `Settings().model` 作为默认值
- `ChatService.stream()` 没有默认模型逻辑 (BUG)

## Goals / Non-Goals

**Goals:**
- 修复 stream() 缺少默认模型的问题
- 按 provider 维度设置默认模型
- 保持向后兼容

**Non-Goals:**
- 不改变 API 接口
- 不添加新的环境变量

## Decisions

### 方案：Provider-specific 默认模型

**决定**：在 Settings 中按 provider 定义默认模型。

```python
# settings.py
DEFAULT_MODELS = {
    "openai": "gpt-4",
    "anthropic": "claude-3-sonnet-20240229",
}

def get_default_model(self, provider: str) -> str:
    """获取 provider 的默认模型。"""
    return self.model or self.DEFAULT_MODELS.get(provider, "gpt-4")
```

**理由**：
- 清晰：每个 provider 有明确的默认值
- 安全：Anthropic 不会被错误地设为 gpt-4
- 一致：chat() 和 stream() 使用相同逻辑

## Risks / Trade-offs

无显著风险。这是纯粹的 bug 修复。
