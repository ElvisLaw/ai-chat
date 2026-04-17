# AI Chat

一个简单的 AI 聊天应用，支持多种大语言模型。

## 功能特性

- 支持 OpenAI GPT 系列模型 ✓
- 支持 Anthropic Claude 模型 ✓
- 支持 MiniMax API（通过 OpenAI 兼容接口） ✓
- 基于 Pydantic 的配置管理 ✓
- 环境变量配置支持 ✓
- LangChain 集成 ✓
- LLM 客户端统一接口 ✓
- CLI 命令行界面 ✓

## 安装

```bash
# 克隆项目
git clone https://github.com/ElvisLaw/ai-chat.git
cd ai-chat

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows

# 安装项目
pip install -e .
```

## 配置

项目已实现配置管理模块：

1. 复制 `.env.example` 作为模板：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入你的 API keys：
   ```bash
   # OpenAI 配置
   OPENAI_API_KEY=your-openai-api-key

   # Anthropic 配置 (可选)
   ANTHROPIC_API_KEY=your-anthropic-api-key
   ```

### 配置模块使用

```python
from app.settings import get_settings

# 获取 Settings 单例（首次调用自动加载 .env）
settings = get_settings()

# 检查配置
if settings.is_openai_configured():
    print("OpenAI 已配置")

if settings.is_anthropic_configured():
    print("Anthropic 已配置")

# 获取 provider 默认模型
model = settings.get_default_model("openai")   # gpt-4 或全局 MODEL
model = settings.get_default_model("anthropic") # claude-3-sonnet-20240229
```

### LLM 客户端使用

```python
from app.settings import get_settings
from app.clients import create_llm_client

settings = get_settings()

# OpenAI / MiniMax 客户端
client = create_llm_client('openai', settings.openai_api_key, base_url=settings.openai_base_url)

# 发送消息
response = client.send_message([{"role": "user", "content": "Hello!"}])
print(response)

# 流式响应
for chunk in client.stream_message([{"role": "user", "content": "Hello!"}]):
    print(chunk, end='', flush=True)
```

## 启动 API 服务

项目使用 FastAPI 框架构建 Web API，通过 uvicorn 服务器运行。

### 快速启动

```bash
# 进入项目目录
cd ai-chat

# 设置环境变量
export OPENAI_API_KEY=your-api-key
export OPENAI_BASE_URL=https://api.minimaxi.com/v1  # MiniMax API

# 启动服务
fastapi dev
# 或
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

**说明：**
- `fastapi dev` 是 FastAPI CLI 开发模式，自动检测代码变化并热重载
- `uvicorn` 是 ASGI 服务器，用于运行 FastAPI 应用
- `--reload` 开启热更新，代码修改后自动重启
- `--host 0.0.0.0` 允许外部访问
- `--port 8000` 指定端口

### API 访问

- API 地址: http://localhost:8000
- Swagger 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc

### API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/chat` | POST | 同步聊天 |
| `/chat/stream` | POST | 流式 SSE 聊天 |

### 测试 API

```bash
# 健康检查
curl http://localhost:8000/health

# 聊天（同步）
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'

# 聊天（流式）
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

### 前端集成

前端可通过 HTTP 请求调用 API：

```javascript
// 同步请求
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: '你好', provider: 'openai' })
});
const data = await response.json();
console.log(data.response);

// 流式请求 (SSE)
const eventSource = new EventSource('/chat/stream', { method: 'POST' });
// 使用 fetch + ReadableStream 更推荐
```

## CLI 界面

项目提供命令行界面，无需启动 API 服务器即可与 AI 对话。

### 快速开始

```bash
# 安装后直接使用
ai-chat main "你好，AI！"

# 进入交互模式
ai-chat-interactive

# 使用 Anthropic 模型
ai-chat main "Hello" --provider anthropic

