"""FastAPI 依赖注入函数。"""

from fastapi import Request

from ..conversation import ChatService, ConversationStore
from ..rag import RAGService


def get_chat_service(request: Request) -> ChatService:
    """从 app.state 获取 ChatService 实例。"""
    return request.app.state.chat_service


def get_store(request: Request) -> ConversationStore:
    """从 app.state 获取 ConversationStore 实例。"""
    return request.app.state.store


def get_rag_service(request: Request) -> RAGService:
    """从 app.state 获取 RAGService 实例。"""
    return request.app.state.rag_service
