"""Retriever for semantic document search."""

from dataclasses import dataclass
from typing import List, Optional

from app.rag.store import VectorStore


@dataclass
class RetrievedChunk:
    """A retrieved document chunk with similarity score."""

    content: str
    score: float
    source: str
    chunk_index: int


class Retriever:
    """Retrieves relevant document chunks based on semantic similarity."""

    def __init__(self, vector_store: VectorStore, top_k: int = 4, similarity_threshold: float = 0.0):
        """
        Initialize the retriever.

        Args:
            vector_store: The vector store to search in.
            top_k: Number of top results to return.
            similarity_threshold: Minimum similarity score (0.0 to 1.0).
        """
        self.vector_store = vector_store
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

    def retrieve(self, query_embedding: List[float]) -> List[RetrievedChunk]:
        """
        Retrieve relevant chunks for a query.

        Args:
            query_embedding: The embedding of the query.

        Returns:
            List of RetrievedChunk objects with similarity scores.
        """
        if self.vector_store.is_empty:
            return []

        results = self.vector_store.search(query_embedding, self.top_k)

        retrieved = []
        for chunk, score in results:
            if score >= self.similarity_threshold:
                retrieved.append(
                    RetrievedChunk(
                        content=chunk.content,
                        score=score,
                        source=chunk.source,
                        chunk_index=chunk.chunk_index,
                    )
                )

        return retrieved

    def build_context(self, retrieved_chunks: List[RetrievedChunk]) -> str:
        """
        Build a context string from retrieved chunks.

        Args:
            retrieved_chunks: List of retrieved chunks.

        Returns:
            A formatted context string.
        """
        if not retrieved_chunks:
            return ""

        context_parts = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            context_parts.append(
                f"[Source {i}] ({chunk.source}, chunk {chunk.chunk_index}, score: {chunk.score:.2f})\n{chunk.content}"
            )

        return "\n\n".join(context_parts)
