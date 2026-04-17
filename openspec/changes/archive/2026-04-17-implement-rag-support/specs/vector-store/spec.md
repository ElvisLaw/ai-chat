## ADDED Requirements

### Requirement: Vector Store

系统 SHALL 使用内存向量存储文档 chunks，支持添加文档和清除所有文档。

#### Scenario: Add document chunks to store
- **WHEN** 用户上传文档并完成分割后
- **THEN** 系统 SHALL 将 chunks 及其向量存储到内存中

#### Scenario: Clear all documents
- **WHEN** 用户调用清除功能
- **THEN** 系统 SHALL 清空内存中的所有文档和向量

#### Scenario: Document metadata
- **WHEN** 存储文档 chunk 时
- **THEN** 系统 SHALL 保留文档来源文件名和 chunk 索引信息
