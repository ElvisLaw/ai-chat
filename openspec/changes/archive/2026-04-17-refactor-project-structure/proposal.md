## Why

当前项目使用 `src/ai_chat/` 布局，与 FastAPI 官方推荐的 `app/` 布局不一致。这导致：
- `fastapi dev` 无法直接启动，需要变通方案
- Python 3.13 venv 的 pth 文件处理问题
- 与 FastAPI 生态（模板、教程、插件）不兼容

## What Changes

- 将 `src/ai_chat/` 重命名为 `app/`
- 更新 `pyproject.toml` 的 `packages` 配置
- 修复所有模块导入路径 (`from src.ai_chat.X` → `from app.X`)
- 删除变通文件 `main.py` 和 `sitecustomize.py`
- 保持功能不变，仅调整目录结构

## Capabilities

### New Capabilities
- `project-structure`: 项目结构标准化，采用 FastAPI 官方推荐的 `app/` 目录布局

### Modified Capabilities
- 无（仅重构，无功能变更）

## Impact

- 所有 Python 导入路径需更新
- `pyproject.toml` 的 `packages` 配置需修改
- `pyproject.toml` 的 `scripts` 入口点路径需更新
- 测试文件导入路径需更新
- CI/CD 配置（如果有）需更新
- `fastapi dev` 可直接启动（不再需要 workaround）
