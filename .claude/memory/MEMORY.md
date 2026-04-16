# Claude Code Memory Index

## 项目信息
- [AI Chat项目规划](ai-chat-project-plan.md) — OpenSpec工作流规划、已归档changes、待处理changes、self-improving-agent使用指南

## 技术栈
- Python 3.10+
- OpenAI SDK (openai>=1.0.0)
- Anthropic SDK (anthropic>=0.18.0)
- LangChain (langchain>=0.1.0, langchain-openai>=0.0.5)
- Pydantic (pydantic>=2.0.0)
- python-dotenv (python-dotenv>=1.0.0)

## 项目结构
- 源码: src/ai_chat/
- 测试: tests/
- 配置: config/
- 文档: docs/
- OpenSpec: openspec/

## Git 仓库
- https://github.com/ElvisLaw/ai-chat

## Skills
- self-improving-agent: ~/.claude/skills/self-improving-agent/ & ai-chat/.claude/skills/self-improving-agent/
- find-skills: ~/.claude/skills/find-skills/ & ai-chat/.claude/skills/find-skills/
- OpenSpec 系列: ai-chat/.claude/skills/openspec-*/

## OpenSpec Changes
- 2026-04-16-init-ai-chat-project-structure (archived)
- 2026-04-16-add-langchain-dependency (archived)
- implement-config-management (待归档)

## 开发习惯
- 每次开发新功能前先创建 OpenSpec change
- 使用 /opsx:propose 创建完整 artifacts
- 实现完成后及时归档 changes
- 使用 self-improving-agent 记录错误和学习
- **每完成一个 OpenSpec change 后更新 memory 文件夹内容**
- **每完成一个 OpenSpec change 后更新 README.md**
