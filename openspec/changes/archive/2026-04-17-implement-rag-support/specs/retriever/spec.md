## ADDED Requirements

### Requirement: Retriever

系统 SHALL 基于语义相似度检索相关文档 chunks。

#### Scenario: Retrieve relevant documents
- **WHEN** 用户提交查询
- **THEN** 系统 SHALL 返回与查询语义最相关的 4 个文档 chunks

#### Scenario: No documents uploaded
- **WHEN** 用户在文档库为空时发起查询
- **THEN** 系统 SHALL 返回友好提示："请先上传文档"

#### Scenario: No relevant documents
- **WHEN** 查询与所有文档相似度都低于阈值
- **THEN** 系统 SHALL 返回空结果并提示用户

#### Scenario: Context integration
- **WHEN** 检索到相关 chunks 后
- **THEN** 系统 SHALL 将 chunks 内容注入到 LLM 上下文中生成回答
