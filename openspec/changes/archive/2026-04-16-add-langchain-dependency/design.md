## Context

我们需要为 AI Chat 项目添加 LangChain 依赖。LangChain 是构建复杂 AI 应用的流行框架。

## Goals / Non-Goals

**Goals:**
- 添加 LangChain 作为项目依赖
- 支持使用 LangChain 构建聊天应用

**Non-Goals:**
- 不实现具体的 LangChain 功能（本阶段仅添加依赖）
- 不配置 LangChain 的特定集成

## Decisions

### Decision 1: 添加 langchain 和 langchain-openai

**原因：**
- `langchain` 提供核心框架
- `langchain-openai` 提供 OpenAI 的 LangChain 接口

## Risks / Trade-offs

无重大风险，添加依赖是简单的变更。
