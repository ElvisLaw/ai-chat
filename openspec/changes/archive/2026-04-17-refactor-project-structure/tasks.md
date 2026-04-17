## 1. 项目结构变更

- [x] 1.1 将 `src/ai_chat/` 目录重命名为 `app/`
- [x] 1.2 更新 `pyproject.toml` 的 `packages = ["app"]`
- [x] 1.3 更新 `pyproject.toml` 的 `scripts` 入口点路径 (`ai_chat.X` → `app.X`)

## 2. 修复导入路径

- [x] 2.1 修复 `app/__init__.py` 导入
- [x] 2.2 修复 `app/api/__init__.py` 导入
- [x] 2.3 修复 `app/api/__main__.py` 导入
- [x] 2.4 修复 `app/api/server.py` 导入
- [x] 2.5 修复 `app/api/dependencies.py` 导入
- [x] 2.6 修复 `app/api/models.py` 导入
- [x] 2.7 修复 `app/api/routes/*.py` 导入
- [x] 2.8 修复 `app/cli/*.py` 导入
- [x] 2.9 修复 `app/clients/*.py` 导入
- [x] 2.10 修复 `app/conversation/*.py` 导入
- [x] 2.11 修复 `app/rag/*.py` 导入

## 3. 删除变通文件

- [x] 3.1 删除根目录 `main.py`
- [x] 3.2 删除 `sitecustomize.py`（如果存在）

## 4. 更新测试

- [x] 4.1 更新测试文件中的导入路径
- [x] 4.2 验证测试通过

## 5. 验证

- [x] 5.1 验证 `fastapi dev` 可以直接启动（需用 `fastapi dev app/api`）
- [x] 5.2 验证 CLI 命令正常工作
- [x] 5.3 验证 API 端点正常工作
