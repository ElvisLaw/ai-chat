---
name: ai-chat-project-plan
description: AI Chat Python项目OpenSpec工作流规划
type: project
originSessionId: fc845397-edf5-4bb1-b74a-b4db1e5a3c41
---

## AI Chat 项目 OpenSpec 工作流

> 已归档 Changes 查看：`openspec list` 或访问 [openspec/changes/archive/](openspec/changes/archive/)

---

### 待处理 Changes（按优先级）

#### 1. implement-conversation-memory
多轮对话记忆

**Capabilities:**
- `memory-buffer`: 对话缓冲
- `memory-summary`: 对话摘要
- `memory-persistence`: 记忆持久化

---

#### 2. implement-tool-calling
工具调用功能

**Capabilities:**
- `tool-registry`: 工具注册表
- `tool-executor`: 工具执行器
- `tool-definitions`: 工具定义规范

---

### self-improving-agent 使用指南

**安装位置:** `~/.claude/skills/self-improving-agent/`

**触发时机（在项目开发中）：**
1. 命令或操作意外失败时
2. 用户纠正 Claude（"不对，应该是..."）
3. 用户请求不存在的功能
4. 外部 API 或工具失败
5. Claude 发现知识过时或有误
6. 发现更好的方法解决反复出现的任务

**使用方式:**
- 在遇到错误或用户纠正时，主动调用 self-improving-agent
- 将错误、纠正和学习记录到 `.learnings/` 目录
- 定期回顾 `.learnings/` 内容，避免重复犯错

**注意事项:**
- 项目内和全局都安装了 self-improving-agent
- 全局安装路径: `~/.claude/skills/self-improving-agent/`
- 项目安装路径: `ai-chat/.claude/skills/self-improving-agent/`
