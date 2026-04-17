## ADDED Requirements

### Requirement: Text Splitter

系统 SHALL 将长文档分割成适合检索的 chunks，每个 chunk 包含不超过 500 字符。

#### Scenario: Split long document
- **WHEN** 文档文本长度超过 500 字符
- **THEN** 系统 SHALL 将文档分割成多个 chunks，每个 chunk 最多 500 字符

#### Scenario: Chunk overlap
- **WHEN** 文档被分割时
- **THEN** 相邻 chunks 之间 SHALL 有 50 字符的重叠以保持上下文连贯

#### Scenario: Short document
- **WHEN** 文档文本长度不超过 500 字符
- **THEN** 系统 SHALL 返回单个 chunk
