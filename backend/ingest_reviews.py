"""
Script to ingest Women's Clothing Reviews dataset and create embeddings.

This script:
1. Loads the processed_reviews.csv dataset
2. Combines Title and Review Text for each row
3. Chunks the text using the chunking service
4. Generates embeddings using OpenAI
5. Stores embeddings in ChromaDB vector database
"""

import asyncio
import pandas as pd
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

from app.services.embedding_service import EmbeddingService
from app.services.chunking_service import ChunkingService
from app.services.vector_store import VectorStore
from app.models.domain import Document


async def ingest_dataset():
    """Main ingestion function."""

    # Load environment variables directly
    load_dotenv()

    # Get configuration from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    chunk_size = int(os.getenv("CHUNK_SIZE", "250"))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "50"))
    embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    chroma_persist_dir = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    chroma_collection = os.getenv("CHROMA_COLLECTION_NAME", "rag_documents")

    if not openai_api_key:
        print("\nError: OPENAI_API_KEY not found in .env file")
        sys.exit(1)

    print("=" * 60)
    print("RAG RETRIEVAL SYSTEM - DATASET INGESTION")
    print("=" * 60)
    print(f"\nConfiguration:")


    # Initialize services
    embedding_service = EmbeddingService(
        api_key=openai_api_key
    )
    chunking_service = ChunkingService(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    vector_store = VectorStore(
        collection_name=chroma_collection,
        persist_directory=chroma_persist_dir
    )

    # Load dataset (relative to script location)
    script_dir = Path(__file__).parent
    dataset_path = script_dir / "data" / "processed_reviews.csv"
    if not dataset_path.exists():
        print(f"\nError: Dataset not found at {dataset_path}")
        sys.exit(1)

    print(f"\nLoading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"   Loaded {len(df)} reviews")

    # Convert rows to documents
    # Combine Title and Review Text for better context
    documents = []
    for idx, row in df.iterrows():
        # Combine title and review text
        title = str(row.get('Title', ''))
        review = str(row.get('Review Text', ''))

        # Create combined text
        if title and review:
            content = f"{title}. {review}"
        elif review:
            content = review
        elif title:
            content = title
        else:
            continue  # Skip empty rows

        # Create document with metadata
        doc = Document(
            content=content,
            metadata={
                "source_file": "processed_reviews.csv",
                "row_index": int(idx),
                "age": str(row.get('Age', '')),
                "age_category": str(row.get('Age Category', '')),
                "division": str(row.get('Division Name', '')),
                "department": str(row.get('Department Name', '')),
                "class": str(row.get('Class Name', '')),
            }
        )
        documents.append(doc)

    print(f"   Created {len(documents)} documents")

    # Chunk all documents
    print(f"\nChunking documents...")
    all_chunks = []
    for doc in documents:
        chunks = chunking_service.process_document(doc)
        all_chunks.extend(chunks)

    print(f"   Created {len(all_chunks)} chunks")
    print(f"   Average chunk size: {sum(len(c.text) for c in all_chunks) / len(all_chunks):.1f} characters")

    # Generate embeddings
    print(f"\nGenerating embeddings using {embedding_model}...")
    chunk_texts = [chunk.text for chunk in all_chunks]

    try:
        embeddings = await embedding_service.embed_batch(chunk_texts)
        print(f"   Generated {len(embeddings)} embeddings")
        print(f"   Embedding dimensions: {len(embeddings[0])}")

        # Assign embeddings to chunks
        for chunk, embedding in zip(all_chunks, embeddings):
            chunk.embedding = embedding

    except Exception as e:
        print(f"\nError generating embeddings: {e}")
        sys.exit(1)

    # Store in vector database
    print(f"\nStoring chunks in ChromaDB...")
    try:
        await vector_store.add_chunks(all_chunks)
        stored_count = vector_store.count()
        print(f"   Successfully stored {stored_count} chunks")

    except Exception as e:
        print(f"\nError storing chunks: {e}")
        sys.exit(1)

    # Display sample chunks
    print(f"\nSample Chunks:")
    for i, chunk in enumerate(all_chunks[:3], 1):
        print(f"\n   Chunk {i} (ID: {chunk.chunk_id[:8]}...):")
        print(f"   Text: {chunk.text[:100]}...")
        print(f"   Metadata: Age={chunk.metadata.get('age_category', 'N/A')}, "
              f"Dept={chunk.metadata.get('department', 'N/A')}")

    print("\n" + "=" * 60)
    print("INGESTION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nEmbeddings are stored in: {chroma_persist_dir}")
    print("You can now start the API server and query the system.")
    print("\nNext steps:")
    print("  1. Start backend: uvicorn main:app --reload")
    print("  2. Start frontend: cd ../frontend && npm run dev")
    print("  3. Open browser: http://localhost:5173")


if __name__ == "__main__":
    asyncio.run(ingest_dataset())
