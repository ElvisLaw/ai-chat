## Context

我们正在为 AI Chat 项目实现配置管理模块。项目使用 Python，需要集中管理 API keys（OpenAI、Anthropic 等）并支持多环境配置。

当前状态：
- 项目结构已初始化
- 依赖已声明在 pyproject.toml 中
- 尚未有统一的配置管理机制

## Goals / Non-Goals

**Goals:**
- 提供安全的环境变量加载机制
- 使用 Pydantic 验证配置完整性
- 支持多 LLM 提供商（OpenAI、Anthropic）
- 配置与代码分离，便于管理敏感信息

**Non-Goals:**
- 不实现数据库配置（本项目暂无数据库）
- 不实现复杂的配置热重载
- 不实现多环境切换（dev/staging/prod）的自动化机制

## Decisions

### Decision 1: 使用 python-dotenv 加载 .env 文件

**选择：** `python-dotenv` 库

**原因：**
- 业界标准，成熟稳定
- 与 python-dotenv>=1.0.0 依赖一致
- 自动加载 .env 文件到环境变量

**替代方案：**
- 手动 os.environ 读取：繁琐，不支持 .env 文件
- pydantic-settings 内置支持：功能类似但本项目已依赖 python-dotenv

### Decision 2: 使用 Pydantic BaseSettings 进行配置验证

**选择：** Pydantic v2 的 `BaseModel` + 手动环境变量读取

**原因：**
- 类型安全，IDE 支持好
- 可以定义字段验证器
- 与已安装的 pydantic>=2.0.0 一致

**替代方案：**
- 使用 pydantic-settings：需要额外依赖
- 使用 dataclasses：验证功能较弱

### Decision 3: API Key 字段设计

**设计：**
```python
openai_api_key: str | None = None  # 可选，允许部分配置
anthropic_api_key: str | None = None
```

**原因：**
- 允许用户只配置部分 LLM 的 API Key
- 未配置时系统可以给出友好提示

## Risks / Trade-offs

- **风险**：.env 文件可能遗漏在 .gitignore 中导致 API Key 泄露
  - **缓解**：项目已有完整的 .gitignore，已排除 .env 文件

- **风险**：配置验证失败时错误信息不清晰
  - **缓解**：在 Settings 类中提供自定义错误消息
