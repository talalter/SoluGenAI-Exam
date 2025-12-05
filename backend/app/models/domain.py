"""Domain entities."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid


@dataclass
class Chunk:
    """Represents a text chunk with metadata."""

    text: str
    chunk_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    document_id: str = ""
    chunk_index: int = 0
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "document_id": self.document_id,
            "chunk_index": self.chunk_index,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class Document:
    """Represents a source document."""

    content: str
    document_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)
    chunks: List[Chunk] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "document_id": self.document_id,
            "content": self.content[:100] + "..." if len(self.content) > 100 else self.content,
            "num_chunks": len(self.chunks),
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }
