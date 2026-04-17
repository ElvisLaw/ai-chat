"""Text splitter for dividing documents into chunks."""

from typing import List

from langchain_text_splitters import CharacterTextSplitter


class TextSplitter:
    """Splits text into overlapping chunks."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize the text splitter.

        Args:
            chunk_size: Maximum number of characters per chunk.
            chunk_overlap: Number of overlapping characters between adjacent chunks.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self._splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def split(self, text: str) -> List[str]:
        """
        Split text into chunks.

        Args:
            text: The text to split.

        Returns:
            List of text chunks.
        """
        if not text or len(text.strip()) == 0:
            return []

        chunks = self._splitter.split_text(text)
        return chunks

    def split_with_metadata(self, text: str, source: str) -> List[dict]:
        """
        Split text into chunks with metadata.

        Args:
            text: The text to split.
            source: The source filename.

        Returns:
            List of dicts with 'content', 'source', and 'chunk_index'.
        """
        chunks = self.split(text)
        return [
            {
                "content": chunk,
                "source": source,
                "chunk_index": i,
            }
            for i, chunk in enumerate(chunks)
        ]