# 使用 Agent 模式（可调用工具）
ai-chat main "What's 15 * 23?" --provider agent
```

### CLI 选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `MESSAGE` (main 命令) | 要发送的消息 | - |
| `--provider` | LLM 提供商 (`openai` / `anthropic` / `agent`) | `openai` |
| `--model` | 模型名称 | provider 默认模型 |
| `--stream` | 启用流式输出 | `false` |

### 交互模式命令

在交互模式下可用以下命令：

| 命令 | 说明 |
|------|------|
| `exit` / `quit` / `q` | 退出交互模式 |
| `history` | 显示当前会话历史 |
| `clear` | 清除会话历史 |

### CLI 子命令

```bash
# 发送单条消息
ai-chat main "Hello"

# 进入交互模式
ai-chat-interactive

# 查看历史
ai-chat history

# 清除历史
ai-chat clear
```

### Agent 模式

使用 `--provider agent` 启用 LangChain Agent 模式，AI 可以调用内置工具：

- **calculator**: 数学计算（支持加减乘除、指数、三角函数）
- **datetime**: 获取当前 UTC 时间

示例：
```bash
ai-chat main "What's (2 + 3) * 10?" --provider agent
ai-chat main "What time is it now?" --provider agent --stream
```

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black .
ruff check .
```

## 项目结构

```
ai-chat/
├── app/                   # 应用代码
│   ├── __init__.py
│   ├── config.py           # 配置加载（简化版）
│   ├── settings.py         # Pydantic Settings 单例（get_settings）
│   ├── clients/            # LLM 客户端 ✓
│   │   ├── __init__.py
│   │   ├── base.py              # 抽象基类
│   │   ├── openai_client.py     # OpenAI / MiniMax 客户端
│   │   └── anthropic_client.py  # Anthropic 客户端
│   ├── conversation/       # 对话管理 ✓
│   │   ├── __init__.py
│   │   ├── models.py            # 消息模型（Role, Conversation）
│   │   ├── store.py             # 会话存储（InMemoryConversationStore）
│   │   └── service.py           # 聊天服务（async + asyncio.to_thread）
│   ├── api/              # Web API ✓
│   │   ├── __init__.py
│   │   ├── server.py            # FastAPI 主入口（lifespan 管理资源）
│   │   ├── dependencies.py       # DI 依赖函数
│   │   ├── models.py            # 请求/响应模型
│   │   └── routes/
│   │       ├── chat.py          # 聊天端点
│   │       └── rag.py           # RAG 端点
│   ├── cli/               # CLI 界面 ✓
│   │   ├── __init__.py
│   │   ├── main.py              # Typer 主入口
│   │   ├── factory.py           # LLM 客户端工厂
│   │   └── rag.py              # RAG CLI 命令
│   ├── agent/             # LangChain Agent ✓
│   │   ├── __init__.py
│   │   ├── client.py            # Agent 客户端
│   │   ├── factory.py           # Agent 工厂函数
│   │   ├── service.py          # Agent 服务封装
│   │   └── tools.py           # 内置工具集
│   └── rag/                # RAG 模块 ✓
│       ├── __init__.py
│       ├── loader.py           # 文档加载器
│       ├── splitter.py         # 文本分割器
│       ├── store.py           # 向量存储
│       ├── retriever.py       # 检索器
│       └── service.py         # RAG 服务
├── tests/                 # 测试文件 ✓
├── main.py                # FastAPI 入口点
├── openspec/              # OpenSpec 工作流
├── pyproject.toml         # 项目配置
├── requirements.txt       # 依赖列表
├── .env.example           # 环境变量模板 ✓
└── README.md
```

## 依赖

- **openai**: OpenAI GPT 模型接口
- **anthropic**: Anthropic Claude 模型接口
- **python-dotenv**: 环境变量管理
- **pydantic**: 数据验证
- **langchain**: AI 应用开发框架
- **langchain-openai**: LangChain OpenAI 集成
- **fastapi**: Web API 框架
- **uvicorn**: ASGI 服务器

## 开发进度

查看已完成变更：https://github.com/ElvisLaw/ai-chat/tree/main/openspec/changes/archive

查看待处理功能计划：[ai-chat-project-plan.md](.claude/memory/ai-chat-project-plan.md)

## License

MIT
