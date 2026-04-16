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
from src.ai_chat.config import load_config, get_env
from src.ai_chat.settings import Settings

# 加载配置
load_config()

# 创建设置实例
settings = Settings()

# 检查配置
if settings.is_openai_configured():
    print("OpenAI 已配置")

if settings.is_anthropic_configured():
    print("Anthropic 已配置")
```

### LLM 客户端使用

```python
from src.ai_chat.settings import Settings
from src.ai_chat.clients import create_llm_client

# 方式一：使用 Settings 创建客户端
settings = Settings(
    openai_api_key='your-api-key',
    openai_base_url='https://api.minimaxi.com/v1'  # MiniMax
)
client = create_llm_client('openai', settings.openai_api_key, base_url=settings.openai_base_url)

# 发送消息
response = client.send_message("Hello!")
print(response)

# 流式响应
for chunk in client.stream_message("Hello!"):
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
uvicorn src.ai_chat.api.server:app --reload --host 0.0.0.0 --port 8000
```

**说明：**
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
├── src/
│   └── ai_chat/
│       ├── __init__.py
│       ├── config.py      # 配置加载 ✓
│       ├── settings.py    # Pydantic 配置模型 ✓
│       ├── clients/       # LLM 客户端 ✓
│       │   ├── __init__.py
│       │   ├── base.py           # 抽象基类
│       │   ├── openai_client.py  # OpenAI 客户端
│       │   ├── anthropic_client.py # Anthropic 客户端
│       │   └── factory.py        # 客户端工厂
│       └── api/           # Web API 接口 ✓
│           ├── __init__.py
│           ├── server.py        # FastAPI 主入口
│           ├── models.py        # 请求/响应模型
│           └── routes/
│               └── chat.py      # 聊天端点
├── tests/                # 测试文件
├── config/               # 配置文件
├── docs/                 # 文档
├── openspec/             # OpenSpec 工作流
├── pyproject.toml        # 项目配置
├── requirements.txt      # 依赖列表
├── .env.example          # 环境变量模板 ✓
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

- [x] 项目初始化
- [x] 添加 LangChain 依赖
- [x] 配置管理模块 (config.py, settings.py)
- [x] LLM 客户端 (OpenAI, Anthropic, MiniMax)
- [x] Web API 接口 (FastAPI)
- [x] 对话管理
- [ ] CLI 界面
- [ ] 单元测试
- [ ] LangChain Agent
- [ ] RAG 支持
- [ ] 多轮对话记忆
- [ ] 工具调用

## License

MIT
