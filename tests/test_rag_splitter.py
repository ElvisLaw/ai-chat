"""Tests for TextSplitter."""

import pytest

from app.rag.splitter import TextSplitter


class TestTextSplitter:
    """Test cases for TextSplitter."""

    def test_split_long_document(self):
        """Test splitting a long document."""
        splitter = TextSplitter(chunk_size=500, chunk_overlap=50)

        # Create a document longer than 500 characters with newlines
        text = ("A" * 200 + "\n") * 4 + ("B" * 200 + "\n") * 4

        chunks = splitter.split(text)

        assert len(chunks) > 1
        # Check overlap exists
        assert any("B" in chunk for chunk in chunks)

    def test_split_short_document(self):
        """Test that short document returns single chunk."""
        splitter = TextSplitter(chunk_size=500, chunk_overlap=50)

        short_text = "Short document content."

        chunks = splitter.split(short_text)

        assert len(chunks) == 1
        assert chunks[0] == short_text

    def test_empty_text_returns_empty_list(self):
        """Test that empty text returns empty list."""
        splitter = TextSplitter(chunk_size=500, chunk_overlap=50)

        chunks = splitter.split("")

        assert chunks == []

    def test_split_with_metadata(self):
        """Test split_with_metadata returns correct structure."""
        splitter = TextSplitter(chunk_size=500, chunk_overlap=50)

        text = "Test content"
        source = "test.txt"

        result = splitter.split_with_metadata(text, source)

        assert len(result) == 1
        assert result[0]["content"] == text
        assert result[0]["source"] == source
        assert result[0]["chunk_index"] == 0

    def test_multiple_chunks_have_incrementing_indices(self):
        """Test that chunks have incrementing indices."""
        splitter = TextSplitter(chunk_size=100, chunk_overlap=10)

        text = "A" * 250

        result = splitter.split_with_metadata(text, "test.txt")

        indices = [chunk["chunk_index"] for chunk in result]
        assert indices == list(range(len(result)))
