"""RAG Service integrating document loading, splitting, storage, and retrieval."""

from typing import Any, Dict, List, Optional

from app.rag.loader import DocumentLoader
from app.rag.retriever import Retriever, RetrievedChunk
from app.rag.splitter import TextSplitter
from app.rag.store import VectorStore


class RAGService:
    """Main RAG service for document-based question answering."""

    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        top_k: int = 4,
        similarity_threshold: float = 0.0,
    ):
        """
        Initialize the RAG service.

        Args:
            embedding_model: Name of the embedding model to use.
            chunk_size: Maximum characters per chunk.
            chunk_overlap: Overlap between chunks in characters.
            top_k: Number of chunks to retrieve per query.
            similarity_threshold: Minimum similarity threshold (0.0 to 1.0).
        """
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.loader = DocumentLoader()
        self.splitter = TextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.vector_store = VectorStore()
        self.retriever = Retriever(
            vector_store=self.vector_store,
            top_k=top_k,
            similarity_threshold=similarity_threshold,
        )

    def load_document(self, file_path: str, embeddings: List[List[float]]) -> None:
        """
        Load a document, split it into chunks, and add to the vector store.

        Args:
            file_path: Path to the document file.
            embeddings: Pre-computed embeddings for the chunks.
        """
        content = self.loader.load(file_path)
        chunks = self.splitter.split_with_metadata(content, source=file_path)
        self.vector_store.add_documents(chunks, embeddings)

    def query(
        self,
        question: str,
        query_embedding: List[float],
        llm_client: Any,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Query the RAG system with a question.

        Args:
            question: The user's question.
            query_embedding: Pre-computed embedding of the question.
            llm_client: LLM client for generating answers.
            system_prompt: Optional custom system prompt.

        Returns:
            Dict with 'answer' and 'sources'.
        """
        if self.vector_store.is_empty:
            return {
                "answer": "请先上传文档",
                "sources": [],
            }

        retrieved_chunks = self.retriever.retrieve(query_embedding)

        if not retrieved_chunks:
            return {
                "answer": "没有找到与问题相关的文档内容",
                "sources": [],
            }

        context = self.retriever.build_context(retrieved_chunks)

        default_system = (
            "你是一个基于文档的问答助手。请根据提供的文档内容回答问题。\n"
            "如果文档中没有相关信息，请说明'我没有找到相关内容'。"
        )

        messages = [
            {"role": "system", "content": system_prompt or default_system},
            {
                "role": "user",
                "content": f"根据以下文档内容回答问题。\n\n{context}\n\n问题: {question}",
            },
        ]

        response = llm_client.chat(messages)
        answer = response.get("content", "") if isinstance(response, dict) else str(response)

        sources = [
            {
                "content": chunk.content,
                "score": chunk.score,
                "source": chunk.source,
                "chunk_index": chunk.chunk_index,
            }
            for chunk in retrieved_chunks
        ]

        return {
            "answer": answer,
            "sources": sources,
        }

    def clear(self) -> None:
        """Clear all documents from the vector store."""
        self.vector_store.clear()

    @property
    def is_empty(self) -> bool:
        """Check if the document store is empty."""
        return self.vector_store.is_empty
