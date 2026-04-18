"""会话管理路由模块。"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_store
from ...conversation import ConversationStore


router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get("", response_model=list[dict[str, Any]])
async def list_conversations(store: ConversationStore = Depends(get_store)) -> list[dict[str, Any]]:
    """列出所有会话。

    Returns:
        会话列表，按最后更新时间倒序。
    """
    conversations = store.list()
    return [
        {
            "id": conv.id,
            "message_count": len(conv.messages),
            "is_summarized": conv.is_summarized,
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat(),
        }
        for conv in conversations
    ]


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    store: ConversationStore = Depends(get_store),
) -> dict[str, str]:
    """删除指定会话。

    Args:
        conversation_id: 会话 ID。
        store: 通过 DI 注入的会话存储实例。

    Returns:
        删除结果。
    """
    deleted = store.delete(conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "deleted", "conversation_id": conversation_id}
