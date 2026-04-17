## Context

当前项目使用 `src/ai_chat/` 布局，Python 包安装到 `site-packages` 后通过 pth 文件引用 `src/` 目录。这与 FastAPI 官方推荐的 `app/` 布局不一致，且在 Python 3.13 venv 环境下存在 pth 文件处理问题。

**当前结构：**
```
ai-chat/
├── src/ai_chat/       # 所有代码
├── main.py            # 变通方案
├── sitecustomize.py   # 变通方案
└── pyproject.toml     # packages = ["src/ai_chat"]
```

**目标结构：**
```
ai-chat/
├── app/               # 所有代码（直接布局）
└── pyproject.toml     # packages = ["app"]
```

## Goals / Non-Goals

**Goals:**
- 采用 FastAPI 官方推荐的 `app/` 目录布局
- `fastapi dev` 可直接启动，无需变通
- 简化项目结构，减少特殊配置

**Non-Goals:**
- 不改变任何功能代码逻辑
- 不添加或删除模块
- 不改变依赖配置（除 `packages` 外）

## Decisions

### Decision 1: 采用 `app/` 直接布局

**选择**: 将 `src/ai_chat/` 重命名为 `app/`

**理由**:
- FastAPI 官方教程和模板都用此布局
- `fastapi dev` 默认查找 `main.py` 或 `app/` 目录
- 消除 pth 文件依赖

### Decision 2: 入口文件简化

**选择**: 删除 `main.py` 和 `sitecustomize.py`

**理由**:
- `app/main.py` 可直接作为 FastAPI 入口
- 不再需要 Python 3.13 venv 的 workaround

### Decision 3: 更新 pyproject.toml

**选择**: 修改 `packages = ["app"]`，更新 `scripts` 入口路径

**理由**:
- hatchling 需要知道包的位置
- CLI 脚本需要更新引用路径

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|------|--------|------------|
| 导入路径大规模修改 | 可能遗漏某些引用 | 使用 IDE 重构功能 + 全局搜索验证 |
| CI/CD 路径硬编码 | 构建可能失败 | 检查并更新 CI 配置 |
| 第三方工具依赖 | 可能需要额外配置 | 验证 `fastapi dev` 工作正常 |
