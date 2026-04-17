## 1. 修改 Settings

- [x] 1.1 添加 DEFAULT_MODELS 常量（按 provider 定义默认模型）
- [x] 1.2 添加 get_default_model(provider) 方法
- [x] 1.3 移除全局 model 字段或改为可选

## 2. 修改 ChatService

- [x] 2.1 统一 chat() 和 stream() 获取默认模型的逻辑
- [x] 2.2 调用 get_default_model(provider) 获取默认值

## 3. 集成验证

- [x] 3.1 测试同步接口未传 model 时使用默认模型
- [x] 3.2 测试流式接口未传 model 时使用默认模型
- [x] 3.3 测试 Anthropic provider 使用正确的默认模型
- [x] 3.4 验证 OpenAI provider 使用 gpt-4
