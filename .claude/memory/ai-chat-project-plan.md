---
name: ai-chat-project-plan
description: AI Chat Python项目OpenSpec工作流规划
type: project
originSessionId: fc845397-edf5-4bb1-b74a-b4db1e5a3c41
---

## AI Chat 项目 OpenSpec 工作流

### 已归档 Changes

| Change | Schema | Status | 描述 |
|--------|--------|--------|------|
| `2026-04-16-init-ai-chat-project-structure` | spec-driven | ✓ archived | 项目初始化、目录结构、基础依赖 |
| `2026-04-16-add-langchain-dependency` | spec-driven | ✓ archived | 添加 LangChain 依赖 |
| `2026-04-16-implement-config-management` | spec-driven | ✓ archived | config.py, settings.py, .env.example |
| `2026-04-16-implement-llm-clients` | spec-driven | ✓ archived | LLM 客户端（OpenAI/Anthropic/MiniMax） |
| `2026-04-16-implement-api-interface` | spec-driven | ✓ archived | FastAPI Web API 接口（/health, /chat, /chat/stream） |
| `2026-04-16-implement-conversation-management` | spec-driven | ✓ archived | 多轮对话管理（message-models, conversation-history, chat-service） |

---

### 待处理 Changes（按优先级）

#### Change 6: implement-cli-interface
**Schema:** spec-driven
**描述:** 实现 CLI 命令行界面

**Capabilities:**
- `cli-entry`: 命令行入口
- `model-selection`: 模型选择
- `streaming-output`: 流式输出
- `history-commands`: 对话历史命令

---

#### Change 7: implement-langchain-agent
**Schema:** spec-driven
**描述:** LangChain Agent 支持

**Capabilities:**
- `agent-core`: Agent 核心实现
- `agent-tools`: 内置工具集
- `agent-chain`: 工具链配置

---

#### Change 8: implement-rag-support
**Schema:** spec-driven
**描述:** RAG（检索增强生成）支持

**Capabilities:**
- `document-loader`: 文档加载器
- `text-splitter`: 文本分割器
- `vector-store`: 向量存储
- `retriever`: 检索器

---

#### Change 9: implement-conversation-memory
**Schema:** spec-driven
**描述:** 多轮对话记忆

**Capabilities:**
- `memory-buffer`: 对话缓冲
- `memory-summary`: 对话摘要
- `memory-persistence`: 记忆持久化

---

#### Change 10: implement-tool-calling
**Schema:** spec-driven
**描述:** 工具调用功能

**Capabilities:**
- `tool-registry`: 工具注册表
- `tool-executor`: 工具执行器
- `tool-definitions`: 工具定义规范

---

### 当前项目状态

**Dependencies (pyproject.toml):**
- openai>=1.0.0
- anthropic>=0.18.0
- python-dotenv>=1.0.0
- pydantic>=2.0.0
- langchain>=0.1.0
- langchain-openai>=0.0.5
- fastapi>=0.100.0
- uvicorn>=0.23.0

**Project Structure:**
```
ai-chat/
├── src/ai_chat/     # 主包
│   ├── __init__.py
│   ├── config.py    # 配置加载 ✓
│   ├── settings.py  # Pydantic 模型 ✓
│   ├── clients/     # LLM 客户端 ✓
│   │   ├── __init__.py
│   │   ├── base.py           # 抽象基类
│   │   ├── openai_client.py  # OpenAI 客户端
│   │   ├── anthropic_client.py # Anthropic 客户端
│   │   └── factory.py        # 客户端工厂
│   ├── conversation/  # 对话管理 ✓
│   │   ├── __init__.py
│   │   ├── models.py         # 消息模型
│   │   ├── store.py          # 会话存储
│   │   └── service.py        # 聊天服务
│   └── api/          # Web API ✓
├── tests/           # 测试目录
├── config/          # 配置目录
├── docs/            # 文档目录
├── openspec/        # OpenSpec 工作流
├── pyproject.toml   # 项目配置
├── requirements.txt # 依赖列表
├── .gitignore
├── .env.example     # 环境变量模板 ✓
└── README.md
```

---

### 下一步建议

使用 `/opsx:new` 开始实现 implement-conversation-management

---

### self-improving-agent 使用指南

**安装位置:** `~/.claude/skills/self-improving-agent/`

**触发时机（在项目开发中）：**
1. 命令或操作意外失败时
2. 用户纠正 Claude（"不对，应该是..."）
3. 用户请求不存在的功能
4. 外部 API 或工具失败
5. Claude 发现知识过时或有误
6. 发现更好的方法解决反复出现的任务

**使用方式:**
- 在遇到错误或用户纠正时，主动调用 self-improving-agent
- 将错误、纠正和学习记录到 `.learnings/` 目录
- 定期回顾 `.learnings/` 内容，避免重复犯错

**注意事项:**
- 项目内和全局都安装了 self-improving-agent
- 全局安装路径: `~/.claude/skills/self-improving-agent/`
- 项目安装路径: `ai-chat/.claude/skills/self-improving-agent/`
