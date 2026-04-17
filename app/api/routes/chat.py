"""聊天路由模块。"""

import asyncio
import threading
from typing import AsyncIterator, Iterator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from ..dependencies import get_chat_service
from ..models import ChatRequest, ChatResponse, ErrorResponse
from ...conversation import ChatService


router = APIRouter(prefix="/chat", tags=["chat"])


async def _stream_sse(generator: Iterator[str], conversation_id: str) -> AsyncIterator[str]:
    """将同步生成器桥接为异步 SSE 输出。"""
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[object] = asyncio.Queue()
    done = object()

    def publish(item: object) -> None:
        loop.call_soon_threadsafe(queue.put_nowait, item)

    def consume() -> None:
        try:
            for chunk in generator:
                publish(chunk)
        except Exception as exc:
            publish(exc)
        finally:
            publish(done)

    threading.Thread(target=consume, daemon=True).start()

    yield f"data: {conversation_id}\n\n"

    while True:
        item = await queue.get()
        if item is done:
            break
        if isinstance(item, Exception):
            raise item
        yield f"data: {item}\n\n"

    yield "data: [DONE]\n\n"


@router.post("", response_model=ChatResponse, responses={500: {"model": ErrorResponse}})
async def chat(request: ChatRequest, service: ChatService = Depends(get_chat_service)) -> ChatResponse:
    """处理聊天请求（同步模式）。

    Args:
        request: 聊天请求。
        service: 通过 DI 注入的 ChatService 实例。

    Returns:
        AI 的回复内容和会话 ID。
    """
    try:
        response, conversation_id = await service.chat(
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
async def chat_stream(request: ChatRequest, service: ChatService = Depends(get_chat_service)) -> StreamingResponse:
    """处理聊天请求（流式 SSE 模式）。

    Args:
        request: 聊天请求。
        service: 通过 DI 注入的 ChatService 实例。

    Returns:
        SSE 流式响应。
    """
    try:
        generator, conversation_id = service.stream(
            message=request.message,
            provider=request.provider or "openai",
            conversation_id=request.conversation_id,
            system_prompt=request.system_prompt,
            model=request.model,
        )

        return StreamingResponse(
            _stream_sse(generator, conversation_id),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}") from e
