"""RAG API 路由。"""

from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel

from ..dependencies import get_rag_service
from ...clients import create_llm_client
from ...rag import RAGService
from ...settings import get_settings

router = APIRouter(prefix="/rag", tags=["rag"])


class SourceResponse(BaseModel):
    """来源片段响应模型。"""

    content: str
    score: float
    source: str
    chunk_index: int


class RAGQueryResponse(BaseModel):
    """RAG 查询响应模型。"""

    answer: str
    sources: list[SourceResponse]


class RAGStatusResponse(BaseModel):
    """RAG 状态响应模型。"""

    chunks: int


class MessageResponse(BaseModel):
    """通用消息响应模型。"""

    message: str


def get_llm_client() -> Any:
    """获取 LLM 客户端。"""
    settings = get_settings()
    api_key = settings.openai_api_key
    base_url = settings.openai_base_url
    model = settings.get_default_model("openai")
    return create_llm_client("openai", api_key, model=model, base_url=base_url)


def get_embedding_client() -> Any:
    """获取 Embedding 客户端。"""
    settings = get_settings()
    api_key = settings.openai_api_key
    base_url = settings.openai_base_url
    return create_llm_client("openai", api_key, base_url=base_url)


@router.post("/upload", response_model=MessageResponse)
async def rag_upload(
    file: UploadFile = File(...),
    service: RAGService = Depends(get_rag_service),
) -> MessageResponse:
    """上传文档到 RAG 系统。

    支持 PDF、TXT、Markdown 格式。
    """
    settings = get_settings()

    if not settings.is_openai_configured():
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".pdf", ".txt", ".md"}:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: {suffix}. Supported: PDF, TXT, Markdown"
        )

    try:
        # 读取文件内容到临时文件
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # 加载文档
        content_text = service.loader.load(tmp_path)

        # 分割文档
        chunks = service.splitter.split_with_metadata(content_text, source=file.filename or "unknown")

        # 计算 embeddings
        embedding_client = get_embedding_client()
        texts = [chunk["content"] for chunk in chunks]
        embeddings = embedding_client.embeddings(texts)

        # 添加到向量存储
        service.vector_store.add_documents(chunks, embeddings)

        # 清理临时文件
        Path(tmp_path).unlink()

        return MessageResponse(message=f"Document uploaded successfully. {len(chunks)} chunks added.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}") from e


@router.post("/query", response_model=RAGQueryResponse)
async def rag_query(
    question: str,
    service: RAGService = Depends(get_rag_service),
) -> RAGQueryResponse:
    """基于已上传的文档提问。

    返回答案和参考来源。
    """
    settings = get_settings()

    if not settings.is_openai_configured():
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    if service.is_empty:
        raise HTTPException(status_code=400, detail="No documents uploaded. Please upload documents first.")

    try:
        embedding_client = get_embedding_client()
        llm_client = get_llm_client()

        # 获取 query embedding
        query_embeddings = embedding_client.embeddings([question])

        # 查询
        result = service.query(
            question=question,
            query_embedding=query_embeddings[0],
            llm_client=llm_client,
        )

        return RAGQueryResponse(
            answer=result["answer"],
            sources=[
                SourceResponse(
                    content=src["content"],
                    score=src["score"],
                    source=src["source"],
                    chunk_index=src["chunk_index"],
                )
                for src in result["sources"]
            ],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}") from e


@router.post("/clear", response_model=MessageResponse)
async def rag_clear(
    service: RAGService = Depends(get_rag_service),
) -> MessageResponse:
    """清除所有已上传的文档。"""
    service.clear()
    return MessageResponse(message="Document store cleared.")


@router.get("/status", response_model=RAGStatusResponse)
async def rag_status(
    service: RAGService = Depends(get_rag_service),
) -> RAGStatusResponse:
    """查看当前文档库状态。"""
    return RAGStatusResponse(chunks=len(service.vector_store))
