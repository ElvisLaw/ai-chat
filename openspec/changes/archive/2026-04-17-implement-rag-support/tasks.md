## 1. 项目依赖和目录

- [x] 1.1 添加 langchain-community, langchain-text-splitters 依赖到 pyproject.toml
- [x] 1.2 创建 src/ai_chat/rag/ 目录结构

## 2. Document Loader

- [x] 2.1 实现 DocumentLoader 类，支持 PDF 加载
- [x] 2.2 实现 DocumentLoader 类，支持 TXT 加载
- [x] 2.3 实现 DocumentLoader 类，支持 Markdown 加载
- [x] 2.4 添加不支持格式的错误处理

## 3. Text Splitter

- [x] 3.1 实现 TextSplitter 类，chunk 大小 500 字符
- [x] 3.2 实现 chunk overlap 50 字符
- [x] 3.3 验证短文档返回单个 chunk

## 4. Vector Store

- [x] 4.1 实现内存向量存储 VectorStore 类
- [x] 4.2 实现 add_documents 方法存储 chunks 和向量
- [x] 4.3 实现 clear 方法清空存储
- [x] 4.4 实现 cosine_similarity 计算

## 5. Retriever

- [x] 5.1 实现 Retriever 类，检索 top-k 相关 chunks
- [x] 5.2 实现 context 注入方法

## 6. RAG Service

- [x] 6.1 实现 RAGService 类，整合 loader/splitter/store/retriever
- [x] 6.2 实现 load_document 方法
- [x] 6.3 实现 query 方法，返回基于文档的回答

## 7. CLI 集成

- [x] 7.1 在 CLI 添加 rag 子命令
- [x] 7.2 支持上传文档并问答
- [x] 7.3 支持清除文档库

## 8. API 集成

- [x] 8.1 在 API 添加 /rag/upload 端点
- [x] 8.2 在 API 添加 /rag/query 端点
- [x] 8.3 在 API 添加 /rag/clear 端点

## 9. 测试

- [x] 9.1 编写 DocumentLoader 单元测试
- [x] 9.2 编写 TextSplitter 单元测试
- [x] 9.3 编写 VectorStore 单元测试
- [x] 9.4 编写 Retriever 单元测试
- [ ] 9.5 集成测试 CLI rag 命令
