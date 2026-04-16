# Claude Code Memory Index

## 项目信息
- [AI Chat项目规划](ai-chat-project-plan.md) — OpenSpec工作流规划、已归档changes、待处理changes、self-improving-agent使用指南

## 技术栈
- Python 3.10+
- OpenAI SDK (openai>=1.0.0)
- Anthropic SDK (anthropic>=0.18.0)
- LangChain (langchain>=0.1.0, langchain-openai>=0.0.5)
- Pydantic (pydantic>=2.0.0)
- python-dotenv (python-dotenv>=1.0.0)
- FastAPI (fastapi>=0.100.0)
- Uvicorn (uvicorn>=0.23.0)

## 项目结构
- 源码: src/ai_chat/
- 测试: tests/
- 配置: config/
- 文档: docs/
- OpenSpec: openspec/

## Git 仓库
- https://github.com/ElvisLaw/ai-chat

## Skills
- self-improving-agent: ~/.claude/skills/self-improving-agent/ & ai-chat/.claude/skills/self-improving-agent/
- find-skills: ~/.claude/skills/find-skills/ & ai-chat/.claude/skills/find-skills/
- OpenSpec 系列: ai-chat/.claude/skills/openspec-*/

## OpenSpec Changes
- 2026-04-16-init-ai-chat-project-structure (archived)
- 2026-04-16-add-langchain-dependency (archived)
- 2026-04-16-implement-config-management (archived)
- 2026-04-16-implement-llm-clients (archived)
- 2026-04-16-implement-api-interface (archived)
- 2026-04-16-implement-conversation-management (archived)
- implement-cli-interface (待实现)
- implement-langchain-agent (待实现)
- implement-rag-support (待实现)
- implement-conversation-memory (待实现)
- implement-tool-calling (待实现)

## 开发习惯
- 每次开发新功能前先创建 OpenSpec change
- 使用 /opsx:propose 创建完整 artifacts
- 实现完成后及时归档 changes
- 使用 self-improving-agent 记录错误和学习
- **每完成一个小需求都要测试一下代码是否可以跑通**
- **每完成一个 OpenSpec change 后更新 memory 文件夹内容**
- **每完成一个 OpenSpec change 后更新 README.md**

## 企业级开发规范

### 代码质量
- 使用 black 格式化代码（`black .`）
- 使用 ruff 检查代码（`ruff check .`）
- 遵循 PEP 8 规范
- 所有公共 API 必须有中文注释

### 测试规范
- 每个模块必须有对应的单元测试
- 测试文件放在 `tests/` 目录
- 使用 pytest 运行测试（`pytest`）
- 测试覆盖率目标：核心业务逻辑 >= 80%

### 安全规范
- **敏感信息绝不能硬编码**（API Key、密码等）
- 使用环境变量或 .env 文件管理配置
- CORS 配置必须限制可信域名
- 用户输入必须验证和清理
- 错误信息不暴露内部实现细节

### 配置管理
- 开发/测试/生产环境分离
- 使用 .env 文件管理本地配置
- 生产环境使用环境变量注入
- 配置默认值应该是安全的

### 日志与监控
- 统一日志格式
- 记录关键操作和错误
- 生产环境必须开启日志

### 错误处理
- 区分业务错误和系统错误
- 统一错误响应格式
- 不暴露敏感信息给用户

### API 设计
- RESTful 风格
- 版本控制（/v1/）
- 统一响应格式
- 限流保护
