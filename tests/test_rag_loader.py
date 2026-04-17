"""Tests for DocumentLoader."""

import tempfile
from pathlib import Path

import pytest

from app.rag.loader import DocumentLoader


class TestDocumentLoader:
    """Test cases for DocumentLoader."""

    def test_load_txt_file(self, tmp_path):
        """Test loading a text file."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("Hello, world!\nThis is a test.")

        content = DocumentLoader.load(str(txt_file))

        assert "Hello, world!" in content
        assert "This is a test." in content

    def test_load_markdown_file(self, tmp_path):
        """Test loading a markdown file."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Title\n\nThis is a test document.")

        content = DocumentLoader.load(str(md_file))

        assert "Title" in content or "Title" in content
        assert "This is a test document." in content

    def test_unsupported_format_raises_error(self, tmp_path):
        """Test that unsupported format raises ValueError."""
        exe_file = tmp_path / "test.exe"
        exe_file.write_text("binary content")

        with pytest.raises(ValueError, match="Unsupported file format"):
            DocumentLoader.load(str(exe_file))

    def test_file_not_found_raises_error(self):
        """Test that non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            DocumentLoader.load("/non/existent/file.txt")

    def test_supported_formats(self):
        """Test that supported formats are correctly defined."""
        assert ".pdf" in DocumentLoader.SUPPORTED_FORMATS
        assert ".txt" in DocumentLoader.SUPPORTED_FORMATS
        assert ".md" in DocumentLoader.SUPPORTED_FORMATS
        assert ".exe" not in DocumentLoader.SUPPORTED_FORMATS
