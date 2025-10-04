"""
Create and populate the ChromaDB vector database with entrepreneur biographies.

This script:
1. Loads markdown documents from the current directory
2. Enriches them with metadata from metadata_config.py
3. Splits them into chunks with proper overlap
4. Creates embeddings and stores in ChromaDB
"""

import os
import shutil
from typing import List
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import glob

from metadata_config import DOCUMENT_METADATA

# Load environment variables
load_dotenv()

# Configuration
CHROMA_PATH = "chroma"
DATA_PATH = "transcripts"  # Directory where the markdown files are stored


def main():
    """Main function to orchestrate database creation."""
    print("Starting database creation...")
    generate_data_store()
    print("Database creation complete!")


def generate_data_store():
    """Generate the vector store from documents."""
    # Load documents
    documents = load_documents()
    print(f"Loaded {len(documents)} documents")
    
    # Debug: Print document lengths
    for doc in documents:
        subject = doc.metadata.get("subject", "Unknown")
        print(f"  {subject}: {len(doc.page_content)} characters")
    
    # Split into chunks
    chunks = split_text(documents)
    print(f"Split into {len(chunks)} chunks")
    
    # Debug: Print chunks per subject
    from collections import Counter
    subjects = [c.metadata.get("subject", "Unknown") for c in chunks]
    print(f"Chunks per subject: {dict(Counter(subjects))}")
    
    # Save to ChromaDB
    save_to_chroma(chunks)


def load_documents() -> List[Document]:
    """Load markdown documents and enrich with metadata."""
    # Find all markdown files in the data directory
    md_files = glob.glob(os.path.join(DATA_PATH, "*.md"))
    
    # Enrich each document with metadata
    enriched_documents = []
    for filepath in md_files:
        filename = os.path.basename(filepath)
        
        # Skip if not in our metadata config
        if filename not in DOCUMENT_METADATA:
            print(f"Warning: No metadata found for {filename}, skipping...")
            continue
        
        # Load the file using TextLoader
        try:
            loader = TextLoader(filepath, encoding='utf-8')
            docs = loader.load()
            
            if not docs or len(docs[0].page_content.strip()) == 0:
                print(f"Warning: {filename} appears to be empty, skipping...")
                continue
                
            doc = docs[0]
            
            # Get metadata and convert lists to comma-separated strings for ChromaDB compatibility
            doc_metadata = DOCUMENT_METADATA[filename].copy()
            
            # Convert list fields to strings
            if "themes" in doc_metadata and isinstance(doc_metadata["themes"], list):
                doc_metadata["themes"] = ", ".join(doc_metadata["themes"])
            if "key_concepts" in doc_metadata and isinstance(doc_metadata["key_concepts"], list):
                doc_metadata["key_concepts"] = ", ".join(doc_metadata["key_concepts"])
                
            # Create a new document with enriched metadata
            enriched_doc = Document(
                page_content=doc.page_content,
                metadata={
                    "source": filename,  # Use just the filename
                    **doc_metadata  # Add our custom metadata (with lists converted to strings)
                }
            )
            enriched_documents.append(enriched_doc)
            print(f"Enriched {filename} with metadata ({len(doc.page_content)} chars)")
            
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue
    
    return enriched_documents


def split_text(documents: List[Document]) -> List[Document]:
    """
    Split documents into chunks with improved parameters.
    
    Using:
    - chunk_size: 1200 (middle of 1000-1500 range)
    - chunk_overlap: 250 (middle of 200-300 range)
    - Separators that respect paragraph boundaries
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,  # Increased from 300
        chunk_overlap=250,  # Increased from 100
        length_function=len,
        add_start_index=True,
        # Separators that respect document structure
        separators=[
            "\n\n\n",  # Multiple blank lines (major sections)
            "\n\n",    # Paragraph breaks
            "\n",      # Line breaks
            ". ",      # Sentence ends
            "; ",      # Semi-colons
            ", ",      # Commas
            " ",       # Spaces
            ""         # Individual characters
        ]
    )
    
    chunks = text_splitter.split_documents(documents)
    
    # Add chunk index to metadata for tracking
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i
        chunk.metadata["total_chunks"] = len(chunks)
    
    # Print sample chunk for verification
    if chunks:
        print("\n--- Sample chunk (first chunk) ---")
        print(f"Content preview: {chunks[0].page_content[:200]}...")
        print(f"Metadata: {chunks[0].metadata}")
        print(f"Chunk size: {len(chunks[0].page_content)} characters")
        print("--- End sample ---\n")
    
    return chunks


def save_to_chroma(chunks: List[Document]):
    """Save document chunks to ChromaDB."""
    # Clear existing database
    if os.path.exists(CHROMA_PATH):
        print(f"Clearing existing database at {CHROMA_PATH}")
        shutil.rmtree(CHROMA_PATH)
    
    # Create new database with OpenAI embeddings
    print("Creating embeddings and saving to ChromaDB...")
    db = Chroma.from_documents(
        chunks,
        OpenAIEmbeddings(),
        persist_directory=CHROMA_PATH,
        collection_metadata={"hnsw:space": "cosine"}  # Use cosine similarity
    )
    
    # Persist the database
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}")
    
    # Print some statistics
    print("\n--- Database Statistics ---")
    subjects = set()
    themes = set()
    for chunk in chunks:
        if "subject" in chunk.metadata:
            subjects.add(chunk.metadata["subject"])
        if "themes" in chunk.metadata:
            themes.update(chunk.metadata["themes"])
    
    print(f"Unique subjects: {', '.join(sorted(subjects))}")
    print(f"Unique themes: {', '.join(sorted(themes))}")
    print("--- End Statistics ---\n")


if __name__ == "__main__":
    main()
