## ADDED Requirements

### Requirement: Document Loader

系统 SHALL 支持加载文档文件，支持 PDF、TXT、Markdown 格式。

#### Scenario: Load PDF document
- **WHEN** 用户上传 `.pdf` 文件
- **THEN** 系统 SHALL 返回文档的纯文本内容

#### Scenario: Load TXT document
- **WHEN** 用户上传 `.txt` 文件
- **THEN** 系统 SHALL 返回文件原始文本内容

#### Scenario: Load Markdown document
- **WHEN** 用户上传 `.md` 文件
- **THEN** 系统 SHALL 返回 Markdown 解析后的纯文本内容

#### Scenario: Unsupported file format
- **WHEN** 用户上传不支持的格式（如 `.exe`）
- **THEN** 系统 SHALL 返回错误信息
