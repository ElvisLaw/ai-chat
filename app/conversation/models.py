"""消息和会话数据模型。"""

from datetime import datetime, timezone
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field


def _utc_now() -> datetime:
    """返回当前 UTC 时间（timezone-aware）。"""
    return datetime.now(timezone.utc)


class Role(str, Enum):
    """消息角色枚举。"""

    user = "user"
    assistant = "assistant"
    system = "system"


class Message(BaseModel):
    """消息模型。"""

    role: Role = Field(..., description="消息角色")
    content: str = Field(..., description="消息内容")
    timestamp: datetime = Field(default_factory=_utc_now, description="创建时间")

    model_config = {
        "json_schema_extra": {
            "example": {
                "role": "user",
                "content": "你好，请介绍一下你自己",
                "timestamp": "2026-04-16T12:00:00"
            }
        }
    }


class Conversation(BaseModel):
    """会话模型。"""

    id: str = Field(default_factory=lambda: __import__("uuid").uuid4().hex, description="会话 ID")
    messages: list[Message] = Field(default_factory=list, description="消息列表")
    created_at: datetime = Field(default_factory=_utc_now, description="创建时间")
    updated_at: datetime = Field(default_factory=_utc_now, description="最后更新时间")
    is_summarized: bool = Field(default=False, description="是否已生成摘要")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "abc123def456",
                "messages": [],
                "created_at": "2026-04-16T12:00:00",
                "updated_at": "2026-04-16T12:00:00"
            }
        }
    }

    def add_message(self, role: Role, content: str) -> Message:
        """添加消息到会话。

        Args:
            role: 消息角色。
            content: 消息内容。

        Returns:
            创建的消息。
        """
        message = Message(role=role, content=content)
        self.messages.append(message)
        self.updated_at = datetime.now(timezone.utc)
        return message

    def get_messages_for_llm(self, system_prompt: str | None = None) -> list[dict]:
        """获取适合发送给 LLM 的消息格式。

        Args:
            system_prompt: 系统提示词。

        Returns:
            消息字典列表。
        """
        result = []
        if system_prompt:
            result.append({"role": "system", "content": system_prompt})
        for msg in self.messages:
            result.append({"role": msg.role.value, "content": msg.content})
        return result
