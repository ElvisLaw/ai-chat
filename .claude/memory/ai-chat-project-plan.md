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

---

### 已完成 Changes

| Change | Schema | Status | 描述 |
|--------|--------|--------|------|
| `implement-config-management` | spec-driven | ✓ complete | config.py, settings.py, .env.example |

---

### 待处理 Changes（按优先级）

#### Change 2: implement-llm-clients（推荐下一步）
**Schema:** spec-driven
**描述:** 实现 LLM 客户端（OpenAI/Claude）

**Capabilities:**
- `llm-client-base`: 客户端基类
- `openai-client`: OpenAI 实现
- `anthropic-client`: Claude 实现
- `client-registry`: 客户端工厂

---

#### Change 2: implement-llm-clients
**Schema:** spec-driven
**描述:** 实现 LLM 客户端（OpenAI/Claude）

**Capabilities:**
- `llm-client-base`: 客户端基类
- `openai-client`: OpenAI 实现
- `anthropic-client`: Claude 实现
- `client-registry`: 客户端工厂

**Tasks:**
- [ ] 2.1 创建 src/ai_chat/clients/base.py
- [ ] 2.2 创建 src/ai_chat/clients/openai_client.py
- [ ] 2.3 创建 src/ai_chat/clients/anthropic_client.py
- [ ] 2.4 创建 src/ai_chat/clients/registry.py

---

#### Change 3: implement-conversation-management
**Schema:** spec-driven
**描述:** 实现对话管理模块

**Capabilities:**
- `message-models`: 消息模型
- `conversation-history`: 对话历史管理
- `chat-service`: 聊天服务主类

**Tasks:**
- [ ] 3.1 创建 src/ai_chat/messages.py
- [ ] 3.2 创建 src/ai_chat/conversation.py
- [ ] 3.3 创建 src/ai_chat/chat.py

---

#### Change 4: implement-cli-interface
**Schema:** spec-driven
**描述:** 实现 CLI 命令行界面

**Capabilities:**
- `cli-entry`: 命令行入口
- `model-selection`: 模型选择
- `streaming-output`: 流式输出
- `history-commands`: 对话历史命令

---

#### Change 5: implement-advanced-features（可选）
**Schema:** spec-driven
**描述:** 高级功能

**Capabilities:**
- `langchain-agent`: LangChain Agent 支持
- `rag-support`: RAG 支持
- `conversation-memory`: 多轮对话记忆
- `tool-calling`: 工具调用

---

### 当前项目状态

**Dependencies (pyproject.toml):**
- openai>=1.0.0
- anthropic>=0.18.0
- python-dotenv>=1.0.0
- pydantic>=2.0.0
- langchain>=0.1.0
- langchain-openai>=0.0.5

**Project Structure:**
```
ai-chat/
├── src/ai_chat/     # 主包
│   ├── __init__.py
│   ├── config.py    # 配置加载 ✓
│   └── settings.py  # Pydantic 模型 ✓
├── tests/           # 测试目录
├── config/          # 配置目录
├── docs/            # 文档目录
├── pyproject.toml   # 项目配置
├── requirements.txt # 依赖列表
├── .gitignore
├── .env.example     # 环境变量模板 ✓
└── README.md
```

---

### 下一步建议

使用 `/opsx:propose implement-llm-clients` 实现 LLM 客户端

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
