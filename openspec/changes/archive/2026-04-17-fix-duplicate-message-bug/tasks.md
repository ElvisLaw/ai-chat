## 1. 修复 ChatService

- [x] 1.1 修改 `service.py` 的 `chat()` 方法，传递完整消息历史
- [x] 1.2 修改 `service.py` 的 `stream()` 方法，传递完整消息历史

## 2. 修复 OpenAI 客户端

- [x] 2.1 修改 `openai_client.py` 的 `send_message()` 接收 `messages` 参数
- [x] 2.2 修改 `openai_client.py` 的 `stream_message()` 接收 `messages` 参数

## 3. 修复 Anthropic 客户端

- [x] 3.1 修改 `anthropic_client.py` 的 `send_message()` 接收 `messages` 参数
- [x] 3.2 修改 `anthropic_client.py` 的 `stream_message()` 接收 `messages` 参数

## 4. 集成验证

- [x] 4.1 测试单轮对话正常
- [x] 4.2 测试多轮对话（第二轮不应有重复消息）
- [x] 4.3 验证 token 使用量正常
