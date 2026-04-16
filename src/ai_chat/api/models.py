"""API 请求/响应模型。"""

from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """聊天请求模型。"""

    message: str = Field(..., description="用户发送的消息")
    provider: Optional[str] = Field(default="openai", description="LLM 提供商 (openai/anthropic)")
    model: Optional[str] = Field(default=None, description="模型名称（可选）")
    system_prompt: Optional[str] = Field(default=None, description="系统提示词（可选）")
    conversation_id: Optional[str] = Field(default=None, description="会话 ID（None 表示新会话）")

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "你好，请介绍一下你自己",
                "provider": "openai",
                "model": "gpt-4",
                "conversation_id": None
            }
        }
    }


class ChatResponse(BaseModel):
    """聊天响应模型。"""

    response: str = Field(..., description="AI 的回复内容")
    conversation_id: str = Field(..., description="会话 ID（用于继续对话）")

    model_config = {
        "json_schema_extra": {
            "example": {
                "response": "你好！我是 AI Chat，一个智能对话助手。",
                "conversation_id": "abc123def456"
            }
        }
    }


class HealthResponse(BaseModel):
    """健康检查响应模型。"""

    status: str = Field(default="ok", description="服务状态")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "ok"
            }
        }
    }


class ErrorResponse(BaseModel):
    """错误响应模型。"""

    error: str = Field(..., description="错误信息")
    detail: Optional[str] = Field(default=None, description="错误详情")

    model_config = {
        "json_schema_extra": {
            "example": {
                "error": "Internal Server Error",
                "detail": "LLM API 调用失败"
            }
        }
    }
