## ADDED Requirements

### Requirement: Dependency Declaration via pyproject.toml

项目 SHALL 使用 `pyproject.toml` 声明所有依赖和项目元数据，包括：

- 项目名称和版本
- Python 版本要求
- 所有运行时依赖列表
- 所有开发依赖列表

#### Scenario: pyproject.toml exists and valid

- **WHEN** 开发者运行 `pip install -e .` 时
- **THEN** `pyproject.toml` SHALL 被正确解析并安装所有依赖

#### Scenario: Dependencies are listed

- **WHEN** 查看 `pyproject.toml` 时
- **THEN** 所有 AI Chat 相关的 Python 包 SHALL 被列出

### Requirement: Configuration File Support

项目 SHALL 支持通过 `.env` 文件或环境变量进行配置管理。

#### Scenario: Environment variable configuration

- **WHEN** 应用启动时
- **THEN** 环境变量 SHALL 可被读取并覆盖默认配置
