"""Tests for Retriever."""

import pytest

from app.rag.retriever import Retriever, RetrievedChunk
from app.rag.store import VectorStore


class TestRetriever:
    """Test cases for Retriever."""

    def test_retrieve_with_results(self):
        """Test retrieving relevant chunks."""
        store = VectorStore()

        chunks = [
            {"content": "Python is a programming language", "source": "doc1.txt", "chunk_index": 0},
            {"content": "Java is another programming language", "source": "doc2.txt", "chunk_index": 0},
        ]
        embeddings = [[1.0, 0.0], [0.0, 1.0]]
        store.add_documents(chunks, embeddings)

        retriever = Retriever(store, top_k=1)

        results = retriever.retrieve([1.0, 0.0])

        assert len(results) == 1
        assert results[0].content == "Python is a programming language"

    def test_retrieve_empty_store(self):
        """Test retrieving from empty store."""
        store = VectorStore()
        retriever = Retriever(store, top_k=4)

        results = retriever.retrieve([1.0, 0.0])

        assert results == []

    def test_retrieve_respects_top_k(self):
        """Test that retrieval respects top_k parameter."""
        store = VectorStore()

        chunks = [
            {"content": f"Chunk {i}", "source": f"doc{i}.txt", "chunk_index": 0}
            for i in range(5)
        ]
        embeddings = [[1.0 if i == 0 else 0.0, 0.0 if i == 0 else 1.0] for i in range(5)]
        store.add_documents(chunks, embeddings)

        retriever = Retriever(store, top_k=3)

        results = retriever.retrieve([1.0, 0.0])

        assert len(results) == 3

    def test_build_context(self):
        """Test building context string from chunks."""
        store = VectorStore()
        retriever = Retriever(store)

        chunks = [
            RetrievedChunk(
                content="First chunk content",
                score=0.9,
                source="doc1.txt",
                chunk_index=0
            ),
            RetrievedChunk(
                content="Second chunk content",
                score=0.8,
                source="doc2.txt",
                chunk_index=1
            ),
        ]

        context = retriever.build_context(chunks)

        assert "First chunk content" in context
        assert "Second chunk content" in context
        assert "doc1.txt" in context
        assert "doc2.txt" in context

    def test_build_context_empty(self):
        """Test building context from empty chunks."""
        store = VectorStore()
        retriever = Retriever(store)

        context = retriever.build_context([])

        assert context == ""
