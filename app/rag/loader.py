"""Document loader for PDF, TXT, and Markdown files."""

from pathlib import Path
from typing import Optional

from langchain_community.document_loaders import PyPDFLoader, TextLoader


class DocumentLoader:
    """Loads documents from various file formats."""

    SUPPORTED_FORMATS = {".pdf", ".txt", ".md"}

    @staticmethod
    def load(file_path: str) -> str:
        """
        Load a document and return its text content.

        Args:
            file_path: Path to the document file.

        Returns:
            The text content of the document.

        Raises:
            ValueError: If the file format is not supported.
            FileNotFoundError: If the file does not exist.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        suffix = path.suffix.lower()
        if suffix not in DocumentLoader.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {suffix}. Supported: {DocumentLoader.SUPPORTED_FORMATS}")

        if suffix == ".pdf":
            return DocumentLoader._load_pdf(file_path)
        elif suffix == ".txt":
            return DocumentLoader._load_txt(file_path)
        elif suffix == ".md":
            return DocumentLoader._load_markdown(file_path)

        return ""

    @staticmethod
    def _load_pdf(file_path: str) -> str:
        """Load a PDF file and return its text content."""
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        return "\n".join(doc.page_content for doc in docs)

    @staticmethod
    def _load_txt(file_path: str) -> str:
        """Load a text file and return its content."""
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()
        return "\n".join(doc.page_content for doc in docs)

    @staticmethod
    def _load_markdown(file_path: str) -> str:
        """Load a Markdown file and return its plain text content."""
        # 使用简单的文件读取，不依赖 unstructured 包
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
