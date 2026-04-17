## Why

当前 AI Chat 只支持纯文本对话，无法基于私有文档（如知识库、技术文档）回答问题。RAG（检索增强生成）让 AI 能够"阅读"文档并在回答时引用相关内容，提升回答的准确性和可信度。

## What Changes

- 新增 RAG 模块，支持文档加载、分割、向量存储和检索
- CLI 和 API 支持上传文档并基于文档问答
- 向量存储使用内存存储（后续可扩展到 Chroma/Pinecone）
- LangChain 用于 RAG 链式调用

## Capabilities

### New Capabilities
- `document-loader`: 文档加载器，支持 PDF、TXT、Markdown 等格式
- `text-splitter`: 文本分割器，将长文档分割成适合检索的 chunks
- `vector-store`: 向量存储，使用内存向量存储（FAISS 或简单列表）
- `retriever`: 检索器，基于语义相似度检索相关文档

### Modified Capabilities
- 无

## Impact

- `src/ai_chat/rag/` - 新增 RAG 模块
- `src/ai_chat/cli/main.py` - 新增 `/rag` 子命令
- `src/ai_chat/api/routes/` - 新增 `/rag` API 端点
- 依赖：`langchain-community`, `langchain-text-splitters`
