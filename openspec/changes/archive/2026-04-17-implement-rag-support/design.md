## Context

当前 AI Chat 是纯文本对话机器人，用户无法让 AI 基于私有文档（如公司知识库、技术文档、用户手册）回答问题。

RAG（Retrieval-Augmented Generation）通过检索相关文档片段并注入到 LLM 上下文中，让 AI 能"阅读"文档后回答问题。

## Goals / Non-Goals

**Goals:**
- 支持文档上传和解析（PDF、TXT、Markdown）
- 文档分割成 chunks
- 内存向量存储（无需外部向量数据库）
- 基于文档内容的语义检索
- CLI 和 API 提供 RAG 问答接口

**Non-Goals:**
- 不实现持久化向量存储（Chroma/Pinecone 等）
- 不实现多租户隔离
- 不实现文档管理（上传/删除/列表）

## Decisions

### Decision 1: 使用 LangChain 生态

**选择**: 使用 `langchain-community`, `langchain-text-splitters`

**理由**:
- 与现有 `langchain` 和 `langchain-openai` 依赖一致
- LangChain 提供统一的文档加载、分割、检索接口
- 便于后续切换到 Chroma 等向量存储

### Decision 2: 向量存储使用内存列表 + 余弦相似度

**选择**: 简单内存向量存储，不引入 FAISS 等外部依赖

**理由**:
- 简化初始实现，降低复杂度
- 文档量少时性能足够
- 后续可平滑迁移到 FAISS 或 Chroma

### Decision 3: Embedding 模型

**选择**: 使用 OpenAI `text-embedding-3-small`（通过 MiniMax 或 OpenAI API）

**理由**:
- 保持与 LLM 调用方式一致
- 嵌入式模型成熟，效果好

### Decision 4: CLI 和 API 双接口

**选择**: CLI 新增 `rag` 子命令，API 新增 `/rag` 端点

**理由**:
- CLI 便于快速测试
- API 便于集成到其他系统

### Decision 5: API 返回格式

**选择**: `/rag/query` 返回结构化结果

```json
{
  "answer": "基于文档生成的回答...",
  "sources": [
    {
      "content": "chunk文本内容...",
      "score": 0.85,
      "source": "文件名.pdf",
      "chunk_index": 0
    }
  ]
}
```

**理由**:
- `answer` 包含 LLM 生成的回答
- `sources` 包含参考的文档片段，便于用户验证
- 每个 source 包含相似度分数、来源文件、chunk 索引

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|------|--------|------------|
| 向量检索精度不足 | 检索到不相关文档 | 使用 text-embedding-3-small，支持按 threshold 过滤 |
| 大文档内存爆炸 | 文档过大导致内存问题 | 限制单文件大小（如 10MB），分 chunk 大小控制 |
| 检索性能慢 | 文档量大时线性扫描慢 | 后续迁移到 FAISS 索引 |

## Open Questions

1. **文档更新策略**: 文档内容变化后如何更新向量？（暂定：重启服务重新加载）
2. **Chunk 大小**: 多少字符一个 chunk？（暂定：500 字符，overlap 50）
3. **检索数量**: 每次检索返回多少个相关片段？（暂定：top 4）
