"""In-memory vector store with cosine similarity."""

import uuid
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import numpy as np


@dataclass
class DocumentChunk:
    """A document chunk with its embedding and metadata."""

    id: str
    content: str
    embedding: List[float]
    source: str
    chunk_index: int


class VectorStore:
    """In-memory vector store for document chunks."""

    def __init__(self):
        """Initialize an empty vector store."""
        self._chunks: List[DocumentChunk] = []

    def add_documents(
        self,
        chunks: List[dict],
        embeddings: List[List[float]],
    ) -> None:
        """
        Add document chunks and their embeddings to the store.

        Args:
            chunks: List of chunk dicts with 'content', 'source', 'chunk_index'.
            embeddings: List of embedding vectors corresponding to chunks.

        Raises:
            ValueError: If the number of chunks doesn't match embeddings.
        """
        if len(chunks) != len(embeddings):
            raise ValueError(
                f"Number of chunks ({len(chunks)}) must match number of embeddings ({len(embeddings)})"
            )

        for chunk, embedding in zip(chunks, embeddings):
            doc_chunk = DocumentChunk(
                id=str(uuid.uuid4()),
                content=chunk["content"],
                embedding=embedding,
                source=chunk["source"],
                chunk_index=chunk["chunk_index"],
            )
            self._chunks.append(doc_chunk)

    def clear(self) -> None:
        """Clear all documents and vectors from the store."""
        self._chunks.clear()

    def search(self, query_embedding: List[float], top_k: int = 4) -> List[Tuple[DocumentChunk, float]]:
        """
        Search for the most similar chunks to a query embedding.

        Args:
            query_embedding: The query embedding vector.
            top_k: Number of top results to return.

        Returns:
            List of (DocumentChunk, similarity_score) tuples.
        """
        if not self._chunks:
            return []

        query_np = np.array(query_embedding)

        similarities = []
        for chunk in self._chunks:
            sim = self._cosine_similarity(query_np, np.array(chunk.embedding))
            similarities.append((chunk, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            a: First vector.
            b: Second vector.

        Returns:
            Cosine similarity score between -1 and 1.
        """
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot_product / (norm_a * norm_b))

    @property
    def is_empty(self) -> bool:
        """Check if the store is empty."""
        return len(self._chunks) == 0

    def __len__(self) -> int:
        """Return the number of chunks in the store."""
        return len(self._chunks)
