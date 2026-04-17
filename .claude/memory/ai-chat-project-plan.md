---
name: ai-chat-project-plan
description: AI Chat Python项目OpenSpec工作流规划
type: project
originSessionId: fc845397-edf5-4bb1-b74a-b4db1e5a3c41
---

## AI Chat 项目 OpenSpec 工作流

> 已归档 Changes 查看：`openspec list` 或访问 [openspec/changes/archive/](openspec/changes/archive/)

---

### 待处理 Changes（按优先级）

#### 1. implement-rag-support
RAG（检索增强生成）支持

**Capabilities:**
- `document-loader`: 文档加载器
- `text-splitter`: 文本分割器
- `vector-store`: 向量存储
- `retriever`: 检索器

**Note:** CLI 使用流程待单独设计（见 design-rag-cli-ux）

---

#### 2. design-rag-cli-ux
RAG CLI 使用流程设计（独立命令 vs 交互模式）

**待明确：**
- `rag upload` / `rag query` / `rag clear` 独立命令
- `rag-interactive` 交互模式
- 文档持久化策略

---

#### 3. implement-conversation-memory
多轮对话记忆

**Capabilities:**
- `memory-buffer`: 对话缓冲
- `memory-summary`: 对话摘要
- `memory-persistence`: 记忆持久化

---

#### 4. implement-tool-calling
工具调用功能

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
├── app/                   # 主包（FastAPI 推荐布局）
│   ├── __init__.py
│   ├── config.py          # 配置加载
│   ├── settings.py         # Pydantic Settings 单例
│   ├── clients/            # LLM 客户端
│   │   ├── __init__.py
│   │   ├── base.py              # 抽象基类
│   │   ├── openai_client.py     # OpenAI 客户端
│   │   ├── anthropic_client.py  # Anthropic 客户端
│   │   └── factory.py           # 客户端工厂
│   ├── conversation/       # 对话管理
│   │   ├── __init__.py
│   │   ├── models.py            # 消息模型
│   │   ├── store.py             # 会话存储
│   │   └── service.py          # 聊天服务
│   ├── api/              # Web API
│   │   ├── __init__.py
│   │   ├── server.py            # FastAPI 主入口
│   │   ├── dependencies.py      # DI 依赖函数
│   │   ├── models.py            # 请求/响应模型
│   │   └── routes/
│   │       ├── chat.py          # 聊天端点
│   │       └── rag.py          # RAG 端点
│   ├── cli/               # CLI 界面
│   │   ├── __init__.py
│   │   ├── main.py              # Typer 主入口
│   │   ├── factory.py           # LLM 客户端工厂
│   │   └── rag.py              # RAG CLI 命令
│   ├── agent/             # LangChain Agent
│   │   ├── __init__.py
│   │   ├── client.py            # Agent 客户端
│   │   ├── factory.py           # Agent 工厂函数
│   │   ├── service.py          # Agent 服务封装
│   │   └── tools.py           # 内置工具集
│   └── rag/                # RAG 模块
│       ├── __init__.py
│       ├── loader.py           # 文档加载器
│       ├── splitter.py         # 文本分割器
│       ├── store.py           # 向量存储
│       ├── retriever.py       # 检索器
│       └── service.py         # RAG 服务
├── tests/                # 测试目录
├── main.py              # FastAPI 入口点
├── openspec/             # OpenSpec 工作流
├── pyproject.toml        # 项目配置
├── requirements.txt      # 依赖列表
├── .env.example          # 环境变量模板
└── README.md
```

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
