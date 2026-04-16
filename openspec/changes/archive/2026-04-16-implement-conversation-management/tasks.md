## 1. 模块结构

- [x] 1.1 创建 `src/ai_chat/conversation/` 目录
- [x] 1.2 创建 `src/ai_chat/conversation/__init__.py`
- [x] 1.3 创建 `src/ai_chat/conversation/models.py`（Message、Role、Conversation）
- [x] 1.4 创建 `src/ai_chat/conversation/store.py`（ConversationStore、InMemoryConversationStore）
- [x] 1.5 创建 `src/ai_chat/conversation/service.py`（ChatService）

## 2. 数据模型实现

- [x] 2.1 实现 `Role` 枚举（user、assistant、system）
- [x] 2.2 实现 `Message` 模型（role、content、timestamp）
- [x] 2.3 实现 `Conversation` 模型（id、messages、created_at、updated_at）

## 3. 会话存储实现

- [x] 3.1 实现 `ConversationStore` 抽象接口
- [x] 3.2 实现 `InMemoryConversationStore` 内存存储
- [x] 3.3 实现 `create()` 方法
- [x] 3.4 实现 `get()` 方法
- [x] 3.5 实现 `save()` 方法
- [x] 3.6 实现 `delete()` 方法
- [x] 3.7 实现 `list()` 方法

## 4. 聊天服务实现

- [x] 4.1 实现 `ChatService.__init__()` 方法
- [x] 4.2 实现 `chat()` 方法（新会话流程）
- [x] 4.3 实现 `chat()` 方法（继续会话流程）
- [x] 4.4 实现 `stream()` 方法（新会话流程）
- [x] 4.5 实现 `stream()` 方法（继续会话流程）
- [x] 4.6 添加消息数量限制检查（100 条）

## 5. API 集成

- [x] 5.1 修改 `ChatRequest` 添加 `conversation_id` 字段
- [x] 5.2 修改 `ChatResponse` 添加 `conversation_id` 字段
- [x] 5.3 修改 `/chat` 端点支持多轮对话
- [x] 5.4 修改 `/chat/stream` 端点支持多轮对话

## 6. 单元测试

- [x] 6.1 测试数据模型（Message、Conversation）
- [x] 6.2 测试会话存储（InMemoryConversationStore）
- [x] 6.3 测试 ChatService 新会话流程
- [x] 6.4 测试 ChatService 继续会话流程
- [x] 6.5 测试 API 端点多轮对话

## 7. 集成验证

- [x] 7.1 启动服务验证 /health 端点
- [x] 7.2 测试 /chat 端点单轮对话
- [x] 7.3 测试多轮对话（使用 conversation_id）
- [x] 7.4 验证 Settings 能正确读取环境变量
- [x] 7.5 验证 LLM 客户端支持 conversation_messages 参数
