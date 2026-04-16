"""聊天路由模块。"""

from typing import Iterator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from ..models import ChatRequest, ChatResponse, ErrorResponse
from ...clients import create_llm_client, ConfigurationError
from ...conversation import ChatService, InMemoryConversationStore


# 全局聊天服务和会话存储
_store = InMemoryConversationStore()
_chat_service = ChatService(
    store=_store,
    llm_client_factory=lambda provider: _get_llm_client(provider)
)


def _get_llm_client(provider: str) -> object:
    """获取 LLM 客户端实例。

    Args:
        provider: LLM 提供商名称。

    Returns:
        LLM 客户端实例。

    Raises:
        HTTPException: 如果配置缺失或不支持的提供商。
    """
    from .. import load_config
    load_config()
    from ...settings import Settings
    settings = Settings()

    try:
        if provider == "openai":
            api_key = settings.openai_api_key
            base_url = settings.openai_base_url
            if not api_key:
                raise HTTPException(status_code=500, detail="OpenAI API key not configured")
            return create_llm_client("openai", api_key, base_url=base_url)
        elif provider == "anthropic":
            api_key = settings.anthropic_api_key
            if not api_key:
                raise HTTPException(status_code=500, detail="Anthropic API key not configured")
            return create_llm_client("anthropic", api_key)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider}")
    except ConfigurationError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse, responses={500: {"model": ErrorResponse}})
async def chat(request: ChatRequest) -> ChatResponse:
    """处理聊天请求（同步模式）。

    Args:
        request: 聊天请求。

    Returns:
        AI 的回复内容和会话 ID。
    """
    try:
        response, conversation_id = _chat_service.chat(
            message=request.message,
            provider=request.provider or "openai",
            conversation_id=request.conversation_id,
            system_prompt=request.system_prompt,
            model=request.model,
        )
        return ChatResponse(response=response, conversation_id=conversation_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}") from e


@router.post("/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    """处理聊天请求（流式 SSE 模式）。

    Args:
        request: 聊天请求。

    Returns:
        SSE 流式响应。
    """
    try:
        generator, conversation_id = _chat_service.stream(
            message=request.message,
            provider=request.provider or "openai",
            conversation_id=request.conversation_id,
            system_prompt=request.system_prompt,
            model=request.model,
        )

        def generate() -> Iterator[str]:
            # 先发送 conversation_id
            yield f"data: {conversation_id}\n\n"
            # 然后发送流式内容
            for chunk in generator:
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}") from e
