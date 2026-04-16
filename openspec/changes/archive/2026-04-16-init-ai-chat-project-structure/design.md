## Context

我们正在初始化一个 AI Chat Python 项目。当前项目目录几乎是空的，只有 OpenSpec 的技能文件夹。我们需要建立一个标准化的 Python 项目结构作为后续开发的基础。

项目将使用标准的 Python 打包工具（pyproject.toml），而不是传统的 setup.py 或 requirements.txt。

## Goals / Non-Goals

**Goals:**
- 创建清晰的目录结构，便于代码组织和维护
- 使用现代 Python 打包标准（pyproject.toml + hatch）
- 支持虚拟环境隔离
- 为 AI Chat 功能预留扩展能力

**Non-Goals:**
- 不实现具体的 AI 聊天功能（本阶段仅建立项目结构）
- 不配置 CI/CD 或部署流程
- 不创建数据库 schema

## Decisions

### Decision 1: 使用 `src/` 布局还是根目录布局？

采用 `src/` 布局（src/ai_chat/）而不是纯根目录布局。

**原因：**
- 避免 Python 导入路径问题
- 允许同时安装和开发版本
- 符合 pytest 和其他工具的默认期望

**替代方案：**
- 根目录布局：简单但可能导致导入问题，不推荐

### Decision 2: 使用 hatch 而不是 setuptools

使用 `hatch` 作为打包后端。

**原因：**
- pyproject.toml 原生支持，无需额外配置
- 清晰的依赖声明格式
- 更好的虚拟环境管理集成

**替代方案：**
- setuptools：更成熟但配置更复杂
- poetry：功能类似但生态稍小

### Decision 3: 目录结构

采用以下目录结构：

```
ai-chat/
├── src/              # 源代码
│   └── ai_chat/      # 主包
├── tests/            # 测试文件
├── config/           # 配置文件
├── docs/             # 文档
├── pyproject.toml    # 项目配置
├── .gitignore        # Git 忽略文件
└── README.md         # 项目说明
```

## Risks / Trade-offs

- **风险**：对初学者来说，`src/` 布局可能需要额外的 PYTHONPATH 配置
  - **缓解**：在 pyproject.toml 中正确配置包路径

- **风险**：AI 包可能需要特定版本的 Python 或依赖
  - **缓解**：在 pyproject.toml 中明确声明 Python 版本要求
