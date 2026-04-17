"""RAG CLI commands."""

import asyncio
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from ..clients import create_llm_client
from ..rag import RAGService
from ..settings import get_settings

console = Console()

rag_app = typer.Typer(help="RAG 文档问答命令")


def _get_embedding_client():
    """获取用于 embedding 的客户端。"""
    settings = get_settings()
    api_key = settings.openai_api_key
    base_url = settings.openai_base_url
    return create_llm_client("openai", api_key, base_url=base_url)


def _get_llm_client():
    """获取用于生成回答的 LLM 客户端。"""
    settings = get_settings()
    api_key = settings.openai_api_key
    base_url = settings.openai_base_url
    model = settings.get_default_model("openai")
    return create_llm_client("openai", api_key, model=model, base_url=base_url)


# 全局 RAG Service 实例
_rag_service: RAGService | None = None


def get_rag_service() -> RAGService:
    """获取或创建全局 RAG Service 实例。"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service


@rag_app.command()
def upload(
    file_path: Annotated[str, typer.Argument(help="文档文件路径 (PDF/TXT/MD)")],
) -> None:
    """上传文档到 RAG 系统。

    用法:
        ai-chat rag upload ./document.pdf
    """
    settings = get_settings()

    if not settings.is_openai_configured():
        console.print("[red]OpenAI API key 未配置[/red]")
        console.print("请设置 OPENAI_API_KEY 环境变量")
        raise typer.Exit(1)

    path = Path(file_path)
    if not path.exists():
        console.print(f"[red]文件不存在: {file_path}[/red]")
        raise typer.Exit(1)

    suffix = path.suffix.lower()
    if suffix not in {".pdf", ".txt", ".md"}:
        console.print(f"[red]不支持的文件格式: {suffix}[/red]")
        console.print("支持的格式: PDF, TXT, Markdown")
        raise typer.Exit(1)

    console.print(f"[dim]正在加载文档: {file_path}[/dim]")

    try:
        service = get_rag_service()
        embedding_client = _get_embedding_client()

        # 加载文档
        content = service.loader.load(file_path)
        console.print(f"[dim]文档加载完成，字符数: {len(content)}[/dim]")

        # 分割文档
        chunks = service.splitter.split_with_metadata(content, source=file_path)
        console.print(f"[dim]分割为 {len(chunks)} 个 chunks[/dim]")

        # 计算 embeddings
        texts = [chunk["content"] for chunk in chunks]
        embeddings = embedding_client.embeddings(texts)
        console.print(f"[dim]计算 embeddings 完成[/dim]")

        # 添加到向量存储
        service.vector_store.add_documents(chunks, embeddings)
        console.print(f"[green]文档上传成功！共 {len(chunks)} 个 chunks[/green]")

    except Exception as e:
        console.print(f"[red]上传失败: {e}[/red]")
        raise typer.Exit(1)


@rag_app.command()
def query(
    question: Annotated[str, typer.Argument(help="问题")],
) -> None:
    """基于已上传的文档提问。

    用法:
        ai-chat rag query "文档主要内容是什么？"
    """
    settings = get_settings()

    if not settings.is_openai_configured():
        console.print("[red]OpenAI API key 未配置[/red]")
        console.print("请设置 OPENAI_API_KEY 环境变量")
        raise typer.Exit(1)

    service = get_rag_service()

    if service.is_empty:
        console.print("[yellow]文档库为空，请先上传文档: ai-chat rag upload <文件路径>[/yellow]")
        raise typer.Exit(1)

    try:
        embedding_client = _get_embedding_client()
        llm_client = _get_llm_client()

        console.print(f"[dim]正在检索相关文档...[/dim]")

        # 获取 query embedding
        query_embeddings = embedding_client.embeddings([question])

        # 查询
        result = service.query(
            question=question,
            query_embedding=query_embeddings[0],
            llm_client=llm_client,
        )

        console.print()
        console.print("[bold cyan]回答:[/bold cyan]")
        console.print(result["answer"])

        if result["sources"]:
            console.print()
            console.print("[bold]参考来源:[/bold]")
            for i, src in enumerate(result["sources"], 1):
                console.print(f"  [{i}] {src['source']} (chunk {src['chunk_index']}, score: {src['score']:.2f})")

    except Exception as e:
        console.print(f"[red]查询失败: {e}[/red]")
        raise typer.Exit(1)


@rag_app.command()
def clear() -> None:
    """清除所有已上传的文档。

    用法:
        ai-chat rag clear
    """
    service = get_rag_service()
    service.clear()
    console.print("[green]文档库已清空[/green]")


@rag_app.command()
def status() -> None:
    """查看当前文档库状态。

    用法:
        ai-chat rag status
    """
    service = get_rag_service()
    count = len(service.vector_store)
    if count == 0:
        console.print("[yellow]文档库为空[/yellow]")
    else:
        console.print(f"[green]文档库包含 {count} 个 chunks[/green]")
