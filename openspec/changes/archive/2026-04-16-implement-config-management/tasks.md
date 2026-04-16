## 1. Configuration Files

- [x] 1.1 创建 `src/ai_chat/config.py` - 配置加载模块
- [x] 1.2 创建 `src/ai_chat/settings.py` - Pydantic 配置模型
- [x] 1.3 创建 `.env.example` - 环境变量模板

## 2. Implementation Details

- [x] 2.1 在 `config.py` 中实现 `load_dotenv()` 加载
- [x] 2.2 在 `settings.py` 中实现 `Settings` 类
- [x] 2.3 实现 `is_openai_configured()` 方法
- [x] 2.4 实现 `is_anthropic_configured()` 方法

## 3. Verification

- [x] 3.1 验证配置可从环境变量读取
- [x] 3.2 验证 Pydantic 模型验证正常工作
- [x] 3.3 验证配置完整性检查方法工作正常
