# AI Chat

一个简单的 AI 聊天应用，支持多种大语言模型。

## 功能特性

- 支持 OpenAI GPT 系列模型
- 支持 Anthropic Claude 模型
- 基于 Pydantic 的配置管理 ✓
- 环境变量配置支持 ✓
- LangChain 集成 ✓

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

## 使用

```bash
# 运行聊天应用 (待实现)
python -m ai_chat
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
│       └── settings.py   # Pydantic 配置模型 ✓
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

## 开发进度

- [x] 项目初始化
- [x] 添加 LangChain 依赖
- [x] 配置管理模块 (config.py, settings.py)
- [ ] LLM 客户端
- [ ] 对话管理
- [ ] CLI 界面
- [ ] 单元测试

## License

MIT
