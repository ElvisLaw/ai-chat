# AI Chat

一个简单的 AI 聊天应用，支持多种大语言模型。

## 功能特性

- 支持 OpenAI GPT 系列模型
- 支持 Anthropic Claude 模型
- 基于 Pydantic 的配置管理
- 环境变量配置支持

## 安装

```bash
# 克隆项目
git clone <repository-url>
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

在项目根目录创建 `.env` 文件：

```bash
# OpenAI 配置
OPENAI_API_KEY=your-api-key

# Anthropic 配置 (可选)
ANTHROPIC_API_KEY=your-api-key
```

## 使用

```bash
# 运行聊天应用
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
│   └── ai_chat/      # 主包
├── tests/            # 测试文件
├── config/           # 配置文件
├── docs/             # 文档
├── pyproject.toml    # 项目配置
└── README.md
```

## 依赖

- **openai**: OpenAI GPT 模型接口
- **anthropic**: Anthropic Claude 模型接口
- **python-dotenv**: 环境变量管理
- **pydantic**: 数据验证

## License

MIT
