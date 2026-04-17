"""Tests for VectorStore."""

import pytest

from app.rag.store import VectorStore


class TestVectorStore:
    """Test cases for VectorStore."""

    def test_add_and_search(self):
        """Test adding documents and searching."""
        store = VectorStore()

        chunks = [
            {"content": "Hello world", "source": "doc1.txt", "chunk_index": 0},
            {"content": "Goodbye world", "source": "doc2.txt", "chunk_index": 0},
        ]
        embeddings = [[1.0, 0.0], [0.0, 1.0]]

        store.add_documents(chunks, embeddings)

        results = store.search([1.0, 0.0], top_k=1)

        assert len(results) == 1
        assert results[0][0].content == "Hello world"

    def test_clear(self):
        """Test clearing the store."""
        store = VectorStore()

        chunks = [{"content": "Test", "source": "test.txt", "chunk_index": 0}]
        embeddings = [[1.0, 0.0]]

        store.add_documents(chunks, embeddings)
        assert len(store) == 1

        store.clear()
        assert len(store) == 0
        assert store.is_empty

    def test_cosine_similarity(self):
        """Test cosine similarity calculation."""
        # Identical vectors
        similarity = VectorStore._cosine_similarity(
            np.array([1.0, 0.0]),
            np.array([1.0, 0.0])
        )
        assert similarity == pytest.approx(1.0)

        # Orthogonal vectors
        similarity = VectorStore._cosine_similarity(
            np.array([1.0, 0.0]),
            np.array([0.0, 1.0])
        )
        assert similarity == pytest.approx(0.0)

        # Opposite vectors
        similarity = VectorStore._cosine_similarity(
            np.array([1.0, 0.0]),
            np.array([-1.0, 0.0])
        )
        assert similarity == pytest.approx(-1.0)

    def test_search_empty_store(self):
        """Test searching empty store returns empty."""
        store = VectorStore()

        results = store.search([1.0, 0.0])

        assert results == []

    def test_is_empty(self):
        """Test is_empty property."""
        store = VectorStore()
        assert store.is_empty is True

        store.add_documents(
            [{"content": "Test", "source": "test.txt", "chunk_index": 0}],
            [[1.0, 0.0]]
        )
        assert store.is_empty is False

    def test_chunks_have_metadata(self):
        """Test that stored chunks preserve metadata."""
        store = VectorStore()

        chunks = [
            {"content": "Content A", "source": "file1.pdf", "chunk_index": 2},
            {"content": "Content B", "source": "file2.txt", "chunk_index": 5},
        ]
        embeddings = [[1.0, 0.0], [0.0, 1.0]]

        store.add_documents(chunks, embeddings)

        results = store.search([1.0, 0.0], top_k=2)
        found = {r[0].source: r[0] for r in results}

        assert found["file1.pdf"].chunk_index == 2
        assert found["file2.txt"].chunk_index == 5


# Import numpy for cosine similarity tests
import numpy as np
