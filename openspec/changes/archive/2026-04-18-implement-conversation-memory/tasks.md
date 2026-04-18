## 1. 持久化存储实现

- [x] 1.1 创建 `FileConversationStore` 类，继承 `ConversationStore`
- [x] 1.2 实现 `_load` 方法，从 JSON 文件加载对话
- [x] 1.3 实现 `_save` 方法，保存对话到 JSON 文件
- [x] 1.4 实现 `_get_file_path` 方法，返回 `{home}/.ai-chat/conversations/{id}.json`
- [x] 1.5 在 `ConversationStoreFactory` 中添加 `file` 类型支持
- [x] 1.6 实现 `list_conversations` 方法，返回持久化对话列表
- [x] 1.7 实现 `delete_conversation` 方法，删除对话文件

## 2. 对话缓冲实现

- [x] 2.1 在 `ConversationService` 中添加 `_buffer_messages` 方法
- [x] 2.2 实现 `_estimate_tokens` 方法（字符数 / 4 估算）
- [x] 2.3 实现 `_trim_buffer_by_count` 方法，按消息数量清理（保留最新 20 条）
- [x] 2.4 实现 `_trim_buffer_by_tokens` 方法，按 Token 数量清理

## 3. 对话摘要实现

- [x] 3.1 创建 `MemorySummarizer` 类
- [x] 3.2 实现 `_generate_summary` 方法，调用 LLM 生成摘要（限制 500 字）
- [x] 3.3 实现 `_should_summarize` 方法，判断是否需要摘要（消息数 > 15 且 Token > 3000 且未摘要）
- [x] 3.4 在 `ConversationService` 中集成摘要触发逻辑
- [x] 3.5 实现增量摘要逻辑（基于原始摘要 + 新消息）
- [x] 3.6 添加 `is_summarized` 标记，追踪摘要状态

## 4. 配置和集成

- [x] 4.1 在 `Settings` 中添加记忆相关配置项（buffer_size, max_tokens, summarize_threshold）
- [x] 4.2 在 API 路由中支持查看会话历史列表
- [x] 4.3 在 API 路由中支持清除会话历史
- [x] 4.4 在 CLI 中添加 `history` 命令查看会话列表
- [x] 4.5 在 CLI 中添加 `clear` 命令清除会话

## 5. 测试

- [x] 5.1 编写 `FileConversationStore` 单元测试
- [x] 5.2 编写对话缓冲单元测试
- [x] 5.3 编写对话摘要单元测试
- [x] 5.4 集成测试持久化和摘要流程
