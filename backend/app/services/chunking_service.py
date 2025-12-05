"""Text chunking service."""

import re
from typing import List
from app.models.domain import Document, Chunk


class ChunkingService:
    """Handles text chunking with sentence-based strategy."""

    def __init__(self, chunk_size: int = 250, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks at sentence boundaries.

        Args:
            text: Input text to chunk

        Returns:
            List of text chunks
        """
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            # If adding this sentence exceeds chunk size, save current chunk
            if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())

                # Start new chunk with overlap from previous chunk
                overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else current_chunk
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence

        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def process_document(self, document: Document) -> List[Chunk]:
        """
        Convert document into chunks.

        Args:
            document: Document to process

        Returns:
            List of Chunk objects
        """
        text_chunks = self.chunk_text(document.content)

        chunks = []
        for idx, text in enumerate(text_chunks):
            chunk = Chunk(
                text=text,
                document_id=document.document_id,
                chunk_index=idx,
                metadata={
                    "source_file": document.metadata.get("source_file", ""),
                    "chunk_size": len(text),
                }
            )
            chunks.append(chunk)

        return chunks
