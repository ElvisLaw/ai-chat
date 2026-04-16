## ADDED Requirements

### Requirement: Environment Variable Loading

配置模块 SHALL 从 `.env` 文件加载环境变量，并将其注入到 Python 的 `os.environ` 中。

#### Scenario: Load .env file on initialization

- **WHEN** 配置模块被导入并初始化时
- **THEN** 系统 SHALL 自动查找并加载项目根目录下的 `.env` 文件

#### Scenario: Environment variables accessible after loading

- **WHEN** `.env` 文件包含 `OPENAI_API_KEY=test-key` 时
- **THEN** `os.environ.get("OPENAI_API_KEY")` SHALL 返回 `"test-key"`

### Requirement: API Key Access

配置模块 SHALL 提供对 API keys 的访问接口。

#### Scenario: Get OpenAI API key

- **WHEN** 应用请求 `openai_api_key` 时
- **THEN** 配置模块 SHALL 返回环境变量 `OPENAI_API_KEY` 的值

#### Scenario: Get Anthropic API key

- **WHEN** 应用请求 `anthropic_api_key` 时
- **THEN** 配置模块 SHALL 返回环境变量 `ANTHROPIC_API_KEY` 的值
